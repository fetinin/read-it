import datetime
import os
import subprocess
import tempfile
from typing import ClassVar, Dict, List, Type

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


class Converter:
    _converters: ClassVar[Dict[str, ConverterPluginType]] = {}

    def __init__(self, converter_type):
        try:
            self.converter: ConverterPluginType = self._converters[converter_type]
        except KeyError:
            raise UnsupportedFormatError(
                f"{converter_type} format is not supported. "
                f"Choose one of: {self._converters.keys()}."
            )

    @staticmethod
    def _sanitize(text: str):
        """Escape html tags"""
        return bleach.clean(text)

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
