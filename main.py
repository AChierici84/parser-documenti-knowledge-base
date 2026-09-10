import logging
import logging.config
import configparser
from model.index import DocumentIndex
from utils.UIUtility import UIUtility

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
                'level': 'ERROR',  #different lvl for console
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

def main(logger):
    index=DocumentIndex()
    UI=UIUtility(commandList)
    cmd=UI.print_intro()
    while(cmd != "8"):
        cmd=UI.validator_command(cmd)
        if (cmd == "h"):
            UI.print_menu()
        if (cmd == "1"):
            index_new_folder()
        if (cmd == "2"):
            search_file()
        if (cmd == "3"):
            view_index()
        if (cmd == "4"):
            delete_file()
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