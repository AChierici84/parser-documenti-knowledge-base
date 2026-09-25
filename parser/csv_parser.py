import csv
from model.parser import DocumentParser
from model.custom_exceptions import ParsingException, MissingParserException

class CSVParser(DocumentParser):
    """
    Parser for CSV file
    """
    def __init__(self):
        """
        Initialize the CSV parser.
        """
        self.extension = "csv|tsv"
        self.CSV_reader = None
    
    def parse(self,file_path):
        """
        Parse the CSV file and return its content as a string.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            str: Content of the CSV file.
        """
        content = ""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                CSV_reader = csv.reader(file)

                # Read the file row by row.
                for row in CSV_reader:
                    content += ",".join(row) + "\n"

            return content
        except Exception as e:
            raise ParsingException(f"Error parsing CSV file {file_path}: {e}")
