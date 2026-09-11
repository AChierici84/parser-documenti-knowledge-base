class ParsingException(Exception):
    """Exception raised for errors encountered during parsing."""
    pass

class MissingParserException(Exception):
    """Exception raised when a required parser is missing."""
    pass

class UnsupportedFileFormatException(Exception):
    """Exception raised for unsupported file formats."""
    pass

class FileNotFoundException(Exception):
    """Exception raised when a file is not found."""
    pass

class IndexingException(Exception):
    """Exception raised for errors encountered during indexing."""
    pass

class DuplicateFileException(Exception):
    """Exception raised when a duplicate file is encountered."""
    pass

class InvertedIndexException(Exception):
    """Exception raised for errors encountered with the inverted index."""
    pass

class FolderNotFoundException(Exception):
    """Exception raised when a folder is not found."""
    pass