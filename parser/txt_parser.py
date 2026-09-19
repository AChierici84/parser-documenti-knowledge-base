from model.parser import DocumentParser
from model.custom_exceptions import ParsingException
class TxtParser(DocumentParser):
    """
    Parser for TXT file
    """
    def __init__(self):
        """
        Initialize the TXT parser.
        """
        self.extension = "txt"

    def parse(self,file_path):
        """
        Parse the TXT file and return its content as a string.

        Args:
            file_path (str): Path to the TXT file.

        Returns:
            str: Content of the TXT file.
        """
        content = ""
        try:
            with open(file_path, 'r', encoding=self.detect_encoding(file_path)) as f:
                content = f.read()
                return content
        except Exception as e:
            raise ParsingException(f"Error parsing TXT file {file_path}: {e}")