from model.parser import DocumentParser
from model.custom_exceptions import ParsingException
class TxtParser(DocumentParser):
    """
    Parser for MD file
    """
    def __init__(self):
        self.extension = "txt"

    def parse(self,file_path):
        """
        Parse Method
        """
        content = ""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return content
        except Exception as e:
            raise ParsingException(f"Error parsing TXT file {file_path}: {e}")