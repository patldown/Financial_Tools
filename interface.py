import tkinter as tk
import os
from tkinter import filedialog, Toplevel, IntVar
from texteditor import *
from stock_pull_A_1 import *


class gui:
    def __init__(self, master, tag, title = 'FAT: Financial Analysis Tools'):
        ### sets master = object
        self.master = master

        ### sets title
        self.master.title(title)

        self.menu_()
        self.master.config(menu = self.menubar)

        #lbox = self.create_program_list(tag)
        #lbox.pack()

    def menu_(self):
        self.menubar = tk.Menu(self.master)
        self.filemenu = tk.Menu(self.menubar, tearoff = 0)
        
        self.filemenu.add_command(label = "Close", command = '')

        self.filemenu.add_separator()
        self.filemenu.add_command(label = "Exit", command = self.master.quit)
        self.menubar.add_cascade(label = "File", menu = self.filemenu)

        self.editmenu = tk.Menu(self.menubar, tearoff = 0)
        
        self.editmenu.add_command(label="Launch PortEditor", command = PortEditor)
        self.editmenu.add_command(label="Parameters", command = self.params_window)
        self.menubar.add_cascade(label = "Edit", menu = self.editmenu)

        self.macromenu = tk.Menu(self.menubar, tearoff = 0)
        
        self.macromenu.add_command(label="Download Data", command = '')
        self.macromenu.add_command(label="View Data Stats", command = '')
        self.macromenu.add_command(label="Combine Data", command = '')
        self.macromenu.add_command(label="Balance Portfolio", command = '')
        self.menubar.add_cascade(label = "Functions", menu = self.macromenu)

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

    def params_window(self):
        
        w = tk.Toplevel(height = 300, width = 400)
        
        tFrame = tk.Frame(w)
        tLabel = tk.Label(tFrame, text ="Months to Backlog:").pack(anchor = "w")
        tEntry = tk.Entry(tFrame)
        tEntry.pack(anchor = "e")

        CheckVar1 = IntVar()
        CheckVar2 = IntVar()
        CheckVar3 = IntVar()
        pFrame = tk.Frame(w)
        pLabel = tk.Checkbutton(pFrame, text ="High Performance", variable = CheckVar1,
                                onvalue = True, offvalue = False)
        lLabel = tk.Checkbutton(pFrame, text ="Low Performance", variable = CheckVar2,
                                onvalue = True, offvalue = False)
        pLabel.pack(anchor = "w")
        lLabel.pack(anchor = "e")

        mFrame = tk.Frame(w)
        mLabel = tk.Label(mFrame, text ="Working Capital:").pack(anchor = "w")
        mEntry = tk.Entry(mFrame)
        mEntry.pack(anchor = "e")

        rFrame = tk.Frame(w)
        rLabel = tk.Label(rFrame, text ="Required Rate of Return:").pack(anchor = "w")
        rEntry = tk.Entry(rFrame)
        rEntry.pack(anchor = "e")

        sFrame = tk.Frame(w)
        sLabel = tk.Checkbutton(sFrame, text ="Short", variable = CheckVar3,
                                onvalue = True, offvalue = False).pack(anchor = "e")

        SetButton = tk.Button(w, text = 'Set Parameters', command = lambda: set_params('Gui',
                                                                                       tEntry.get(),
                                                                                       CheckVar1.get(),
                                                                                       CheckVar2.get(),
                                                                                       mEntry.get(),
                                                                                       rEntry.get(),
                                                                                       CheckVar3.get()))
        SetButton.pack()

        tFrame.pack()
        pFrame.pack()
        mFrame.pack()
        rFrame.pack()
        sFrame.pack()

        w.mainloop()

        
                
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('800x600')
    root.resizable(width=False, height=False)
    gui(root, 'scr_')
    root.mainloop()
