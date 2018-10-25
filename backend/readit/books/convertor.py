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

from readit.helpers import sliced, classproperty


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
                f"Choose one of: {self.supported_formats}."
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
        safe_pages = (self._sanitize(page) for page in pages)
        return [page for page in safe_pages if page]

    @classproperty
    def supported_formats(cls) -> List[str]:
        return list(cls._converters.keys())


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

    @staticmethod
    def _add_html_tags(text: str) -> str:
        return text.replace("  ", "&nbsp;&nbsp;").replace("\n", "<br>")

    @classmethod
    def convert(cls, content: bytes) -> List[str]:
        encoding = cls._get_encoding(content)
        text = content.decode(encoding, errors="ignore")
        # todo: be smarter with page breaks, do not cut words
        sliced_text = sliced(text, cls.page_length)
        return [cls._add_html_tags(page) for page in sliced_text]


@Converter.add_converter("pdf")
class _PDFConverter:
    body_regexp = re.compile(rb"<body[^>]*>(.*)</body>", re.DOTALL | re.IGNORECASE)

    @classmethod
    def _extract_body(cls, text: bytes) -> bytes:
        res = cls.body_regexp.search(text)
        if res is not None:
            return res.group(1)
        return b""

    @classmethod
    def _extract_content(cls, text: bytes, to: str) -> bytes:
        in_name = f"{to}/in_file"
        with open(in_name, "wb") as fh:
            fh.write(text)
        try:
            res = subprocess.run(
                f"pdftohtml -p -noframes -nomerge -stdout {in_name}".split(" "),
                capture_output=True,
                check=True,
            )
        except subprocess.CalledProcessError as err:
            raise ConvertError(f"Failed to convert file. {res.stdout}") from err
        html_content = res.stdout
        return cls._extract_body(html_content).strip()

    @staticmethod
    def _extract_images_content(path: str) -> Dict[bytes, bytes]:
        images = [file for file in os.listdir(path) if file.endswith((".jpg", ".png"))]
        images_data = {}
        for image in images:
            img_path = os.path.join(path, image)
            with open(img_path, "rb") as fh:
                images_data[img_path.encode("utf-8")] = base64.b64encode(fh.read())
        return images_data

    @staticmethod
    def _insert_images(html: bytes, images: Dict[bytes, bytes]) -> bytes:
        for img_name, img_content in images.items():
            extension = img_name.split(b".")[-1].lower()
            img_data = b"data:image/%s;base64,%s" % (extension, img_content)
            html = html.replace(img_name, img_data)
        return html

    @staticmethod
    def _split_html(html: str) -> List[str]:
        return [page.strip() for page in html.split("<hr/>")]

    @classmethod
    def convert(cls, data: bytes) -> List[str]:
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_html = cls._extract_content(data, to=tmp_dir)
            images = cls._extract_images_content(tmp_dir)
            out_html = cls._insert_images(out_html, images)
        pages = cls._split_html(out_html.decode("utf-8"))
        return pages


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
