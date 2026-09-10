import os
import json
import math
import re
import datetime
from logging import Logger
from typing import List
from document import Document
from parser import DocumentParser
from collections import defaultdict

class DocumentIndex:
    """
    Class representing document index
    """
    def __init__(self, file_path,inverted_file_path, logger:Logger):
        self.file_path = file_path
        self.inverted_file_path=inverted_file_path
        self.index= []
        self.documents= []
        self.inverted_index= {}
        self.logger = logger
        
        if not os.path.exists(file_path):
            # if not exists, create new index
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
            logger(f"File '{file_path}' not found. New index file created.")
        else:
            # if exists, load data
            with open(file_path, 'r', encoding='utf-8') as f:
                index = json.load(f)
            
            # json to Documents
            self.documents = [Document.from_dict(d) for d in index]
            logger(f"Loaded {len(self.documents)} documents from JSON file.")

        if not os.path.exists(inverted_file_path):
            # if not exists, create new index
            with open(inverted_file_path, 'w', encoding='utf-8') as f:
                json.dump({}, f)
            logger(f"File '{file_path}' not found. New inverted index file created.")
        else:
            # if exists, load data
            with open(file_path, 'r', encoding='utf-8') as f:
                self.inverted_index = json.load(f)
            logger(f"Loaded inverted index JSON file.")        
    
    def add_document(self,document:Document,logger:Logger):
        self.documents.append(document)
        self.index.append(document.to_dict())
        logger.debug(f"document.file_name (document.doc_id) saved")
        self.save_index()

    def title_from_filename(self, title,logger):
        """
        get title from filename
        """
        normalized_title = (
        title
        .replace("-", " ")
        .replace("_", " ")
        .replace("!", " ")
        .replace(":", " ")
        .replace("@", " ")
        .replace("#", " ")
        .replace("$", " ")
        .replace("%", " ")
        .replace("^", " ")
        .replace("&", " ")
        .replace("*", " ")
        .replace("(", " ")
        .replace(")", " ")
        )

        # Rimuovi spazi doppi usando espressioni regolari
        cleaned_title = re.sub(r'\s+', ' ', normalized_title).strip()

        logger.debug("Testo originale:", title)
        logger.debug("Testo normalizzato:", normalized_title)
        logger.debug("Testo pulito:", cleaned_title)
        return cleaned_title

    def add_folder(self, folder, parsers: list[DocumentParser],logger:Logger):
        for root, dirs, files in os.walk(folder):
                for file in files:
                    logger.debug(f"parsing file {file}")
                    filename= os.path.splitext(file)[0]
                    extension=os.path.splitext(file)[1]
                    for parser in parsers:
                        if parser.get_extension == extension:
                            content = parser.parse(os.path.join(folder,filename))
                            doc_id = parser.get_doc_id(content)
                            abstract = content[0,math.Min()]
                            title= self.title_from_filename(filename)
                            modification_timestamp = os.path.getmtime(os.path.join(folder,filename))
                            modification_time = datetime.datetime.fromtimestamp(modification_timestamp)
                            words = re.findall(r'\b\w+\b', title.lower()+" "+content.lower())
                            # Popola l'inverted index
                            for word in words:
                                if doc_id not in self.inverted_index[word]:
                                    self.inverted_index[word].append(doc_id)
                            num_words = len(words)
                    #TODO gestire no parser found 
                    new_document = Document(doc_id,folder,filename,title,modification_time,num_words,abstract,content,extension)
                    self.add_document(new_document)

                for dir in dirs:
                    self.add_folder(dir)

        self.save_index()

    def search(self, search,logger:Logger):
        words = re.findall(r'\b\w+\b', search.lower())
        doc_scores = defaultdict(float)

        # Calcolate scores
        for word in words:
            if word in self.inverted_index:
                # for every matching word add 1 to score
                for doc_id in self.inverted_index[word]:
                    doc_scores[doc_id] += 1 

        # order documents for score descending
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x, reverse=True)

        #get doc_ids
        doc_id_to_doc = {doc["doc_id"]: doc for doc in self.documents}

        results = []
        for doc_id, score in sorted_docs:
            if doc_id in doc_id_to_doc:
                results.append((doc_id_to_doc[doc_id], score))

        if logger:
            logger.info(f"Trovati {len(results)} risultati per la query: '{search}'")

        return results

    
    def save_index(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.index, f)
        # Save inverted index
        with open(self.inverted_file_path, "w") as f:
            json.dump(dict(self.inverted_file_path), f)

    
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
        self.inverted_index=[]
        self.documents = []
        self.save_index()

    def update_index(self):
        #get all folders
        folders=[]
        for document in self.documents:
            if document.folder in folders:
                folders.append(folder)
        self.empty_index()
        for folder in folders:
            self.add_folder(folder)
             

    



        




    

  
