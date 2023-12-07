import os
import tkinter as tk
from tkinter import filedialog

import os

class FolderPathManager:
 
    
    def __init__(self):
        self.rootpath=os.path.dirname(os.path.abspath(__file__))
        #print(self.rootpath)
        self.configed_file = self.rootpath+"/config.txt"
        #print(self.configed_file)
        self.saved_folder_path=""    
        self.folderpath=""    
        self.select_folder()

    def getsavedpath(self):
        return self.saved_folder_path
        
    def save_folder_path(self):
        with open(self.configed_file, "w") as file:
            file.write(self.folderpath)

    def load_folder_path(self):
        if os.path.exists(self.configed_file):
            with open(self.configed_file, "r") as file:
                #print(file.read().strip())
                return file.read().strip()
        else:
            return None
    def uiToSelectFolder(self):
        self.folderpath = filedialog.askdirectory()
        print(self.folderpath)
        root = tk.Tk()
        root.withdraw()  # Hide the main window
            # This keeps the window open until the user closes it manually
        #root.mainloop()

    def select_folder(self):
        self.saved_folder_path = self.load_folder_path()
        if self.saved_folder_path:
            pass
            #print(f"Using saved folder path: {self.saved_folder_path}")
        else:
            #print("No saved folder path found.")
            self.uiToSelectFolder()
            self.save_folder_path()
            #print(f"Folder path saved: {self.folderpath}")

# Example of using the class
# folder_path_manager = FolderPathManager()

# # Call the method to select a folder
# folder_path_manager.select_folder()

 


# if os.name == 'posix':
#         # For Unix-like systems (including Linux)
#         normalized_path = path.replace('\\', '/')
#     elif os.name == 'nt':
#         # For Windows
#         normalized_path = path.replace('/', '\\')


























# def save_folder_path(folder_path):
#     with open("config.txt", "w") as file:
#         file.write(folder_path)

# def load_folder_path():
#     current_script_path = os.path.dirname(os.path.abspath(__file__))
#     print(current_script_path+"/config.txt")
#     if os.path.exists(current_script_path+"/config.txt"):
#         try:
#             with open(current_script_path+"/config.txt", "r") as file:
#                 return file.read().strip()
#         except:
#             pass
        

  

# def select_folder():
#     saved_folder_path = load_folder_path()
#     if saved_folder_path:
#         return save_folder_path
#         #print(f"Using saved folder path: {saved_folder_path}")
#     else:
#         #print("No saved folder path found.")
#         folder_path = uiToSelectFolder()
#         save_folder_path(folder_path)
#         #print(f"Folder path saved: {folder_path}")
    

# # Call the function to select a folder
#select_folder()
