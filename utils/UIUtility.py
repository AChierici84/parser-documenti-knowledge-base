class UIUtility:
  """
  Class for UI utility
  """
  def __init__(self,list_action):
    """
    Initialize the UIUtility with a list of actions.

    Args:
        list_action (dict): A dictionary containing action keys and their corresponding descriptions.
    """
    self.list_action = list_action
  def print_menu(self):
    """
    Print the menu in the UI.
    """
    print("Select an action:")
    for key in self.list_action.keys():
      print(f"[{key}] {self.list_action[key]}")

  def print_separator(self):
    """
    Print a separator line in the UI for better readability.
    """
    print("/***********************************************************************************/")

  def print_welcome(self):
    self.print_separator()
    """
    Print the welcome message in the UI.
    """
    print("                 Welcome                       ")
    self.print_separator()

  def print_intro(self):
    """
    Print the introduction message in the UI.
    """
    self.print_welcome()
    self.print_menu()
    self.print_separator()
    cmd=input("Insert your command: ")
    return cmd

  def new_command(self):
    """
    Print the new command prompt in the UI.
    """
    self.print_menu()
    self.print_separator()
    cmd=input("Insert your command: ")
    return cmd

  def ask_folder(self):
    """
    Ask for the path of the folder to index.
    """
    path=input("Insert path of the folder to index: ")
    return path

  def ask_keyword(self):
    """
    Ask for the string to search.
    """
    search=input("Insert string to search: ")
    return search

  def validator_command(self,cmd):
    """
    Validate the given command.
    """
    while (cmd not in self.list_action.keys()):
      print("Invalid command")
      cmd=input("Insert your command: ")

    print("Action selected:",self.list_action[cmd])
    self.print_separator()

    return cmd


  def print_bye(self):
    """
    Print a goodbye message.
    """
    print("Goodbye!!")