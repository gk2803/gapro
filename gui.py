
import tkinter as tk
from tkinter import END

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    
)
from gnt import *
from matplotlib.ticker import MaxNLocator
import threading 


class MainWindow:
    def __init__(self, root, color):
        self.color = color
        self.root = root
        self.root.resizable(0, 0)
        self.root.geometry("700x800")
        self.root.title("Γενετικοί")
        #self.root.columnconfigure(0,weight=1)
        #self.root.rowconfigure(8, weight=1)
        self.root.configure(bg=self.color)
        '''Frames'''
        self.top_frame = tk.Frame(self.root, width=400,height=400,pady=3,bg=self.color,relief=tk.RIDGE, bd=8)
        self.bot_frame = tk.Frame(self.root, width=400, height=400,pady=3,bg=self.color)
        self.inner_frame = tk.Frame(self.top_frame,width=200, height=200,pady=3,relief=tk.RIDGE,bd=3, bg=self.color)
        self.inner_frame.grid(row=7,columnspan=3)
        self.top_frame.grid(row=0)
        self.bot_frame.grid(row=1)
        
        '''labels'''
        variables_label = tk.Label(
            self.top_frame,
            text="   Πεδία Ορισμού    ",
            fg="#000000",
            font="Courier ",
            bg="#C6BFBB",
            relief="raised",
            borderwidth=2
        )
        
        variables_label.grid(row=0, column=0, )

        function_label = tk.Label(
            self.top_frame,
            text="      Συνάρτηση     ",
            fg="#000000",
            font="Courier",
            bg="#C6BFBB",
            relief="raised",
            borderwidth=2
        )
        
        function_label.grid(row=2, column=0, )

        population_label = tk.Label(
            self.top_frame,
            text="      Πληθυσμός     ",
            fg="#000000",
            font="Courier",
            bg="#C6BFBB",
            relief="raised",
            borderwidth=2,
        )
        population_label.grid(row=4, column=0,)

        generations_label = tk.Label(
            self.top_frame,
            text="     Γενιές     ",
            fg="black",
            font="Courier ",
            bg="#C6BFBB",
            relief="raised",
            borderwidth=2,
        )
        generations_label.grid(row=0, column=1, )

        pm_label = tk.Label(
            self.top_frame,
            text=" Π. Μετάλλαξης  ",
            fg="black",
            font="Courier",
            bg="#C6BFBB",
            relief="raised",
            borderwidth=2,
        )
        pm_label.grid(row=4, column=1,)

        pc_label = tk.Label(
            self.top_frame,
            text="Π. Διασταύρωσης ",
            fg="black",
            font="Courier ",
            bg="#C6BFBB",
            relief="raised",
            borderwidth=2,
        )
        pc_label.grid(row=2, column=1, )

        cp_label = tk.Label(
            self.top_frame,
            text="Σημεία διασταύρωσης",
            fg="black",
            font="Courier ",
            bg="#C6BFBB",
            relief="raised",
            borderwidth=2,
        )
        cp_label.grid(row=0, column=2, )

        bits_label = tk.Label(
            self.top_frame,
            text="       Bits        ",
            fg="black",
            font="Courier",
            bg="#C6BFBB",
            relief="raised",
            borderwidth=2,
        )
        bits_label.grid(row=2, column=2, )

        selection_label = tk.Label(
            self.top_frame,
            text=" Τελεστής Επιλογής  ",
            fg="black",
            font="Courier",
            bg="#C6BFBB",
            relief="raised",
            borderwidth=2,
        )
        selection_label.grid(row=4, column=2, )

        self.bounds_label = tk.Label(
            self.top_frame,
            text='',
            bg=self.color,
        )
        self.bounds_label.grid(row=1,column=0,sticky=tk.E,padx=10)

        cur_label = tk.Label(
            self.inner_frame,
            text="Τρέχων",
            fg="white",
            font="Courier",
            bg="#343434",
            relief="raised",
            borderwidth=2,
        )
        cur_label.grid(row=1,column=0)

        bestest_label = tk.Label(
            self.inner_frame,
            text=" Best ",
            fg="white",
            font="Courier",
            bg="#343434",
            relief="raised",
            borderwidth=2,
        )
        bestest_label.grid(row=2,column=0)

        gener_label = tk.Label(
            self.inner_frame,
            text="  Γενιά  ",
            fg="black",
            font="Courier",
            bg="#C0C0C0",
            relief="raised",
            borderwidth=2,
        )
        gener_label.grid(row=0,column=1)
        best_label = tk.Label(
            self.inner_frame,
            text="Καλύτερη Λύση",
            fg="black",
            font="Courier",
            bg="#C0C0C0",
            relief="raised",
            borderwidth=2,
        )
        best_label.grid(row=0,column=2,sticky=tk.E)
        average_label = tk.Label(
            self.inner_frame,
            text="Μ.Ο. Λύσεων",
            fg="black",
            font="Courier",
            bg="#C0C0C0",
            relief="raised",
            borderwidth=2,
        )
        average_label.grid(row=0,column=3,sticky=tk.W)

        
        

        self.vars_output = tk.Label(
            self.inner_frame,
            text="",
            fg="black",
            font="Courier",
            bg=self.color,            
        )
        self.vars_output.grid(row=1,column=4)

        self.gener_output = tk.Label(
            self.inner_frame,
            text="",
            fg="black",
            font="Courier",
            bg=self.color,            
        )
        self.gener_output.grid(row=1,column=1)

        self.best_output = tk.Label(
            self.inner_frame,
            text="",
            fg="black",
            font="Courier",
            bg=self.color,
            
        )
        self.best_output.grid(row=1,column=2)

        self.avg_output = tk.Label(
            self.inner_frame,
            text="",
            fg="black",
            font="Courier",
            bg=self.color,
            
        )
        self.avg_output.grid(row=1,column=3)
        
        self.best_gen_output = tk.Label(
            self.inner_frame,
            text="",
            fg="black",
            font="Courier",
            bg=self.color,
            
        )

        self.best_gen_output.grid(row=2, column=1)

        self.best_sol_output = tk.Label(
            self.inner_frame,
            text="",
            fg="black",
            font="Courier",
            bg=self.color,
            
        )
        self.best_sol_output.grid(row=2, column=2)
    #
        '''
        Sliders
        '''        
        self.pop_slider = tk.Scale(
            self.top_frame,
            from_=2,
            to=500,
            resolution=2,
            orient="horizontal",
            bg= self.color
        )
        self.pop_slider.grid(
            row=5,
            column=0,
        )

        self.generation_slider = tk.Scale(
            self.top_frame,
            from_=2,
            to=1000,
            resolution=1,
            orient="horizontal",
            bg= self.color
        )

        self.generation_slider.grid(
            row=1,
            column=1,
        )

        self.pm_slider = tk.Scale(
            self.top_frame,
            from_=0,
            to=1,
            resolution=0.01,
            orient="horizontal",
            bg= self.color,
        )

        self.pm_slider.grid(
            row=5,
            column=1,
        )

        self.pc_slider = tk.Scale(
            self.top_frame,
            from_=0,
            to=1,
            resolution=0.01,
            orient="horizontal",
            bg= self.color
        )

        self.pc_slider.grid(
            row=3,
            column=1,
        )

        self.bits_slider = tk.Scale(
            self.top_frame,
            from_=2,
            to=40,
            resolution=1,
            orient="horizontal",
            command=self.update_scale,
            bg= self.color
        )

        self.bits_slider.grid(
            row=3,
            column=2,
        )

        self.cp_slider = tk.Scale(
            self.top_frame,
            from_=1,
            to=self.bits_slider.get(),
            resolution=1,
            orient="horizontal",
            bg= self.color
        )

        self.cp_slider.grid(
            row=1,
            column=2,
        )
        '''
        dropdown
        '''
        self.var=tk.StringVar(self.top_frame)
        self.choices = {
            'x[0]':'0,10',
            'x[1]':'0,20',
            'x[2]':'0,30',
        }
        self.option = tk.OptionMenu(self.top_frame, self.var, *self.choices)
        
        self.option.grid(row=1,column=0,sticky=tk.W)
        self.var2=tk.StringVar()
        
        

        '''
        entries
        '''
        #function
        self.function_entry = tk.Entry(self.top_frame,width=26, font=("Courier", 10 ))       
        self.function_entry
        self.function_entry.grid(row=3, column=0, )        
        #bounds
        self.vars_entry = tk.Entry(self.top_frame, width=5, font='Courier',text=self.var2)
        self.vars_entry.grid(row=1, column=0,)
        self.var2.set('0,10')
        self.vars_entry.bind('<Return>',self.bind_func)
        '''
        buttons
        '''
        
        self.run_button = tk.Button(
            self.bot_frame,
            text="Εκτέλεση",
            width=10,
            font="none 14",
            command=lambda: threading.Thread(target=self.run).start(),
        )
        self.run_button.grid(row=2, column=0, sticky=tk.W)

        
        exit_button = tk.Button(
            self.bot_frame,
            text="Έξοδος",
            width=10,
            font="none 14",
            command=self.root.destroy,
        )

        exit_button.grid(row=2, column=2, sticky=tk.E)
        '''
        radiobutton 
        '''
        self.v = tk.IntVar()
        
        self.tourn_button = tk.Radiobutton(self.top_frame,bg=self.color, text="Tournament",variable=self.v,value=1)
        self.tourn_button.grid(row=5,column=2)
        self.roulette_button = tk.Radiobutton(self.top_frame, bg=self.color, text="Roulette wheel",variable=self.v,value=2)
        self.roulette_button.grid(row=6,column=2)
        

        '''canvas'''
        self.fig = plt.Figure(figsize=(7, 4), dpi=100, facecolor="#efebe9")

        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=self.bot_frame,
        )
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
        self.axes = self.fig.add_subplot(111)


        
        '''initialize values'''
        self.pop_slider.set(100)
        self.generation_slider.set(150)
        self.pm_slider.set(0.01)
        self.pc_slider.set(0.8)
        self.bits_slider.set(30)
        self.function_entry.insert(END, "x[0]**2 + x[1]**2 + x[2]**3 + x[0]*x[1]*x[2]")
        self.v.set(1)
        self.var.set('x[0]')
        '''traced var'''
        self.var.trace('w',self.bounds_f)
        '''mainloop'''
        self.root.mainloop()
    
    def bind_func(self,event):
        ''''''
        if  not self.mk_int(self.vars_entry.get()):
            self.bounds_label.config(text="❌", font='Courier',fg='red')
        else:
            self.bounds_label.config(text="✓", font='Courier',fg='green')
            self.choices[self.var.get()] = self.vars_entry.get() 
        print(self.choices)
            
        
            
            

    def bounds_f(self,*args):
        '''trace var method'''
        var2_ = self.choices[self.var.get()]
        self.var2.set(var2_)
        self.bounds_label.config(text='')

    def update_scale(self, new_max):
        '''configures slider's max val'''
        self.cp_slider.configure(to=int(new_max) - 1)

    @staticmethod
    def mk_int(s):
        '''returns true if entry is two comma separated integers (bounds) or empty string'''
        try:
            x,y = s.split(',')
            int(x)
            int(y)
            return True
        except ValueError:
            return True if s == "" else False
    
    def extract_bounds(self, dict):
        '''returns a dictionary of strings to a list of integers'''
        return [list(map(int, dict[val].split(',')))  for val in dict if dict[val]!=""]
        

    def graph(self,y1 ,y2):
        '''plots'''
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)

        self.axes.plot(y1, "g", label="average fitness")
        self.axes.plot(y2, "r", label="max fitness")
        self.axes.set_ylabel("fitness")
        self.axes.set_xlabel("generations")
        self.axes.yaxis.set_label_position("right")

        # legend options 
        self.axes.legend(
            bbox_to_anchor=(0.5, 1.1),
            loc="upper center",
            ncol=2,
            fancybox=True,
            shadow=True,
        )
        # forces integer spacing between generations
        self.axes.xaxis.set_major_locator(MaxNLocator(integer=True))
        self.canvas.draw()


    def dreamcatcher(self):
        '''catches exceptions a man can only dream of '''
        try:
            objective_function = self.function_entry.get()
            bounds = self.extract_bounds(self.choices)
            
            if not any(k in objective_function for k in list(self.choices.keys())):
                raise Exception("Καμία μεταβλητή")
            for key in self.choices.keys():
                if self.choices[key] == "" and key in objective_function:
                    raise Exception("Ασυμφωνία συνάρτησης με μεταβλητές Π.Ο.")
            #if all(value == "" for value in self.choices.values()):
            #    raise Exception("Δεν βρέθηκαν πεδία ορισμού")
            for key in self.choices.keys():
                if self.choices[key] != "" and key not in objective_function:
                    raise Exception("Ασυμφωνία συνάρτησης με μεταβλητές Π.Ο.")
            
            self.generations = self.generation_slider.get()
            
            
            ga = GeneticAlgorithm(
                self.pop_slider.get(),
                self.bits_slider.get(),
                bounds,
                self.pm_slider.get(),
                self.pc_slider.get(),
                self.cp_slider.get(),
                eval("lambda *x:" + objective_function),
            )
            return ga 
        except Exception as e:
            print(e)
            return 


    def run(self):
        '''run buttom'''
        
        ga = self.dreamcatcher()
        if ga:
            ga.run(self.v.get())
            b = [ga.best().fitness]
            a = [ga.fitness_average]
            best = b[0]
            best_index = 1
            
            for i in range(1,self.generations):
                
                
                self.gener_output.configure(text=i+1)
                ga.run(self.v.get())
                b.append(ga.best().fitness) 
                self.best_output.configure(text=float("{:.2f}".format(b[i])))
                a.append(ga.fitness_average)
                self.avg_output.configure(text=float("{:.2f}".format(a[i])))
                
                
                if best<ga.best().fitness:
                    best = ga.best().fitness
                    best_index = i+1
                    self.best_sol_output.configure(text=float("{:.2f}".format(best)))
                    self.best_gen_output.configure(text=best_index)
            self.graph(a,b)
        self.fig.clear()
        


def main():
    root = tk.Tk()
    window = MainWindow(root, "#efebe9")


main()
