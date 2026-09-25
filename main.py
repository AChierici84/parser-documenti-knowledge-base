import os
from logging import Logger
from pathlib import Path
import importlib
import inspect
import logging.config
import configparser
from model.custom_exceptions import FolderNotFoundException, InvertedIndexException
from model.index import DocumentIndex
from model.parser import DocumentParser
from utils.UIUtility import UIUtility


commandList={
  "h": "Menu",
  "1":"Index new folder",
  "2":"Search a file",
  "3":"Visualize all indexed file",
  "4":"Delete a folder from index",
  "5":"Update index", 
  "6":"Save Index",
  "7":"Empty index",
  "8":"Exit",
  }


def setup_logging(config_file='config.ini'):
    """Setup logging configuration from config file."""



    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
    
    config = configparser.ConfigParser(interpolation=None)
    config.read(config_file)    
    
    # Create the log directory if it does not exist.
    if not os.path.exists(os.path.dirname(config['logging']['file'])):
        os.makedirs(os.path.dirname(config['logging']['file']), exist_ok=True)

    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': config['logging']['format'],
                'datefmt': config['logging']['datefmt']
            },
        },
        'handlers': {
            'file': {
                'class': 'logging.FileHandler',
                'filename': config['logging']['file'],
                'formatter': 'standard',
                'level': config['logging']['level'],
            },
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': 'INFO',  # Use a different log level for the console.
            },
        },
        'root': {
            'handlers': ['file', 'console'],
            'level': config['logging']['level'],
        },
    }

    # Apply the logging configuration.
    logging.config.dictConfig(log_config)
    return logging.getLogger(__name__)

def get_parsers(logger: Logger,config_file='config.ini'):
    """Dynamically load and return all parser instances."""
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
    
    config = configparser.ConfigParser()
    config.read(config_file)

    parsers_folder= Path(config['parsers']['folder'])
    if not parsers_folder.exists():
        raise FileNotFoundError(f"Parsers folder '{parsers_folder}' not found.")

    parsers=[]

    # Iterate over all Python files in the parser folder.
    for file in parsers_folder.glob("*.py"):
        if file.name == "__init__.py":
            continue  # Skip the package initializer.

        module_name = file.stem

        try:
            # Import the parser module dynamically.
            module = importlib.import_module(f"{config['parsers']['folder']}.{module_name}")

            # Inspect the objects defined in the module.
            for name, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, DocumentParser)
                    and obj != DocumentParser  # Exclude the base class.
                ):
                    # Instantiate the parser and add it to the list.
                    instance = obj()
                    parsers.append(instance)
                    logger.debug(f"Loaded instance of {obj.__name__}")
                    

        except ImportError as e:
            logger.error(f"Error when importing {module_name}: {e}")
        except Exception as e:
            logger.error(f"Error when processing {module_name}: {e}")

    return parsers

def main(logger: Logger,config_file='config.ini'):
    """Main entry point for the application."""
    try:
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
        
        config = configparser.ConfigParser()
        config.read(config_file)

        index=DocumentIndex(config['index']['index'],config['index']['inverted_index'],logger)
        parsers =get_parsers(logger)

        UI=UIUtility(commandList)

        cmd=UI.print_intro()
        cmd=UI.validator_command(cmd)

        while(cmd != "8"):
            if (cmd == "h"):
                UI.print_menu()
            if (cmd == "1"):
                try:
                    folder=UI.ask_folder()
                    if not os.path.exists(folder):
                        raise FolderNotFoundException(f"Folder '{folder}' not found.")
                    index.add_folder(folder, parsers)
                    index.print_stats()
                except FolderNotFoundException as e:
                    logger.error(f"Error when adding folder: {e}")
                except Exception as e:
                    logger.error(f"Error when adding folder: {e}")
            if (cmd == "2"):
                try:
                    search=UI.ask_keyword()
                    results=index.search(search)
                    for result in results:
                        print(f"{result[0]} Score: {result[1]}")
                except InvertedIndexException as e:
                    logger.error(f"Error with inverted index: {e}")
                except Exception as e:
                    logger.error(f"Error when searching: {e}")
            if (cmd == "3"):
                try:
                    index.print_stats()
                    index.view_all()
                except Exception as e:
                    logger.error(f"Error when viewing all documents: {e}")
            if (cmd == "4"):
                try:
                    folder_to_delete=UI.ask_folder()
                    index.remove_folder(folder_to_delete)
                    index.print_stats()
                except FolderNotFoundException as e:
                    logger.error(f"Error when removing folder: {e}")
                except Exception as e:
                    logger.error(f"Error when removing folder: {e}")
            if (cmd == "5"):
                try:
                    index.update_index(parsers)
                    index.print_stats()
                except Exception as e:
                    logger.error(f"Error when updating index: {e}")
            if (cmd == "6"):
                try:
                    index.save_index()
                    index.print_stats()
                except Exception as e:
                    logger.error(f"Error when saving index: {e}")
            if (cmd == "7"):
                try:
                    index.empty_index()
                    index.print_stats()
                except Exception as e:
                    logger.error(f"Errore when emptying index: {e}")
            cmd = UI.validator_command(UI.new_command())
    except configparser.Error as e:
        logger.error(f"Error reading the configuration file: {e}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        raise e
    UI.print_bye()
    pass

if __name__ == "__main__":
    """Main entry point for the application."""
    logger = setup_logging()
    main(logger)