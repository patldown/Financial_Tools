import tkinter as tk
import os
from tkinter import *
import webbrowser
from texteditor import *
from tkinter import ttk
from stock_pull_A_0 import *
import threading
import operator
#import matplotlib.pyplot as plt
#from PIL import Image

import matplotlib as mpl
import numpy as np
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg

class gui:
    def __init__(self, master, title = 'FAT: Financial Analysis Tools'):
        ### sets master = object
        self.master = master

        ###theme setup
        self.widget_color = '#196DFF'
        self.wtext_color = '#FFFFFF'
        self.widget_color2 = '#FFAD00'
        self.wtext_color2 = '#000000'
        
        ###widget_setup
        self.mcolor_theme = '#639CFF'
        self.height = '900'
        self.width = '1600'
        self.master.geometry(self.width + 'x' + self.height)
        self.master.configure(background=self.mcolor_theme)

        ### sets title
        self.master.title(title)

        self.main_screen()
        
    def clear_frame(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.main_screen()

    def stocks_by_sector(self):

        self.clear_frame()
        
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
                        self.mdict[file][line[0]] = [line[1], float(line[2]), float(line[3]), float(line[4])]
                    except:
                        self.mdict[file] = {line[0] : [line[1], float(line[2]), 0, 0]}
                handle.close()

        ### Drawing up listboxes to work with port editor
        frame1 = Frame(self.master, background = self.widget_color)
        ###########################
        slabel = Label(frame1, text = 'Sectors', background = self.widget_color, fg = self.wtext_color)
        slistbox = Listbox(frame1, height = 10)
        sButton = Button(frame1, text = 'Push', command = lambda: self.update_tlistbox(slistbox.get(ACTIVE)))

        for key in self.mdict:
            slistbox.insert(END, key.split('_tickers')[0].replace('_', ' ').upper())
        ########################################

        frame2 = Frame(self.master, background = self.widget_color)
        ###########################
        tlabel = Label(frame2, text = 'Tickers by E/P', background = self.widget_color, fg = self.wtext_color)
        self.tlistbox = Listbox(frame2, height = 35, selectmode=EXTENDED)
        

        Filter_Frame = Frame(frame2)
        F1Button = Button(Filter_Frame, text = 'fEPS', command = lambda: self.update_tlistbox(slistbox.get(ACTIVE), Filter = 'EPS'))
        F2Button = Button(Filter_Frame, text = 'fEV/Revenue', command = lambda: self.update_tlistbox(slistbox.get(ACTIVE), Filter = 'EV_REV'))
        F3Button = Button(Filter_Frame, text = 'fEV/EBITDA', command = lambda: self.update_tlistbox(slistbox.get(ACTIVE), Filter = 'EV_EBITDA'))
        tButton = Button(frame2, text = 'Add', command = lambda: self.update_mlistbox(self.tlistbox.curselection()))
        jButton = Button(frame2, text = 'Difference', command = lambda: self.difference(self.tlistbox.curselection(), self.tlistbox, self.mlistbox))

        frame3 = Frame(self.master, background = self.widget_color)
        ###########################
        mlabel = Label(frame3, text = 'Your Picks', background = self.widget_color, fg = self.wtext_color)
        self.mlistbox = Listbox(frame3, height = 35, selectmode=EXTENDED)
        removeButton = Button(frame3, text = 'Remove', command = lambda: self.ritem_listbox(self.mlistbox, self.mlistbox.curselection()))
        saveButton = Button(frame3, text = 'Export', command = lambda: self.save_new_port(self.mlistbox))

        ### Packing occurs below this
        slabel.pack()
        slistbox.pack()
        sButton.pack()
        frame1.pack(side = LEFT, anchor = 'n')
        tlabel.pack()
        self.tlistbox.pack()
        
        F1Button.pack(side = LEFT)
        F2Button.pack(side = LEFT)
        F3Button.pack(side = LEFT)
        
        Filter_Frame.pack()

        tButton.pack()
        jButton.pack()
        
        frame2.pack(side = LEFT, anchor = 'n')
        mlabel.pack()
        self.mlistbox.pack()
        removeButton.pack()
        saveButton.pack()
        frame3.pack(side = LEFT, anchor = 'n')

    def plot_view(self):
        '''
           Deals with plot window setup
        '''
        ### clear window
        self.clear_frame()

        ### setup frame1 ##########
        frame1 = Frame(self.master)
        flabel = Label(frame1, text = 'Currently Downloaded')
        self.flistbox = Listbox(frame1, height = 35)
        fButton = Button(frame1, text = 'Graph', command = lambda: self.plot_file(self.flistbox.get(ACTIVE)))#threading.Thread(target = self.plot_file, args =[self.flistbox.get(ACTIVE)]).start())#
        dButton = Button(frame1, text = 'Remove', command = lambda: self.ritem_listbox2(self.plistbox, self.flistbox.get(ACTIVE)))
        
        for file in os.listdir(os.getcwd()):
            if '.csv' in file.lower() and 'combination' not in file.lower():
                self.flistbox.insert(END, file)

        ### setup frame2 ##########
        frame2 = Frame(self.master)
        plabel = Label(frame2, text = 'Current Portfolio')
        self.plistbox = Listbox(frame2, height = 35)

        handle = open('curr_port.info', 'r')
        reader = handle.readlines()
        handle.close()

        handle = open(reader[0].strip(), 'r')
        reader = handle.readlines()
        handle.close()
        for line in reader:
            self.plistbox.insert(END, line.strip())

        self.plistbox.config(width=0)
        pbutton = Button(frame2, text = 'Save', command = lambda: self.save_new_port(self.plistbox))

        ### Pack the goods
        flabel.pack()
        self.flistbox.pack()
        fButton.pack()
        dButton.pack()
        frame1.pack(side = LEFT, anchor = 'n')

        plabel.pack()
        self.plistbox.pack()
        pbutton.pack()
        frame2.pack(side = LEFT, anchor = 'n')

    def plot_file(self, file):
        '''
           Plots ticker data to tkinter window
        '''

        ### clear any plots/refresh window
        self.plot_view()

        ### set style
        mpl.pyplot.style.use('ggplot')

        ### creates canvas to load plots onto
        canvas = tk.Canvas(self.master, width=self.width, height=self.height, background = self.mcolor_theme)
        canvas.pack()

        ### Reads in infromation from ticker file
        X = []
        Y = []
        I = []
        J = []
        K = []

        x = 0
        handle = open(file, 'r', newline = '')
        reader = handle.readlines()
        for line in reader:
            line = line.strip().split(',')
            X.append(x)
            Y.append(float(line[1]))
            I.append(float(line[2]))
            J.append(float(line[3]))
            K.append(float(line[4]))
            x += 1

        ### determines view range for plot
        min_rng = min(Y) - (min(Y) * .1)
        max_rng = max(Y) + (max(Y) * .1)

        ### creates population plot here
        fig = mpl.figure.Figure(figsize=(7, 8))
        ax = fig.add_subplot(211)
        ax.plot(X, Y)
        ax.plot(X,I, '--')
        ax.plot(X,J, '--')
        ax.plot(X,K, '--')
        ax.axis([0, len(X), min_rng, max_rng])
        ax.set_title(file.split('.')[0])
        ax.legend(["Adj Price", "100 MA", "Upper", "Lower"])

        min_rng = min(Y[-60:]) - (min(Y[-60:]) * .1)
        max_rng = max(Y[-60:]) + (max(Y[-60:]) * .1)

        ### creates sample 60 days plot here
        ax1 = fig.add_subplot(212)
        ax1.plot(Y[-60:])
        ax1.plot(I[-60:], '--')
        ax1.plot(J[-60:], '--')
        ax1.plot(K[-60:], '--')
        ax1.axis([0, 60, min_rng, max_rng])
        ax1.set_title(file.split('.')[0] + ': 60 Days Zoomed')
        ax1.legend(["Adj Price", "100 MA", "Upper", "Lower"])
        
        fig_x, fig_y = 10, 10
        fig_photo = draw_figure(canvas, fig, loc=(fig_x, fig_y))

        ### returns to mainloop
        tk.mainloop()

    def save_new_port(self, listbox):
        x = filedialog.asksaveasfilename(initialdir = os.getcwd(),filetypes=(('Text files', '*.txt'), ('All files', '*.*')))
        handle = open(x, 'w')
        handle.close()
        for i, listbox_entry in enumerate(listbox.get(0, END)):
            handle = open(x, 'a')
            handle.write(listbox_entry + '\n')
            handle.close()

    def ritem_listbox2(self, listbox, choices):
        '''
           listbox = listbox to remove from
           choices = choices to remove from beforementioned listbox
           Deals with removing stocks from current portfolio
        '''
        if isinstance(choices, (list,)) == False:
            choices = [choices]
        for i, listbox_entry in enumerate(listbox.get(0, END)):
            for choice in choices:
                if choice.split('.')[0] in listbox_entry:
                    listbox.delete(i)
        

    def ritem_listbox(self, listbox, choices):
        choices = list(choices)
        choices.sort(reverse = True)
        print(choices)
        for item in choices:
            listbox.delete(item)
        self.mlistbox.config(width=0)

    def update_mlistbox(self, choices):
        '''
           Function to move the selection in tlistbox (ticker listbox)
           to mlistbox (portfolio listbox)
        '''
        for item in choices:
            #print(self.tlistbox.get(item), self.mlistbox.get(0, "end"))
            if self.tlistbox.get(item) not in self.mlistbox.get(0, "end"):
                self.mlistbox.insert(END, self.tlistbox.get(item))
        self.mlistbox.config(width=0)

        #self.tlistbox.delete(ANCHOR)
        
    
    def update_tlistbox(self, choice, Filter = 'EPS'):
        '''
           handles updating sector specific stocks for the gui
           renames the sector to the associated file to draw information
        '''
        
        choice = choice.lower().replace(' ', '_') + '_tickers.txt'

        # deletes info in listbox
        self.tlistbox.delete('0','end')

        #determines max lenth of the population
        max_len = 0
        for key, value in self.mdict[choice].items():
            if len(value[0]) > max_len:
                max_len = len(value[0])

        #add area to sort tickers

        if Filter == 'EPS':
            temp_dict = sorted(self.mdict[choice].items(), key=lambda kv: kv[1][1], reverse = True)
        elif Filter == 'EV_REV':
            temp_dict = sorted(self.mdict[choice].items(), key=lambda kv: kv[1][2], reverse = True)
        elif Filter == 'EV_EBITDA':
            temp_dict = sorted(self.mdict[choice].items(), key=lambda kv: kv[1][3], reverse = True)
        
        #print(temp_dict)
        
        #adds all the items to the listbox
        for key, value in temp_dict:
            s = max_len - len(value[0])
            s = s * ' '
            
            if Filter == 'EPS':
                self.tlistbox.insert(END, key + ':' + value[0] + ' (P/E ratio: ' + str(value[1]) + ')')
            elif Filter == 'EV_REV':
                self.tlistbox.insert(END, key + ':' + value[0] + ' (EV/Revenue: ' + str(value[2]) + ')')
            elif Filter == 'EV_EBITDA':
                self.tlistbox.insert(END, key + ':' + value[0] + ' (EV/EBITDA: ' + str(value[3]) + ')')

        #reconfigs window
        self.tlistbox.config(width=0)

    def difference(self, selection1, listbox1, listbox2):
        potentials = []
        for select in selection1:
            #print(self.tlistbox.get(item), self.mlistbox.get(0, "end"))
            potentials = [listbox1.get(select).split(':')[0]]

        for i, listbox_entry in enumerate(listbox2.get(0, END)):
            if listbox_entry.split(':')[0] not in potentials:
                listbox2.delete(i)
                
        self.mlistbox.config(width=0)
        
                
    def menu_(self):
        # menu
        self.menubar = tk.Menu(self.master)

        ### file dropdown
        self.filemenu = tk.Menu(self.menubar, tearoff = 0)

        self.filemenu.add_separator()
        self.filemenu.add_command(label = "Exit", command = lambda: self.master.destroy())
        self.menubar.add_cascade(label = "File", menu = self.filemenu)

        ### edit dropdown
        self.editmenu = tk.Menu(self.menubar, tearoff = 0)

        self.editmenu.add_command(label="Launch PortEditor", command = PortEditor)
        self.editmenu.add_command(label="Clear Window", command = self.clear_frame)
        self.editmenu.add_command(label="Parameters", command = self.params_window)
        self.menubar.add_cascade(label = "Edit", menu = self.editmenu)

        ### Views Dropdown
        self.viewsmenu = tk.Menu(self.menubar, tearoff = 0)
        self.viewsmenu.add_command(label="Sector/Stock (P/E Ratio) View", command = self.stocks_by_sector)
        self.viewsmenu.add_separator()
        self.viewsmenu.add_command(label="Run Charts View", command = self.plot_view)
        self.viewsmenu.add_separator()
        self.viewsmenu.add_command(label="Portfolio Results", command = self.portfolio_view)
        self.menubar.add_cascade(label = "Views", menu = self.viewsmenu)
        
        
        ### function dropdown
        self.macromenu = tk.Menu(self.menubar, tearoff = 0)

        self.macromenu.add_command(label="Update Sector Stocks", command = lambda: threading.Thread(target = update_sector_populations).start())
        self.macromenu.add_command(label="Download Data", command = lambda: threading.Thread(target = download_data).start())
        self.macromenu.add_command(label="View Data Stats", command = '')
        self.menubar.add_cascade(label = "Functions", menu = self.macromenu)

        ### analysis dropdown
        self.analysismenu = tk.Menu(self.menubar, tearoff = 0)
        self.analysismenu.add_command(label="Balance Portfolio", command = reg_overlay)
        self.menubar.add_cascade(label = "Analysis", menu = self.analysismenu)
        self.master.config(menu = self.menubar)

    def main_screen(self):
        self.menu_()
        
        self.pbar = ttk.Progressbar(self.master, length = self.width)
        self.pbar.pack(side = BOTTOM)

    def portfolio_view(self):
        ### splice portfolio data from excel

        self.clear_frame()
        home = os.getcwd()
        port_fldr = os.path.join(home, 'Results')

        
        for file in os.listdir(port_fldr):
            if 'nfile' not in locals():
                nfile = file
            elif os.stat(os.path.join(port_fldr, file)).st_mtime > os.stat(os.path.join(port_fldr, nfile)).st_mtime:
                nfile = file

        print(nfile)

        handle = open(os.path.join(port_fldr, nfile), 'r', newline = '')
        reader = handle.readlines()
        for line in reader:
            nline = line.strip().split(',')
            if 'Weights' in nline[0]:
                loc = reader.index(line) - 1
                break

        header = reader[loc].split(',')[1:]
        values = reader[loc+4].split(',')[1:]
        prices = reader[loc+5].split(',')[1:]
        ret = float(reader[loc+7].split(',')[1]) * 365 + 1


        data = {}
        x = 0
        while x < len(header):
            data[header[x]] = [values[x], prices[x]]
    
    def params_window(self):
        '''
           Set parameters for general use
        '''
        
        w = Toplevel()
        w.configure(background = self.widget_color2)

        CharVar1 = StringVar()
        CharVar2 = StringVar()
        CharVar3 = StringVar()
        
        tLabel = Label(w, text = 'Months to backlog:', bg = self.widget_color2)
        tEntry = Entry(w, textvariable=CharVar1)

        wLabel = Label(w, text = 'Working capital:', bg = self.widget_color2)
        wEntry = Entry(w, textvariable=CharVar2)

        rLabel = Label(w, text = 'Expected ROR:', bg = self.widget_color2)
        rEntry = Entry(w, textvariable=CharVar3)

        IntVar1 = IntVar()
        IntVar2 = IntVar()
        IntVar3 = IntVar()

        
        sBox = Checkbutton(w, text ='Factor in shorting', variable = IntVar1, onvalue = 1, offvalue = 0, bg = self.widget_color2)

        hBox = Checkbutton(w, text ='Grab high performance', variable = IntVar2, onvalue = 1, offvalue = 0, bg = self.widget_color2)
        lBox = Checkbutton(w, text ='Grab low performance', variable = IntVar3, onvalue = 1, offvalue = 0, bg = self.widget_color2)

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

def draw_figure(canvas, figure, loc=(0, 0)):
    """ Draw a matplotlib figure onto a Tk canvas

    loc: location of top-left corner of figure on canvas in pixels.
    Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
    """
    figure_canvas_agg = FigureCanvasAgg(figure)
    figure_canvas_agg.draw()
    figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
    figure_w, figure_h = int(figure_w), int(figure_h)
    photo = tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)

    # Position: convert from top-left anchor to center anchor
    canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)

    # Unfortunately, there's no accessor for the pointer to the native renderer
    tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

    # Return a handle which contains a reference to the photo object
    # which must be kept live or else the picture disappears
    return photo

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
