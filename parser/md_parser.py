import re

from model.parser import DocumentParser
from model.custom_exceptions import ParsingException

class MdParser(DocumentParser):
    """
    Parser for MD file
    """
    def __init__(self):
        self.extension = "md"

    def parse(self,file_path):
        """
        Parse Method for MD file
        """
        content = ""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return self.extract_plain_text(content)
        except Exception as e:
            raise ParsingException(f"Error parsing MD file {file_path}: {e}")

    def extract_plain_text(self, content):
        """
        extract plain text from md file
        """
        # Remove Markdown syntax while keeping the text represented by it.
        plain_text = re.sub(r'^\ufeff?---\s*$.*?^---\s*$', '', content,
                            flags=re.MULTILINE | re.DOTALL)
        plain_text = re.sub(r'```[^\n]*\n|```', '', plain_text)
        plain_text = re.sub(r'!?\[([^\]]+)\]\([^)]*\)', r'\1', plain_text)
        plain_text = re.sub(r'<[^>]+>', '', plain_text)
        plain_text = re.sub(r'^\s{0,3}#{1,6}\s+', '', plain_text,
                            flags=re.MULTILINE)
        plain_text = re.sub(r'^\s{0,3}>\s?', '', plain_text,
                            flags=re.MULTILINE)
        plain_text = re.sub(r'^\s*(?:[-+*]|\d+[.)])\s+', '', plain_text,
                            flags=re.MULTILINE)
        plain_text = re.sub(r'[*_~`]', '', plain_text)
        plain_text = re.sub(r'^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$',
                            '', plain_text, flags=re.MULTILINE)
        plain_text = plain_text.replace('\\', '')
        plain_text = re.sub(r'\n{3,}', '\n\n', plain_text)
        return plain_text.strip()