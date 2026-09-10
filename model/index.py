import os
import json
import math
import re
import datetime
from logging import Logger
from document import Document
from parser import DocumentParser

class DocumentIndex:
    """
    Class representing document index
    """
    def __init__(self, file_path, logger):
        self.file_path = file_path
        self.index= []
        self.documents= []
        self.logger = logger
        
        if not os.path.exists(file_path):
            # if not exists, create new index
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
            print(f"File '{file_path}' not found. New index file created.")
        else:
            # if exists, load data
            with open(file_path, 'r', encoding='utf-8') as f:
                index = json.load(f)
            
            # json to Documents
            self.documents = [Document.from_dict(d) for d in index]
            print(f"Loaded {len(self.documents)} documents from JSON file.")
    
    def add_document(self,document:Document):
        self.documents.append(document)
        self.index.append(document.to_dict())
        self.save_index()

    def title_from_filename(self, title):
        """
        get title from filename
        """
        return title.replace("-"," ").replace("_"," ")

    def add_folder(self, folder, parsers: list[DocumentParser],logger:Logger):
        for root, dirs, files in os.walk(folder):
                for file in files:
                    logger.debug(f"parsing file {file}")
                    filename= os.path.splitext(file)
                    extension=os.path.splitext(file)
                    for parser in parsers:
                        if parser.get_extension == extension:
                            content = parser.parse(os.path.join(folder,filename))
                            doc_id = parser.get_doc_id(content)
                            abstract = content[0,math.Min()]
                            modification_timestamp = os.path.getmtime(os.path.join(folder,filename))
                            modification_time = datetime.datetime.fromtimestamp(modification_timestamp)
                            words = re.findall(r'\b\w+\b', content.toLower())
                            num_words = len(words)
                    #TODO gestire no parser found 
                    new_document = Document(doc_id,folder,filename,self.title_from_filename(filename),modification_time,num_words,abstract,content,extension)
                    self.add_document(new_document)

                for dir in dirs:
                    self.add_folder(dir)

        self.save_index()

    def search(self, search,logger:Logger):
        words = re.findall(r'\b\w+\b', search.toLower())

    
    def save_index(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.index, f)
    
    def remove_document(self, document:Document):
        start_len=len(self.documents)

        # Filter list for path to remove
        self.documents[:] = [doc for doc in self.documents if doc.path != document.path]
        self.index[:] = [r for r in self.index if r["path"] != document.path]
        
        if len(self.documents) < start_len:
            self.save_index();
            print(f"Document with path '{document.path}' removed.")
        else:
            print(f"Document with path '{document.path}' not found.")
    
    def edit_document(self, edit_document:Document):
        found= False;

        for doc in self.documents:
            if doc.file_name == edit_document.file_name:
                found= True;
                doc.folder = edit_document.folder
                doc.path = edit_document.path
                doc.dimension = edit_document.dimension
                doc.title =  edit_document.title
                doc.date =  edit_document.date
                doc.num_words =  edit_document.num_words
                doc.extract =  edit_document.extract
                doc.content =  edit_document.content
                doc.format =  edit_document.format
        
        for doc in self.index:
            if doc.file_name == edit_document.file_name:
                doc.folder = edit_document.folder
                doc.path = edit_document.path
                doc.dimension = edit_document.dimension
                doc.title =  edit_document.title
                doc.date =  edit_document.date
                doc.num_words =  edit_document.num_words
                doc.extract =  edit_document.extract
                doc.content =  edit_document.content
                doc.format =  edit_document.format
        if (found):
            self.save_index()
            print(f"Document with file name '{edit_document.file_name}' edited.")
        else:
            print(f"Document with file name '{edit_document.file_name}' not found.")

    def empty_index(self):
        self.index= []
        self.documents = []
        self.save_index()

    def update_index(self):
        for document in self.documents:
            path = document.path
             

    



        




    

  
