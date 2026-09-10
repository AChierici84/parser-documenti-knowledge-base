from model.index import DocumentIndex
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

def main():
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
    main()