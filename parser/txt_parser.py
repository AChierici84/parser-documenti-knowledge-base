from parser.parser import DocumentParser

class TxtParser(DocumentParser):
    """
    Parser for MD file
    """
    def parse(self,file_path):
        """
        Parse Method
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return content