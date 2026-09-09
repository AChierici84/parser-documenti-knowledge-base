class Document:
    """
    Class representing a document
    """
    def __init__(self, folder, file_name, title, date, num_words, extract, content, format="txt"):
        """
        Init document class
        """
        self.folder = folder
        self.path = os.path.join(folder,file_name)
        self.dimension = os.path.getsize(self.path)
        self.file_name = file_name
        self.title = title
        self.date = date
        self.num_words = num_words
        self.extract = extract
        self.content = content
        self.format = format

    def to_dict(self):
        """
        Document to dictionary
        """
        return {"folder":self.folder,"file_name": self.file_name,"path":self.path,"title":self.title, "date":self.date, "num_words":self.num_words, "extract": self.extract, "content" : self.content, "format" : self.format, "dimension" : self.dimension}
    def from_dict(Document, d):
        """
        Create a Document from a dictionary
        """
        return Document(
            folder=d["folder"],
            file_name=d["file_name"],
            title=d["title"],
            date=d["date"],
            num_words=d["num_words"],
            extract=d["extract"],
            content=d["content"],
            format=d.get("format", "txt") 
        )
    def __repr__(self):
        """
        Print method for document
        """
        return f"{self.file_name}.{self.format}\n{self.dimension/1024:.2f}KB\nLast modified:{self.date}\nNum words:{self.num_words}\n-----------\n{self.title}\n-----------\n{self.extract}"