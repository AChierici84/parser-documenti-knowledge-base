from abc import abstractmethod
import hashlib
from model.custom_exceptions import ParsingException, MissingParserException

class DocumentParser:
    def __init__(self):
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
        hash_object = hashlib.sha256(content)
        doc_id = hash_object.hexdigest()[:16] #first 16 chars
        return doc_id

    @abstractmethod
    def parse(self, file_path: str) -> str:
        """Abstract method to parsare a file."""
        raise MissingParserException(
            f"Parsing non implementato per il file: {file_path}"
        )


