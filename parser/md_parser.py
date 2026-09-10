from parser.parser import DocumentParser

class MdParser(DocumentParser):
    """
    Parser for MD file
    """
    def parse(self,file_path):
        """
        Parse Method
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return self.extract_text(content)

    def extract_plain_text(self, content):
        """
        extract plain text from md file
        """
        plain_text = content.replace('#','')
        return plain_text