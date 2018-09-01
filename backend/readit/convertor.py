import os
import subprocess
import tempfile
from typing import ClassVar, Dict, List

from chardet import UniversalDetector

from .helpers import sliced


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

    @classmethod
    def add_converter(cls, fmt: str):
        """Add converter class to the list of available converters"""

        def wrapper(converter: ConverterPluginType):
            cls._converters[fmt] = converter

        return wrapper

    def convert(self, content: bytes) -> List[str]:
        return self.converter.convert(content)


@Converter.add_converter("txt")
class _TextConverter:
    page_length = 5000  # chars

    @staticmethod
    def _get_encoding(content: bytes) -> str:
        detector = UniversalDetector()
        for line in sliced(content, 250):
            detector.feed(line)
            if detector.done:
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
    @staticmethod
    def convert(text: bytes) -> List[str]:
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(text)
            out_name = tmp.name + ".txt"
            try:
                res = subprocess.run(
                    f"pdftotext -eol unix -layout {tmp.name} {out_name}".split(" ")
                )
            except subprocess.CalledProcessError as err:
                raise ConvertError(f"Failed to convert file. {res.stdout}") from err
            try:
                with open(out_name) as out:
                    return out.read().split("\f")
            finally:
                os.remove(out_name)
