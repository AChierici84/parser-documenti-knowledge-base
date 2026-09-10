from model.parser import DocumentParser

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
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return content