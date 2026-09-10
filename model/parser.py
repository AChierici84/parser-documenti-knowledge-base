from abc import abstractmethod

class DocumentParser:
    def __init__(self):
        self.extension = None

    def get_extension(self):
        """
        Extension
        """
        return self.extension

    @abstractmethod
    def parse(self, file_path: str) -> str:
        """Abstract method to parsare a file."""
        pass


