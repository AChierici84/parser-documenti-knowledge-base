import csv
from model.parser import DocumentParser

class CSVParser(DocumentParser):
    """
    Parser for CSV file
    """
    def __init__(self):
        self.extension = "csv|tsv"
        self.CSV_reader = None
    
    def parse(self,file_path):
        """
        Parse Method
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            CSV_reader = csv.reader(file)

            # Reead line by line
            for row in CSV_reader:
                content += row + "\n"

        return content
