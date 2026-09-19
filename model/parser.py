from abc import abstractmethod
import hashlib
import chardet
from model.custom_exceptions import ParsingException, MissingParserException

class DocumentParser:
    """Base class for document parsers."""
    def __init__(self):
        """
        Initialize the document parser.
        """
        self.extension = None

    def get_extension(self):
        """
        Extension
        """
        return self.extension

    def get_doc_id(self,content):
        """
        Method to generate doc id
        """
        hash_object = hashlib.sha256(content.encode('utf-8'))
        doc_id = hash_object.hexdigest()[:16] #first 16 chars
        return doc_id

    def detect_encoding(self, file_path):
        """
        Detect the encoding of a file.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: Detected encoding of the file.
        """
        with open(file_path, 'rb') as file:
            detector = chardet.universaldetector.UniversalDetector()
            for line in file:
                detector.feed(line)
                if detector.done:
                    break
            detector.close()
        return detector.result['encoding']

    @abstractmethod
    def parse(self, file_path: str) -> str:
        """Abstract method to parse a file."""
        raise MissingParserException(
            f"Parsing non implementato per il file: {file_path}"
        )


