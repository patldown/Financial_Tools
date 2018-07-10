import tkinter as tk
import os
from tkinter import *
import webbrowser
from texteditor import *
from tkinter import ttk
from stock_pull_A_0 import *
import threading

class gui:
    def __init__(self, master, title = 'FAT: Financial Analysis Tools'):
        ### sets master = object
        self.master = master
        self.height = '900'
        self.width = '1600'

        self.master.geometry(self.width + 'x' + self.height)

        ### sets title
        self.master.title(title)

        self.main_screen()
        self.view_sector_stocks()


    def clear_frame(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.main_screen()

    def view_sector_stocks(self):
        ### setup to find files in the main directory to...
        home = os.getcwd()
        self.mdict = {}
        for file in os.listdir(home):
            if 'tickers.txt' in file.lower():
                handle = open(file, 'r')
                reader = handle.readlines()
                for line in reader:
                    line = line.strip().split(':')
                    # filename : ticker : [name, E/P]
                    try:
                        self.mdict[file][line[0]] = [line[1], line[2]]
                    except:
                        self.mdict[file] = {line[0] : [line[1], line[2]]}
                handle.close()

        frame1 = Frame(self.master)
        ###########################
        slabel = Label(frame1, text = 'Sectors')
        slistbox = Listbox(frame1)
        sButton = Button(frame1, text = 'Push', command = lambda: self.update_tlistbox(slistbox.get(ACTIVE)))

        for key in self.mdict:
            slistbox.insert(END, key.split('_tickers')[0].replace('_', ' ').upper())
        ########################################

        frame2 = Frame(self.master)
        ###########################
        tlabel = Label(frame2, text = 'Tickers')
        self.tlistbox = Listbox(frame2)

        slabel.pack()
        slistbox.pack()
        sButton.pack()
        frame1.pack(side = LEFT, anchor = 'n')
        tlabel.pack()
        self.tlistbox.pack()
        frame2.pack(side = LEFT, anchor = 'n')

    def update_tlistbox(self, choice):
        choice = choice.lower().replace(' ', '_') + '_tickers.txt'
        self.tlistbox.delete('0','end')
        for key, value in self.mdict[choice].items():
            self.tlistbox.insert(END, value[0] + ' - ' + value[1])

        self.tlistbox.config(width=0)
                
    def menu_(self):
        self.menubar = tk.Menu(self.master)
        self.filemenu = tk.Menu(self.menubar, tearoff = 0)
        
        self.filemenu.add_command(label = "Close", command = '')

        self.filemenu.add_separator()
        self.filemenu.add_command(label = "Exit", command = self.master.quit)
        self.menubar.add_cascade(label = "File", menu = self.filemenu)

        self.editmenu = tk.Menu(self.menubar, tearoff = 0)

        self.editmenu.add_command(label="Launch PortEditor", command = PortEditor)
        self.editmenu.add_command(label="Clear Window", command = self.clear_frame)
        self.editmenu.add_command(label="Parameters", command = self.params_window)
        self.menubar.add_cascade(label = "Edit", menu = self.editmenu)
        

        self.macromenu = tk.Menu(self.menubar, tearoff = 0)

        self.macromenu.add_command(label="Update Sector Stocks", command = lambda: threading.Thread(target = update_sector_populations).start())
        self.macromenu.add_command(label="Download Data", command = lambda: threading.Thread(target = download_data).start())
        self.macromenu.add_command(label="View Data Stats", command = '')
        self.menubar.add_cascade(label = "Functions", menu = self.macromenu)

        self.analysismenu = tk.Menu(self.menubar, tearoff = 0)
        self.analysismenu.add_command(label="Balance Portfolio", command = reg_overlay)
        self.menubar.add_cascade(label = "Analysis", menu = self.analysismenu)
        self.master.config(menu = self.menubar)

    def main_screen(self):
        self.menu_()
        
        self.pbar = ttk.Progressbar(self.master, length = self.width)
        self.pbar.pack(side = BOTTOM)
    
    def params_window(self):
        w = Toplevel()

        CharVar1 = StringVar()
        CharVar2 = StringVar()
        CharVar3 = StringVar()
        
        tLabel = Label(w, text = 'Months to backlog:')
        tEntry = Entry(w, textvariable=CharVar1)

        wLabel = Label(w, text = 'Working capital:')
        wEntry = Entry(w, textvariable=CharVar2)

        rLabel = Label(w, text = 'Expected ROR:')
        rEntry = Entry(w, textvariable=CharVar3)

        IntVar1 = IntVar()
        IntVar2 = IntVar()
        IntVar3 = IntVar()

        
        sBox = Checkbutton(w, text ='Factor in shorting', variable = IntVar1, onvalue = 1, offvalue = 0)

        hBox = Checkbutton(w, text ='Grab high performance', variable = IntVar2, onvalue = 1, offvalue = 0)
        lBox = Checkbutton(w, text ='Grab low performance', variable = IntVar3, onvalue = 1, offvalue = 0)

        sButton = Button(w, text = 'Set Parameters', command = lambda: set_params('gui', CharVar2.get(),
                                                                               CharVar3.get(), IntVar1.get(),
                                                                               IntVar2.get(), IntVar3.get(),
                                                                               tEntry.get()))
        
        tLabel.pack()
        tEntry.pack()
        wLabel.pack()
        wEntry.pack()
        rLabel.pack()
        rEntry.pack()
        sBox.pack()
        hBox.pack()
        lBox.pack()
        sButton.pack()

        w.geometry(str(int(self.width)/7).split('.')[0] + 'x' + str(int(self.height)/4).split('.')[0])

        w.mainloop()
        

def list_from_loc(keyword, initial_dir = os.getcwd()):
    new_list = []
    for file in os.listdir(initial_dir):
        if keyword.lower() in file.lower():
            new_list.append(file)
    return new_list
                
if __name__ == "__main__":
    root = tk.Tk()
    gui(root)
    root.mainloop()
