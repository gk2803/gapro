import tkinter as tk
from tkinter import END
from tkinter import ttk 
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
        self.root.geometry("700x850")
        self.root.title("Γενετικοί")
        # self.root.columnconfigure(0,weight=1)
        # self.root.rowconfigure(8, weight=1)
        self.root.configure(bg=self.color)
        """Frames"""
        self.top_frame = tk.Frame(        
            self.root,                
            width=450,
            height=400,
            pady=3,
            bg=self.color,
            relief=tk.RIDGE,
            bd=8,
        )
        
        self.bot_frame = tk.Frame(                         # γραφική παράσταση και κάτω
            self.root, width=450, height=400, pady=3, bg=self.color,
        )

        self.inner_frame = tk.Frame(                       # κάτω από τα sliders
            self.top_frame,
            width=450,
            height=200,
            pady=3,
            relief=tk.RIDGE,
            bd=3,
            bg=self.color,
        )

        """labels"""
        # top_frame
        variables_label = tk.Label(                        # Πεδία Ορισμού
            self.top_frame,
            text="       Πεδία Ορισμού     ",
            fg="#000000",
            font="Courier ",
            bg="#C6BFBB",
            relief="raised",
            borderwidth=2,
        )

        function_label = tk.Label(                         # Συνάρτηση
            self.top_frame,
            text="Συνάρτηση",
            fg="#000000",
            font="Courier",
            bg="#C6BFBB",
            relief="raised",
            borderwidth=2,
        )

        population_label = tk.Label(
            self.top_frame,
            text="Πληθυσμός",                              # Πληθυσμός
            fg="#000000",
            font="Courier",
            bg="#C6BFBB",
            relief="raised",
            borderwidth=2,
        )

        generations_label = tk.Label(
            self.top_frame,                                # Γενιές
            text="Γενιές",
            fg="black",
            font="Courier ",
            bg="#C6BFBB",
            relief="raised",
            borderwidth=2,
        )

        pm_label = tk.Label(                               # Π. Μετάλλξης
            self.top_frame,
            text="Π. Μετάλλαξης",
            fg="black",
            font="Courier",
            bg="#C6BFBB",
            relief="raised",
            borderwidth=2,
        )

        pc_label = tk.Label(                               # Π. Διασταύρωσης
            self.top_frame,
            text="Π. Διασταύρωσης",
            fg="black",
            font="Courier ",
            bg="#C6BFBB",
            relief="raised",
            borderwidth=2,
        )

        cp_label = tk.Label(                               # Σημ. Διασταύρωσης
            self.top_frame,
            text="Σημ. Διασταύρωσης",
            fg="black",
            font="Courier ",
            bg="#C6BFBB",
            relief="raised",
            borderwidth=2,
        )

        bits_label = tk.Label(                             # bits
            self.top_frame,
            text="Bits",
            fg="black",
            font="Courier",
            bg="#C6BFBB",
            relief="raised",
            borderwidth=2,
        )

        selection_label = tk.Label(                        # Τελεστής Επιλογής
            self.top_frame,
            text="Τελεστής Επιλογής",
            fg="black",
            font="Courier",
            bg="#C6BFBB",
            relief="raised",
            borderwidth=2,
        )

        self.bounds_label = tk.Label(                      # label που εμφανίζει ΤΙΚ σε περίπτωση σωστής καταχώρησης πεδίου ορισμού, διαφορετικά Χ
            self.top_frame,
            text="",
            bg=self.color,
        )
        # top frame - sliders

        self.pop_slider = tk.Scale(                        # πληθυσμός
            self.top_frame,
            from_=2,
            to=500,
            resolution=2,
            orient="horizontal",
            bg=self.color,
        )

        self.generation_slider = tk.Scale(                 # Γενιές
            self.top_frame,
            from_=2,
            to=1000,
            resolution=1,
            orient="horizontal",
            bg=self.color,
        )

        self.pm_slider = tk.Scale(                         # π. διασταύρωσης
            self.top_frame,
            from_=0,
            to=1,
            resolution=0.001,
            orient="horizontal",
            bg=self.color,
        )

        self.pc_slider = tk.Scale(                         # π. μετάλλαξης
            self.top_frame,
            from_=0,
            to=1,
            resolution=0.01,
            orient="horizontal",
            bg=self.color,
        )

        self.bits_slider = tk.Scale(                       # bits
            self.top_frame,
            from_=2,
            to=40,
            resolution=1,
            orient="horizontal",
            command=self.update_scale,
            bg=self.color,
        )

        self.cp_slider = tk.Scale(                         # σημ. διαστάυρωσης
            self.top_frame,
            from_=1,
            to=self.bits_slider.get(),
            resolution=1,
            orient="horizontal",
            bg=self.color,
        )
###################################################################################################################
##################################   DROPDOWN   ###################################################################
###################################################################################################################
        # top frame - dropdowns
        self.var = tk.StringVar(self.top_frame) #bounds 
        self.var2 = tk.StringVar() #entry
        self.var_number = tk.IntVar() #number of variables
        self.choices = {
            "x": "-10,10",
            "y": "-10,10",
            
        }
        self.option = tk.OptionMenu(self.top_frame, self.var, *self.choices)
        self.var_number = tk.IntVar()
        self.var_number.set(2)
        self.option2 = tk.OptionMenu(self.top_frame, self.var_number, *[*range(1,4)],command=self.set_vars )
        # function
        self.function_entry = tk.StringVar()
        self.function = ttk.Combobox(self.top_frame, textvariable=self.function_entry,width=35,height=10)
        self.func_dict = {'Beale function':'(1.5-x+x*y)**2+(2.25-x+x*y**2)**2+(2.625-x+x*y**3)**2',
        'Booth function':'(x+2*y-7)**2 +(2*x +y -5)**2',
        'Matyas function':'0.26*(x**2+y**2)-0.48*x*y',
        'Himmelblau\'s function':'(x**2+y-11)**2 + (x+y**2-7)**2',
        'Three-hump camel function':'2*x**2-1.05*x**4+x**6/6+x*y+y**2'}
        #adding combobox drop down list 
        self.function['values']=list(self.func_dict.keys())
        self.function.bind("<<ComboboxSelected>>",self.setfunc)
        # bounds
        self.var2 = tk.StringVar()
        self.var2.set("-10,10")
        self.vars_entry = tk.Entry(
            self.top_frame, width=5, font="Courier", text=self.var2
        )
        self.vars_entry.bind("<Return>", self.bind_func)
        # radio buttons
        self.v = tk.IntVar()
        self.tourn_button = tk.Radiobutton(
            self.top_frame, bg=self.color, text="Tournament", variable=self.v, value=1
        )

        self.roulette_button = tk.Radiobutton(
            self.top_frame,
            bg=self.color,
            text="Roulette wheel",
            variable=self.v,
            value=2,
        )

###################################################################################################################        
        # inner frame

        cur_label = tk.Label(                              # Τρέχων
            self.inner_frame,
            text="Τρέχων",
            fg="white",
            font="Courier",
            bg="#343434",
            relief="raised",
            borderwidth=2,
        )

        bestest_label = tk.Label(                          # best
            self.inner_frame,
            text=" Best ",
            fg="white",
            font="Courier",
            bg="#343434",
            relief="raised",
            borderwidth=2,
        )

        gener_label = tk.Label(                            # Γενιά
            self.inner_frame,
            text="  Γενιά  ",
            fg="black",
            font="Courier",
            bg="#C0C0C0",
            relief="raised",
            borderwidth=2,
        )

        best_label = tk.Label(                             # Best fitness
            self.inner_frame,
            text="Best Fitness",
            fg="black",
            font="Courier",
            bg="#C0C0C0",
            relief="raised",
            borderwidth=2,
        )

        average_label = tk.Label(                          # Average fitness
            self.inner_frame,
            text="Average Fitness",
            fg="black",
            font="Courier",
            bg="#C0C0C0",
            relief="raised",
            borderwidth=2,
        )

        gener_label2 = tk.Label(                           # Γενιά
            self.inner_frame,
            text="  Γενιά  ",
            fg="black",
            font="Courier",
            bg="#C0C0C0",
            relief="raised",
            borderwidth=2,
        )
        x0 = tk.Label(                                     # x
            self.inner_frame,
            text="x",
            fg="black",
            font="Courier",
            bg="#C0C0C0",
            relief="raised",
            borderwidth=2,
        )
        x1 = tk.Label(                                     # y
            self.inner_frame,
            text="y",
            fg="black",
            font="Courier",
            bg="#C0C0C0",
            relief="raised",
            borderwidth=2,
        )
        x2 = tk.Label(                                     # z
            self.inner_frame, 
            text="       z        ",
            fg="black",
            font="Courier",
            bg="#C0C0C0",
            relief="raised",
            borderwidth=2,
        )

        cur_label2 = tk.Label(                             # τρέχων
            self.inner_frame,
            text="Τρέχων",
            fg="white",
            font="Courier",
            bg="#343434",
            relief="raised",
            borderwidth=2,
        )

        bestest_label2 = tk.Label(                         # Best
            self.inner_frame,
            text=" Best ",
            fg="white",
            font="Courier",
            bg="#343434",
            relief="raised",
            borderwidth=2,
        )

        

        self.gener_output = tk.Label(                      # Output Τρέχων - Γενιά 
            self.inner_frame,
            text="",
            fg="black",
            font="Courier",
            bg=self.color,
        )

        self.best_output = tk.Label(                       # Output τρέχων - Best Fitness
            self.inner_frame,
            text="",
            fg="black",
            font="Courier",
            bg=self.color,
        )

        self.avg_output = tk.Label(                        # Output τρέχων - average fitness
            self.inner_frame,
            text="",
            fg="black",
            font="Courier",
            bg=self.color,
        )

        self.best_gen_output = tk.Label(                   # output Best - Γενιά
            self.inner_frame,
            text="",
            fg="black",
            font="Courier",
            bg=self.color,
        )

        self.best_sol_output = tk.Label(                   # output Best - Best Fitness
            self.inner_frame,
            text="",
            fg="black",
            font="Courier",
            bg=self.color,
        )

        self.gener2_output = tk.Label(                     # output Τρέχων - Γενιά (δεύτερο μπλοκ)
            self.inner_frame,
            text="",
            fg="black",
            font="Courier",
            bg=self.color,
        )


        self.x0_output = tk.Label(                         # output Τρέχων - X
            self.inner_frame,
            text="",
            fg="black",
            font="Courier",
            bg=self.color,
        )
        self.x1_output = tk.Label(                         # output Τρέχων - Y
            self.inner_frame,
            text="",
            fg="black",
            font="Courier",
            bg=self.color,
        )
        self.x2_output = tk.Label(                         # output Τρέχων - z
            self.inner_frame, 
            text="",
            fg="black",
            font="Courier",
            bg=self.color,
        )

        self.x_outputs =[self.x0_output, self.x1_output, self.x2_output]

        self.best_gener2_output = tk.Label(                # output Best - Γενιά (κάτω μπλοκ)
            self.inner_frame,
            text="",
            fg="black",
            font="Courier",
            bg=self.color,
        )

        self.best_x0_output = tk.Label(                    # output Best - x
            self.inner_frame,
            text="",
            fg="black",
            font="Courier",
            bg=self.color,
        )
        self.best_x1_output = tk.Label(                    # output Best - y
            self.inner_frame,
            text="",
            fg="black",
            font="Courier",
            bg=self.color,
        )
        self.best_x2_output = tk.Label(                    # output Best - z
            self.inner_frame,
            text="",
            fg="black",
            font="Courier",
            bg=self.color,
        )

        self.bestx_output =[self.best_x0_output, self.best_x1_output, self.best_x2_output]
        # bottom frame
        self.maximize_button = tk.Button(                  # maximize button
            self.bot_frame,
            text="maximize",
            width=10,
            font="Courier 14",
            command=lambda: threading.Thread(target=self.maximize).start(),
            relief='ridge'
        )

        self.minimize_button = tk.Button(                  # minimize button
            self.bot_frame,
            text="minimize",
            width=10,
            font="Courier 14",
            command=lambda: threading.Thread(target=self.minimize).start(),
            relief='ridge'
        )

        

        exit_button = tk.Button(                           # exit butotn
            self.bot_frame,
            text="exit",
            width=10,
            font="Courier 14",
            command=self.root.destroy,
            relief='ridge'
        )
        # canvas
        self.fig = plt.Figure(figsize=(7, 4), dpi=100, facecolor="#efebe9")
        self.canvas = FigureCanvasTkAgg(                  # plot
            self.fig,
            master=self.bot_frame,
        )
        self.axes = self.fig.add_subplot(111)
############################################################################################################
######################################   GRIDS  ############################################################
############################################################################################################
        '''grids'''
        # frames
        self.inner_frame.grid(row=7, columnspan=5, sticky="nsew") 
        self.top_frame.grid(row=0)
        self.bot_frame.grid(row=1)  

        # top frame
        variables_label.grid(row=0, column=0, sticky="nsew")    # dropdown αριθμός μεταβλητών
        generations_label.grid(row=4, column=0, sticky="nsew")  # Γενιές label
        population_label.grid(row=0, column=1, sticky="nsew")   # Πληθυσμός label
        cp_label.grid(row=0, column=2, sticky="nsew")           # Σημ. Διασταύρωσης label
        function_label.grid(row=2, column=0, sticky="nsew")     # Συνάρτηση label
        pc_label.grid(row=2, column=1, sticky="nsew")           # Π. Διασταύρωσης label
        bits_label.grid(row=2, column=2, sticky="nsew")         # Bits label
        pm_label.grid(row=4, column=1, sticky="nsew")           # Π. Μετάλλαξης label
        selection_label.grid(row=4, column=2, sticky="nsew")    # Τελεστής επιλογής label
        self.bounds_label.grid(row=1, column=0,sticky=tk.E )    # ΤΙΚ / Χ label
        # inner
        cur_label.grid(row=1, column=0)                         # Τρέχων label  (πρώτο μπλοκ)
        bestest_label.grid(row=2, column=0)                     # Best label    (πρώτο μπλοκ)

        gener_label.grid(row=0, column=1)                       # Γενιά label   (πρώτο μπλοκ)
        best_label.grid(row=0, column=2)                        # Best Fitness  label
        average_label.grid(row=0, column=3, columnspan=1, sticky=tk.E) # Average fitness label

        gener_label2.grid(row=3, column=1)                      # Γενιά label   (δεύτερο μπλοκ)
        x0.grid(row=3, column=2, sticky="nsew")                 # x label       (δεύτερο μπλοκ)
        x1.grid(row=3, column=3, columnspan=2, sticky="nsew")   # y label       (δεύτερο μπλοκ)
        x2.grid(row=3, column=5,sticky='nsew',columnspan=3)     # z label       (δεύτερο μπλοκ)
 
        cur_label2.grid(row=4, column=0)                        # Τρέχων label  (δεύτερο μπλοκ)
        bestest_label2.grid(row=5, column=0)                    # Best label    (δεύτερο μπλοκ)
        # outputs
        self.gener_output.grid(row=1, column=1)                 # Τρέχων - γενιά, output           (πρώτο μπλοκ)
        self.best_output.grid(row=1, column=2)                  # Τρέχων - Best Fitness, output    (πρώτο μπλοκ)
        self.avg_output.grid(row=1, column=3)                   # Τρέχων - Average Fitness, output (πρώτο μπλοκ)
        self.best_gen_output.grid(row=2, column=1)              # Best -Γενιά, output              (πρώτο μπλοκ)
        self.best_sol_output.grid(row=2, column=2)              # Best - Best Fitness, output      (πρώτο μπλοκ)

        self.gener2_output.grid(row=4, column=1)                # Τρέχων - Γενιά, output (δεύτερο μπλοκ)
        self.x0_output.grid(row=4, column=2)                    # Τρέχων - X output (δεύτερο μπλοκ)
        self.x1_output.grid(row=4, column=3)                    # Τρέχων - Y output (δεύτερο μπλοκ)
        self.x2_output.grid(row=4, column=5)                    # Τρέχων - Z output (δεύτερο μπλοκ)

        self.best_gener2_output.grid(row=5, column=1)           # Best - Γενιά, output (δεύτερο μπλοκ)
        self.best_x0_output.grid(row=5, column=2)               # Best - X, output (δεύτερο μπλοκ)
        self.best_x1_output.grid(row=5, column=3)               # Best - Y, output (δεύτερο μπλοκ)
        self.best_x2_output.grid(row=5, column=5)               # Best - Z, output (δεύτερο μπλοκ)
        # sliders
        
        self.pop_slider.grid(row=1, column=1,sticky='nsew')     # πληθυσμός
        self.generation_slider.grid(row=5, column=0,sticky='nsew') # γενιές
        self.pm_slider.grid(row=5, column=1,sticky='nsew')      # π. μετάλλαξης
        self.pc_slider.grid(row=3, column=1,sticky='nsew')      # π. διασταύρωσης
        self.bits_slider.grid(row=3, column=2,)                 # bits
        self.cp_slider.grid(row=1, column=2,)                   # σημ. διασταύρωσης 
        # dropdown bounds
        self.option.grid(row=1, column=0,padx=(0,50) )          # Πεδία ορισμού δεύτερο dropdown-menu (x,y,z)
        self.option2.grid(row=1, column=0, sticky=tk.W)         # Πεδία ορισμού πρώτο dropdown-menu (1,2,3)
        # function entry
        self.function.grid(row=3, column=0,)                    # συνάρτηση
        #bounds entry
        self.vars_entry.grid(row=1, column=0, padx=(100,0))     # Πεδία ορισμού - Είσοδος πεδίων όρισμού
        # buttons
        self.maximize_button.grid(row=2, column=0, sticky=tk.W) # maximize
        self.minimize_button.grid(row=2, column=1)              # minimize
        exit_button.grid(row=2, column=2, sticky=tk.E)          # exit
        # radio buttons
        self.tourn_button.grid(row=5, column=2)                 # radio - tournament
        self.roulette_button.grid(row=6, column=2)              # radio - roulette wheel
        # canvas
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=3) # graph
        """initialize values"""
        self.pop_slider.set(100)
        self.generation_slider.set(150)
        self.pm_slider.set(0.01)
        self.pc_slider.set(0.8)
        self.bits_slider.set(30)
        self.v.set(1)
        self.var.set(list(self.choices.keys())[0])
        self.function.current()
        
        """traced var"""
        self.var.trace("w", self.bounds_f)
        """mainloop"""
        self.root.mainloop()
    
    def set_vars(self,event):
        
        menu = self.option.children["menu"]
        menu.delete(0,"end")        
        n = self.var_number.get()
        t=['x','y','z']
        t=[t[i] for i in range(n)]
        
        self.choices = dict(zip(t,["0,10"]*n))
        for val in self.choices.keys():
            menu.add_command(label=val, command=tk._setit(self.var,val))
        self.function_entry.set("")
        self.var.set(list(self.choices.keys())[0])
    
    def setfunc(self,event):
        self.function = event.widget.get()
        self.function_entry.set(self.func_dict[self.function])
    
        

    def bind_func(self, event):
        """"""
        if not self.mk_int(self.vars_entry.get()):
            self.bounds_label.config(text="❌", font="Courier", fg="red")

        else:
            self.bounds_label.config(text="✓", font="Courier", fg="green")
            self.choices[self.var.get()] = self.vars_entry.get()

    def bounds_f(self, *args):
        """trace var method"""
        var2_ = self.choices[self.var.get()]
        self.var2.set(var2_)
        self.bounds_label.config(text="")

    def update_scale(self, new_max):
        """configures slider's max val"""
        self.cp_slider.configure(to=int(new_max) - 1)

    @staticmethod
    def mk_int(s):
        """returns true if entry is two comma separated integers (bounds) or empty string else false"""
        try:
            x, y = s.split(",")
            int(x)
            int(y)
            return True
        except ValueError:
            return False

    def extract_bounds(self, dict) -> list:
        """takes a dictionary of strings, returns a list of integers"""
        return [list(map(int, dict[val].split(","))) for val in dict if dict[val] != ""]

    def graph(self, y1, y2):
        """plots"""
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

    def minimize(self):
        '''minimize button'''
        self.objective_function = f"-1*({self.function_entry.get()})"
        self.run()
    
    def maximize(self):
        '''maximize button'''
        self.objective_function = self.function_entry.get()
        self.run()

    def dreamcatcher(self):
        """tries to catch exceptions a man can only dream of"""
        try:
            
            self.bounds = self.extract_bounds(self.choices)
            
            if not any(k in self.objective_function for k in list(self.choices.keys())):
                raise Exception("Καμία μεταβλητή")
            for key in self.choices.keys():
                if self.choices[key] == "" and key in self.objective_function:
                    raise Exception(
                        "Ασυμφωνία μεταβλητών συνάρτησης με μεταβλητές Π.Ο."
                    )
            for key in self.choices.keys():
                if self.choices[key] != "" and key not in self.objective_function:
                    raise Exception(
                        "Ασυμφωνία μεταβλητών συνάρτησης με μεταβλητές Π.Ο."
                    )

            self.generations = self.generation_slider.get()

            ga = GeneticAlgorithm(
                self.pop_slider.get(),
                self.bits_slider.get(),
                self.bounds,
                self.pm_slider.get(),
                self.pc_slider.get(),
                self.cp_slider.get(),
                eval("lambda x=0,y=0,z=0:" + self.objective_function),
            )
            return ga
        except Exception as e:
            print(e)
            return

    def run_helper(self,n,ga,output):
        for i in range(n):
            output[i].configure(text='{:.2f}'.format(ga.best().real_genes[i]))
        

    def run(self):
        """run buttom"""

        ga = self.dreamcatcher()
        if ga:
            ga.run(self.v.get())
            b = [ga.best().fitness]
            a = [ga.fitness_average]
            best = b[0]
            best_index = 1

            for i in range(1, self.generations):

                self.run_helper(len(self.bounds),ga,self.x_outputs)
                self.gener_output.configure(text=i + 1)
                self.gener2_output.configure(text=i + 1)
                ga.run(self.v.get())
                b.append(ga.best().fitness)
                self.best_output.configure(text=float("{:.2f}".format(b[i])))
                a.append(ga.fitness_average)
                self.avg_output.configure(text=float("{:.2f}".format(a[i])))

                if best < ga.best().fitness:
                    best = ga.best().fitness
                    best_index = i + 1
                    self.best_sol_output.configure(text=float("{:.2f}".format(best)))
                    self.best_gen_output.configure(text=best_index)

                    self.best_gener2_output.configure(text=best_index)
                    self.run_helper(len(self.bounds), ga, self.bestx_output)
            self.graph(a, b)
        self.fig.clear()


def main():
    root = tk.Tk()
    window = MainWindow(root, "#efebe9")


main()
