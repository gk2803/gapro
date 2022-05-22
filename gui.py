from itertools import count
import tkinter as tk
from tkinter import END, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from gnt import *
import numpy as np 
from matplotlib import animation 
import time 
from matplotlib.ticker import MaxNLocator

BOUNDS = [[0, 10], [0, 20], [0, 30]]

class Sliders:
    def __init__(self, root, row, col, start, end, iter):
        return tk.Scale(
            root,
            from_=start,
            to=end,
            resolution=iter,
            orient="horizontal",
        ).grid(row=row, column=col, command=print("1"))


class MainWindow:
    def __init__(self, root, color):
        self.color = color
        self.root = root
        self.root.resizable(0, 0)
        self.root.geometry("800x700")
        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(7,weight=1)
        self.root.configure(bg=self.color)
        '''
        LABELS
        '''
        function_label = population_label = tk.Label(
            self.root,
            text="Συνάρτηση τριών μεταβλητών f(x, y, z) =",
            fg="#000000",
            font="Courier 14 bold",
            bg=self.color,
        ).grid(row=0, column=0, sticky=tk.W)

        population_label = tk.Label(
            self.root,
            text="Πληθυσμός: ",
            fg="#000000",
            font="Courier 14 bold",
            bg=self.color,
        ).grid(row=1, column=0, sticky=tk.W)
        
        generations_label = tk.Label(
            self.root, text="Γενιές:", fg="black", font="Courier 14 bold", bg=self.color
        ).grid(row=2, column=0, sticky=tk.W)
        
        pm_label = tk.Label(
            self.root,
            text="Πιθανότητα Μετάλλαξης: ",
            fg="black",
            font="Courier 14 bold",
            bg=self.color,
        ).grid(row=3, column=0, sticky=tk.W)
        
        pc_label = tk.Label(
            self.root,
            text="Πιθανότητα Διασταύρωσης: ",
            fg="black",
            font="Courier 14 bold",
            bg=self.color,
        ).grid(row=4, column=0, sticky=tk.W)
        
        cp_label = tk.Label(
            self.root,
            text="Σημεία διασταύρωσης: ",
            fg="black",
            font="Courier 14 bold",
            bg=self.color,
        ).grid(row=5, column=0, sticky=tk.W)
        
        bits_label = tk.Label(
            self.root, text="Bits: ", fg="black", font="Courier 14 bold", bg=self.color
        ).grid(row=6, column=0, sticky=tk.W)
        '''
        SLIDERS
        '''

        '''pop slider'''
        self.pop_slider = tk.Scale(
            root,
            from_=2,
            to=500,
            resolution=2,
            orient="horizontal",
        )
        self.pop_slider.grid(
            row=1,
            column=1,
        )
        
        '''generations slider'''
        self.generation_slider = tk.Scale(
            root,
            from_=1,
            to=1000,
            resolution=2,
            orient="horizontal",
        )
        
        self.generation_slider.grid(
            row=2,
            column=1,
        )

        '''pm slider'''
        self.pm_slider = tk.Scale(
            root,
            from_=0,
            to=1,
            resolution=0.01,
            orient="horizontal",
        )
        
        self.pm_slider.grid(
            row=3,
            column=1,
        )

        '''pc slider'''
        self.pc_slider = tk.Scale(
            root,
            from_=0,
            to=1,
            resolution=0.01,
            orient="horizontal",
        )
        
        self.pc_slider.grid(
            row=4,
            column=1,
        )

        

        '''bits slider'''
        self.bits_slider = tk.Scale(
            root,
            from_=2,
            to=40,
            resolution=1,
            orient="horizontal",
            command=self.update_scale
        )
        
        self.bits_slider.grid(
            row=6,
            column=1,
        )

        '''cp slider'''
        self.cp_slider = tk.Scale(
            root,
            from_=1,
            to=self.bits_slider.get(),
            resolution=1,
            orient="horizontal",
            
            
        )
        
        self.cp_slider.grid(
            row=5,
            column=1,
        )
        '''
        entries
        '''
        self.function_entry = tk.Entry(self.root, width=35, font='Courier')
        self.function_entry.insert(END, "x**2 +y**3 + z**4 + x*y*z")
        self.function_entry.grid(row=0, column=1, sticky=tk.E)
        
        #self.test_entry = tk.Entry(self.root,width=5).grid(row=2, column=2, sticky=tk.W)

        '''
        BUTTONS
        '''

        '''run button '''
        self.run_button = tk.Button(
            self.root,
            text="Εκτέλεση",
            width=10,
            font="none 14",
            command=self.run
        )
        self.run_button.grid(row=9, column=0, sticky=tk.W)

        '''exit button'''
        exit_button = tk.Button(
            self.root,
            text="Έξοδος",
            width=10,
            font="none 14",
            command=self.root.destroy,
        )
        
        exit_button.grid(row=9, column=1,sticky=tk.E)


        self.fig = plt.Figure(figsize=(7,4),dpi=100, facecolor="#efebe9")

        
        #plt.rcParams['animation.ffmpeg_path'] = 'C:\Users\geork\AppData\Local\Programs\Python\Python310\Lib\site-packages\ffmpeg'
        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=self.root,
        )
        self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=2)
        
        
        self.axes = self.fig.add_subplot(111)
        self.root.mainloop()

    def update_scale(self, new_max):
        self.cp_slider.configure(to=int(new_max)-1)
    
    def run(self):
        
        objective_function = self.function_entry.get()
        generations = self.generation_slider.get()
        print(self.pc_slider.get())
        ga = GeneticAlgorithm(self.pop_slider.get(), self.bits_slider.get(), BOUNDS, self.pm_slider.get(), self.pc_slider.get(), self.cp_slider.get(), eval('lambda x,y,z:'+objective_function))
        
        b = []
        a = []
        print(ga)
        for _ in range(generations):
            ga.run()
            b.append(ga.best().fitness)
            print(ga.best().fitness)
            print(ga)
            a.append(ga.fitness_average)
        #print(ga)
        #print(b)
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        
        self.axes.plot(b,'r', label='max fitness')
        self.axes.plot(a,'g', label='average fitness')
        self.axes.set_ylabel('fitness')
        self.axes.set_xlabel('generations')
        self.axes.yaxis.set_label_position("right")
        
        #ypomnima
        self.axes.legend(bbox_to_anchor=(0.5, 1.1), loc='upper center', ncol=2, fancybox=True, shadow=True)
        #forces integer spacing between generations 
        self.axes.xaxis.set_major_locator(MaxNLocator(integer=True))

        self.canvas.draw()





def main():
    root = tk.Tk()
    window = MainWindow(root, "#efebe9")
    


main()

