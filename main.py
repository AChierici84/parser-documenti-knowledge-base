import os
from logging import Logger
from pathlib import Path
import importlib
import inspect
import logging.config
import configparser
from model.index import DocumentIndex
from model.parser import DocumentParser
from utils.UIUtility import UIUtility


commandList={
  "h": "Menu",
  "1":"Index new folder",
  "2":"Search a file",
  "3":"Visualize all indexed file",
  "4":"Delete a file from index",
  "5":"Update index", 
  "6":"Save Index",
  "7":"Empty index",
  "8":"Exit",
  }


def setup_logging(config_file='config.ini'):
    # read config.ini
    config = configparser.ConfigParser()
    config.read(config_file)

    # construct log config
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
                'level': 'INFO',  #different lvl for console
            },
        },
        'root': {
            'handlers': ['file', 'console'],
            'level': config['logging']['level'],
        },
    }

    # Applica la configurazione
    logging.config.dictConfig(log_config)
    return logging.getLogger(__name__)

def get_parsers(logger: Logger,config_file='config.ini'):
    # read config.ini
    config = configparser.ConfigParser()
    config.read(config_file)

    parsers_folder= Path(config['parsers']['folder'])

    parsers=[]

    # Itera su tutti i file .py nella cartella
    for file in parsers_folder.glob("*.py"):
        if file.name == "__init__.py":
            continue  # Salta il file __init__.py

        # module name
        module_name = file.stem

        try:
            # Importa dinamicamente il modulo
            module = importlib.import_module(f"{parsers_folder}.{module_name}")

            # Itera su tutti gli oggetti nel modulo
            for name, obj in inspect.getmembers(module):
                # Controlla se l'oggetto è una classe e se eredita da DocumentParser
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, DocumentParser)
                    and obj != DocumentParser  # Esclude la classe base
                ):
                    # Istanzia la classe e aggiungi alla lista
                    instance = obj()
                    parsers.append(instance)
                    logger.debug(f"Loaded instance of {obj.__name__}")
                    

        except ImportError as e:
            logger.error(f"Errore when importing {module_name}: {e}")
        except Exception as e:
            logger.error(f"Errore when processing {module_name}: {e}")

    return parsers

def main(logger: Logger,config_file='config.ini'):
    # read config.ini
    config = configparser.ConfigParser()
    config.read(config_file)
    index=DocumentIndex(logger,config['index']['index'],config['index']['inverted_index'])
    parsers =get_parsers(logger)
    UI=UIUtility(commandList)
    cmd=UI.print_intro()
    while(cmd != "8"):
        cmd=UI.validator_command(cmd)
        if (cmd == "h"):
            UI.print_menu()
        if (cmd == "1"):
            folder=UI.ask_folder()
            index.add_folder(folder, parsers)
        if (cmd == "2"):
            search=UI.ask_keywords()
            results=index.search(search)
            for result in results:
                print(result)
        if (cmd == "3"):
            index.view_all()
        if (cmd == "4"):
            path_to_delete=UI.ask_path()
            index.delete_file(path_to_delete)
        if (cmd == "5"):
            index.update_index()
        if (cmd == "6"):
            index.save_index()
        if (cmd == "7"):
            index.empty_index()
    pass

if __name__ == "__main__":
    logger = setup_logging()
    main(logger)