import base64
import datetime
import os
import re
import subprocess
import tempfile
from collections import namedtuple
from io import BytesIO
from typing import ClassVar, Dict, List, Tuple, Type
from zipfile import ZipFile

import bleach
from chardet import UniversalDetector

from readit.helpers import sliced


class UnsupportedFormatError(Exception):
    pass


class ConvertError(Exception):
    pass


class ConverterPluginType:
    def convert(self, content: bytes) -> List[str]:
        ...


class BleachSanitizer:
    class BlackList(list):
        forbidden_tags = {"script", "a", "style"}

        def __contains__(self, item):
            return item not in self.forbidden_tags

    forbidden_html_tags = BlackList()
    allowed_attrs = {"img": {"alt", "height", "width", "src"}}

    def sanitize(self, text):
        return bleach.clean(
            text,
            tags=self.forbidden_html_tags,
            attributes=self.allowed_attrs,
            protocols=["data"],
            strip=True,
        )


class Converter:
    _converters: ClassVar[Dict[str, Type[ConverterPluginType]]] = {}
    sanitizer = BleachSanitizer()

    def __init__(self, converter_type):
        try:
            self.converter: ConverterPluginType = self._converters[converter_type]
        except KeyError:
            raise UnsupportedFormatError(
                f"{converter_type} format is not supported. "
                f"Choose one of: {self._converters.keys()}."
            )

    @classmethod
    def _sanitize(cls, text: str):
        """Escape html tags"""
        return cls.sanitizer.sanitize(text)

    @classmethod
    def add_converter(cls, fmt: str):
        """Add converter class to the list of available converters"""

        def wrapper(converter: Type[ConverterPluginType]):
            cls._converters[fmt] = converter

        return wrapper

    def convert(self, content: bytes) -> List[str]:
        pages = self.converter.convert(content)
        return [self._sanitize(page) for page in pages]


@Converter.add_converter("txt")
class _TextConverter:
    page_length = 5000  # chars

    @staticmethod
    def _get_encoding(content: bytes) -> str:
        detector = UniversalDetector()
        timeout = datetime.datetime.now() + datetime.timedelta(seconds=5)
        for line in sliced(content, 2500):
            detector.feed(line)
            if detector.done or datetime.datetime.now() > timeout:
                break
        detector.close()
        return detector.result["encoding"]

    @classmethod
    def convert(cls, content: bytes) -> List[str]:
        encoding = cls._get_encoding(content)
        # todo: be smarter with page breaks, do not cut words
        return list(sliced(str(content, encoding), cls.page_length))


@Converter.add_converter("pdf")
class _PDFConverter:
    @classmethod
    def _extract_text(cls, text: bytes) -> str:
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(text)
            out_name = f"{tmp.name}.txt"
            try:
                res = subprocess.run(
                    f"pdftotext -eol unix -layout {tmp.name} {out_name}".split(" ")
                )
            except subprocess.CalledProcessError as err:
                raise ConvertError(f"Failed to convert file. {res.stdout}") from err
            try:
                with open(out_name) as out:
                    return out.read()
            finally:
                os.remove(out_name)

    @classmethod
    def convert(cls, data: bytes) -> List[str]:
        text = cls._extract_text(data)
        return text.strip().split("\f")


@Converter.add_converter("epub")
class _EpubConverter:
    file_obj = namedtuple("FileObj", "name content")
    body_regexp = re.compile(rb"<body>(.*)</body>", re.DOTALL | re.IGNORECASE)
    anchor_regexp = re.compile(rb"<a.+>(.+)</a>", re.IGNORECASE)

    @classmethod
    def _extract_zip_content(cls, stream) -> Tuple[List[file_obj], List[file_obj]]:
        with ZipFile(stream) as zip_file:
            pages = []
            images = []
            for file in zip_file.filelist:
                if file.filename.endswith(".html"):
                    with zip_file.open(file) as fh:
                        name = file.filename.split(os.sep)[-1]
                        pages.append(cls.file_obj(name.encode("utf-8"), fh.read()))
                if file.filename.endswith(".jpg"):
                    with zip_file.open(file) as fh:
                        name = file.filename.split(os.sep)[-1]
                        images.append(cls.file_obj(name.encode("utf-8"), fh.read()))
            return pages, images

    @classmethod
    def _extract_body(cls, text: bytes) -> bytes:
        res = cls.body_regexp.search(text)
        if res is not None:
            return res.group(1)
        return b""

    @staticmethod
    def _images_to_base64_url(images: List[file_obj]) -> List[Tuple[bytes, bytes]]:
        return [
            (image.name, b"data:image/jpeg;base64,%s" % base64.b64encode(image.content))
            for image in images
        ]

    @staticmethod
    def _replace_images(
        content: bytes, images_urls: List[Tuple[bytes, bytes]]
    ) -> bytes:
        for name, img in images_urls:
            content = content.replace(name, img)
        return content

    @classmethod
    def _extract_pages(cls, data: bytes):
        pages, images = cls._extract_zip_content(BytesIO(data))
        images_urls = cls._images_to_base64_url(images)
        pages_processed = []
        for page in pages:
            content = cls._extract_body(page.content)
            content = cls._replace_images(content, images_urls)
            pages_processed.append(content)
        return pages_processed

    @classmethod
    def convert(cls, data: bytes) -> List[str]:
        return [page.decode("utf-8") for page in cls._extract_pages(data)]
