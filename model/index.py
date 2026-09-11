import os
import json
import math
import re
import datetime
from logging import Logger
from typing import List
from model.document import Document
from model.custom_exceptions import FolderNotFoundException, InvertedIndexException, MissingParserException, ParsingException, IndexingException, DuplicateDocumentException
from model.parser import DocumentParser
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
        self.total_documents = 0
        self.errors = []
        
        if not os.path.exists(file_path):
            # if not exists, create new index
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
            self.logger.debug(f"File '{file_path}' not found. New index file created.")
        else:
            # if exists, load data
            with open(file_path, 'r', encoding='utf-8') as f:
                index = json.load(f)
            
            # json to Documents
            self.documents = [Document.from_dict(d) for d in index]
            self.logger.debug(f"Loaded {len(self.documents)} documents from JSON file.")
            self.total_documents = len(self.documents)

        if not os.path.exists(inverted_file_path):
            # if not exists, create new index
            with open(inverted_file_path, 'w', encoding='utf-8') as f:
                json.dump({}, f)
            self.logger.debug(f"File '{inverted_file_path}' not found. New inverted index file created.")
        else:
            # if exists, load data
            with open(inverted_file_path, 'r', encoding='utf-8') as f:
                self.inverted_index = json.load(f)
            self.logger.debug(f"Loaded inverted index JSON file.")        
    
    def add_document(self,document:Document):
        try:
            self.documents.append(document)
            self.index.append(document.to_dict())
            self.logger.debug(f"{document.file_name} ({document.doc_id}) saved")
            self.total_documents += 1
            self.save_index()
        except IndexingException as e:
            self.errors.append(f"Error adding document {document.file_name}: {e}")
            self.logger.error(f"Error adding document {document.file_name}: {e}")

    def title_from_filename(self, title):
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

        self.logger.debug(f"Testo originale: {title}")
        self.logger.debug(f"Testo normalizzato: {normalized_title}")
        self.logger.debug(f"Testo pulito: {cleaned_title}")
        return cleaned_title

    def add_folder(self, folder, parsers: list[DocumentParser]):
        for root, dirs, files in os.walk(folder):
                for file in files:
                    try:
                        parser_found = False
                        self.logger.debug(f"parsing file {file}")
                        filename= os.path.splitext(file)[0]
                        extension=os.path.splitext(file)[1]
                        for parser in parsers:
                            if parser.get_extension() == extension:
                                self.logger.debug(f"using parser {parser.__class__.__name__} for file {file}")
                                parser_found = True
                                content = parser.parse(os.path.join(folder,file))
                                doc_id = parser.get_doc_id(content)
                                abstract = content[0:min(len(content), 100)]
                                title= self.title_from_filename(filename)
                                modification_timestamp = os.path.getmtime(os.path.join(folder,file))
                                modification_time = datetime.datetime.fromtimestamp(modification_timestamp)
                                words = re.findall(r'\b\w+\b', title.lower()+" "+content.lower())
                                # Popola l'inverted index
                                for word in words:
                                    if doc_id not in self.inverted_index[word]:
                                        self.inverted_index[word].append(doc_id)
                                num_words = len(words)
                        
                        if not parser_found:
                            self.logger.warning(f"No parser found for file {file}")
                            raise MissingParserException(f"No parser found for file {file}")
                        new_document = Document(doc_id,folder,filename,title,modification_time,num_words,abstract,content,extension)
                        doc_id_to_doc = {doc["doc_id"]: doc for doc in self.documents}
                        if doc_id not in doc_id_to_doc:
                            self.add_document(new_document)
                        else:
                            self.logger.warning(f"Document with ID {doc_id} already exists in the index.")
                            raise DuplicateDocumentException(f"Document with ID {doc_id} already exists in the index.")
                    except DuplicateDocumentException as e:
                        self.logger.error(f"Duplicate document for file {file}: {e}")
                        self.errors.append(f"Duplicate document for file {file}: {e}")
                        continue
                    except MissingParserException as e:
                        self.logger.error(f"Missing parser for file {file}: {e}")
                        self.errors.append(f"Missing parser for file {file}: {e}")
                        continue
                    except IndexingException as e:
                        self.logger.error(f"Indexing error for file {file}: {e}")
                        self.errors.append(f"Indexing error for file {file}: {e}")
                        continue
                    except ParsingException as e:
                        self.logger.error(f"Parsing error for file {file}: {e}")
                        self.errors.append(f"Parsing error for file {file}: {e}")
                        continue
                    except Exception as e:
                        self.logger.error(f"Error processing file {file}: {e}")
                        self.errors.append(f"Error processing file {file}: {e}")
                        continue

                for dir in dirs:
                    self.add_folder(os.path.join(folder,dir))

        self.save_index()

    def search(self, search):
        words = re.findall(r'\b\w+\b', search.lower())
        doc_scores = defaultdict(float)

        if not self.inverted_index:
            raise InvertedIndexException("Inverted index is empty.")

        # Calcolate scores
        for word in words:
            if word in self.inverted_index:
                # for every matching word add 1 to score
                for doc_id in self.inverted_index[word]:
                    doc_scores[doc_id] += 1
            else:
                self.logger.debug(f"Word '{word}' not found in inverted index.")

        # order documents for score descending
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x, reverse=True)

        #get doc_ids
        doc_id_to_doc = {doc["doc_id"]: doc for doc in self.documents}

        results = []
        for doc_id, score in sorted_docs:
            if doc_id in doc_id_to_doc:
                results.append((doc_id_to_doc[doc_id], score))

        self.logger.info(f"Trovati {len(results)} risultati per la query: '{search}'")

        return results

    
    def save_index(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.index, f)
        # Save inverted index
        with open(self.inverted_file_path, "w") as f:
            json.dump(dict(self.inverted_index), f)

    
    def remove_folder(self, folder):
        start_len=len(self.documents)

        # Filter list for path to remove
        self.documents[:] = [doc for doc in self.documents if doc.folder != folder]
        self.index[:] = [r for r in self.index if r["folder"] != folder]
        
        if len(self.documents) < start_len:
            self.save_index();
            self.logger.info(f"Documents in folder '{folder}' removed.")
        else:
            self.logger.warning(f"No documents found in folder '{folder}'.")
            raise FolderNotFoundException(f"No documents found in index for folder '{folder}'.")

    def view_all(self):
        if not self.documents:
            print("No documents in the index.")
            return

        for doc in self.documents:
            print(f"{doc}")

    def empty_index(self):
        self.index= []
        self.inverted_index={}
        self.documents = []
        self.total_documents = 0
        self.errors = []
        self.save_index()

    def update_index(self):
        #get all folders
        folders=[]
        for document in self.documents:
            if document.folder not in folders:
                folders.append(document.folder)
        self.empty_index()
        for folder in folders:
            self.add_folder(folder, self.parsers)
        
    def print_stats(self):
        print(f"Total documents: {self.total_documents}")
        print(f"Total errors: {len(self.errors)}")
        for error in self.errors:
            print(f"Error: {error}")
        self.logger.info(f"Total documents: {self.total_documents}")
        self.logger.info(f"Total errors: {len(self.errors)}")
        for error in self.errors:
            self.logger.error(error)
             

    



        




    

  
