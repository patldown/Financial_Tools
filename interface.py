import tkinter as tk
import os
from tkinter import filedialog

def create_new_file(ext = '.txt'):
    x = filedialog.asksaveasfilename(initialdir = os.getcwd,
                                     filetypes=[('text', '.txt'), ('comma separated values', '.csv'),
                                                ('all files', '.*')],
                                     defaultextension = ext)
    handle = open(x, 'w')
    handle.close()
    return x

class gui:
    def __init__(self, master, tag, title = 'Main_Skin_Interface'):
        ### sets master = object
        self.master = master

        ### sets title
        self.master.title(title)

        self.menu_()
        self.master.config(menu = self.menubar)

        lbox = self.create_program_list(tag)
        lbox.pack()

    def menu_(self):
        self.menubar = tk.Menu(self.master)
        self.filemenu = tk.Menu(self.menubar, tearoff = 0)
        
        self.filemenu.add_command(label="New", command = create_new_file)
        self.filemenu.add_command(label = "Open", command = '')
        self.filemenu.add_command(label = "Save", command = '')
        self.filemenu.add_command(label = "Save as...", command = '')
        self.filemenu.add_command(label = "Close", command = '')

        self.filemenu.add_separator()
        self.filemenu.add_command(label = "Exit", command = self.master.quit)
        self.menubar.add_cascade(label = "File", menu = self.filemenu)

        self.editmenu = tk.Menu(self.menubar, tearoff = 0)
        
        self.editmenu.add_command(label="New", command = '')
        self.editmenu.add_command(label = "Open", command = '')
        self.editmenu.add_command(label = "Save", command = '')
        self.editmenu.add_command(label = "Save as...", command = '')
        self.editmenu.add_command(label = "Close", command = '')

        self.editmenu.add_separator()
        self.editmenu.add_command(label = "Exit", command = self.master.quit)
        self.menubar.add_cascade(label = "Edit", menu = self.filemenu)

    def list_programs(self, tag):
        self.scripts = []
        for file in os.listdir(os.getcwd()):
            #print(file)
            if tag in file.lower():
                #print(True)
                self.scripts.append(file)

    def create_program_list(self, tag):
        self.list_programs(tag)
        lbox = tk.Listbox(self.master)
        x = 1
        for item in self.scripts:
            command_name = item.split('.')[0].upper().split('_')[1] + " " + item.split('.')[0].upper().split('_')[2] + " ANALYSIS"
            lbox.insert(x, command_name)
            x+=1
        return lbox
                
if __name__ == "__main__":
    root = tk.Tk()
    gui(root, 'scr_')
    root.mainloop()
