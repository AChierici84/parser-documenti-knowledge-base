class UIUtility:
  """
  Class for UI utility
  """
  def __init__(self,list_action):
    """
    init UIUtility
    """
    self.list_action = list_action
  def print_menu(self):
    """
    Print menu
    """
    print("Seleziona l'operazione desiderata:")
    for key in self.list_action.keys():
      print(f"[{key}] {self.list_action[key]}")

  def print_separator(self):
   print("/***********************************************************************************/")

  def print_welcome(self):
    self.separatore()
    print("                 Welcome                       ")
    self.separatore()

  def print_intro(self):
    """
    Print intro
    """
    self.print_welcome()
    self.print_menu()
    self.print_separator()
    cmd=input("Insert your command: ")
    return cmd

  def new_command(self):
    """
    Print new commmand prompt
    """
    self.print_menu()
    self.print_separator()
    cmd=input("Insert your command: ")
    return cmd

  def ask_folder(self):
    """
    ask path of the folder to index
    """
    path=input("Insert path of the folder to index: ")
    return path

  def ask_keyword(self):
    """
    ask string to search
    """
    search=input("Insert string to search: ")
    return search

  def validator_command(self,cmd):
    """
    Method validating command
    """
    while (cmd not in self.list_action.keys()):
      print("Command non valid")
      cmd=input("Insert your command: ")

    print("Action selected:",self.list_action[cmd])
    self.print_separator()

    return cmd


  def print_bye(self):
    """
    Method that say bye
    """
    print("Goodbye!!")