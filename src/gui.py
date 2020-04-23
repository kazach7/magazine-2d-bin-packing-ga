## 
# gui.py
# The GUI of the application.
# Allows defining the magazine shape, defining boxes to fill the magazine (rectangles),
# setting the genetic algorithm parameters, running the algorithm.
# Displays the returned solution -- location of boxes in the magazine, fill factor.
# 04/2020, Kamil Zacharczuk
##
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from solver import *

class GUI:
    def __init__(self, solver, defaultPopulationSize, defaultIterations, defaultMutationProbability):
        self.solver = solver
        self.magazine_defined = False
        self.solved = False

        self.populationSize = defaultPopulationSize
        self.iterations = defaultIterations
        self.mutationProbability = defaultMutationProbability

        # GUI will store the x,y dimensions of user-defined boxes.
        self.boxes = []

        # Dimensions of the magazine grid in pixels 
        self.canv_width = 400
        self.canv_height = 300
        # Number of fields in the grid vertically and horizontally
        self.magazine_width = 8
        self.magazine_height = 8
        
        self.updateFieldDimensions() # Calculate one field dimensions
        
        # Main window
        self.root = tk.Tk()
        self.root.title("Magazine")
        self.root.resizable(False, False)

        # Magazine grid frame 
        self.canvasFrame = tk.Frame(self.root, bd=4)
        self.canvasFrame.pack(side=tk.LEFT)
        self.canvas = tk.Canvas(self.canvasFrame, bg="white", cursor="arrow", highlightthickness=2,
                            width=self.canv_width, height=self.canv_height)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.fieldClicked)
        self.canvas.bind("<B1-Motion>", self.b1MotionUponField)
        
        self.createMagazineGrid() # Create the fields
      
        # Several frames all gathered in the controlFrame.
        # They contain buttons, litsbox etc.
        self.controlFrame = tk.Frame(self.root)
        self.controlFrame.pack(side=tk.LEFT)

        self.listFrame = tk.Frame(self.controlFrame)
        self.listFrame.pack()
        self.listLabel = tk.Label(self.listFrame, text="Defined boxes:")
        self.listLabel.pack()

        self.boxesListFrame = tk.Frame(self.listFrame)
        self.boxesListFrame.pack()
        self.boxesList = tk.Listbox(self.boxesListFrame)
        self.boxesList.pack(side=tk.LEFT, fill="y")
        self.listScrollbar = tk.Scrollbar(self.boxesListFrame, orient="vertical")
        self.listScrollbar.config(command=self.boxesList.yview)
        self.boxesList.config(yscrollcommand=self.listScrollbar.set)
        self.listScrollbar.pack(side=tk.RIGHT, fill="y")
        
        self.listButtonsFrame = tk.Frame(self.listFrame)
        self.listButtonsFrame.pack()
        self.addBoxButton = tk.Button(self.listButtonsFrame, text="Add box", 
                                    command=lambda:self.addBoxButtonClicked())
        self.addBoxButton.pack(side=tk.LEFT)
        self.removeBoxButton = tk.Button(self.listButtonsFrame, text="Remove box",
                                         command=lambda:self.removeBoxButtonClicked())
        self.removeBoxButton.pack(side=tk.LEFT)
        
        self.magazineButtonsFrame = tk.Frame(self.controlFrame, pady=10)
        self.magazineButtonsFrame.pack()
        self.fillButton = tk.Button(self.magazineButtonsFrame, text="All fields magazine",
                                    command=lambda:self.fillButtonClicked())
        self.fillButton.pack()
        self.resolutionButton = tk.Button(self.magazineButtonsFrame, text="Change resolution",
                                    command=lambda:self.resolutionButtonClicked())
        self.resolutionButton.pack()

        self.algorithmButtonsFrame = tk.Frame(self.controlFrame, pady=10, padx=5)
        self.algorithmButtonsFrame.pack()

        self.algorithmParamsButton = tk.Button(self.algorithmButtonsFrame, text="Algorithm parameters",
                                                      command=lambda:self.algorithmParamsButtonClicked())
        self.algorithmParamsButton.pack(side=tk.LEFT)
        self.performAlgorithmButton = tk.Button(self.algorithmButtonsFrame, text="Perform algorithm",
                                            command=lambda:self.performAlgorithmButtonClicked(), padx=10)
        self.performAlgorithmButton.pack(side=tk.LEFT)

    ## Init and defining functions ##

    def displayGUI(self):
        # Display the main window
        self.root.mainloop()

    def updateFieldDimensions(self):
        self.field_width = self.canv_width / self.magazine_width
        self.field_height = self.canv_height / self.magazine_height

    def createMagazineGrid(self):
        self.fields = [[0 for x in range (self.magazine_width)] for y in range (self.magazine_height)]
        for i in range(self.magazine_height):
            for j in range(self.magazine_width):
                self.fields[j][i] = \
                    self.canvas.create_rectangle(j*self.field_width, i*self.field_height, 
                                                (j+1)*self.field_width, (i+1)*self.field_height, 
                                                fill="grey")

    ## Magazine grid event handlers ##

    def b1MotionUponField(self, event):
        self.fieldClicked(event)

    def fieldClicked(self, event):
        if (self.solved): return

        x = (int)(event.x // self.field_width)
        y = (int)(event.y // self.field_height)
        if (x > self.magazine_width-1): x = self.magazine_width-1
        if (y > self.magazine_height-1): y = self.magazine_height-1
        if (x < 0): x = 0
        if (y < 0): y = 0
        
        if (self.canvas.itemcget(self.fields[x][y], "fill") == "grey"):
            self.makeFieldEmptyIfAllowed(x,y)

    ## Buttons event handlers ##

    def addBoxButtonClicked(self):
        x = simpledialog.askinteger("Add box", "Specify box width")
        if (not x): return
        y = simpledialog.askinteger("Add box", "Specify box height")
        if (not y): return

        self.boxes.append((x,y))
        str_box = str(x) + " x " + str(y)
        self.boxesList.insert(tk.END, str_box)

    def removeBoxButtonClicked(self):
        index = list(map(int, self.boxesList.curselection()))
        if (index):
            self.boxes.pop(index[0])
            self.boxesList.delete(tk.ACTIVE)

    def fillButtonClicked(self):
        fill_color = "grey"
        if (self.fillButton.cget('text') == "All fields magazine"):
            fill_color = "white"
            self.fillButton.config(text="All fields wall")
        else:
            self.fillButton.config(text="All fields magazine")
            self.magazine_defined = False

        for x in range(self.magazine_width):
            for y in range(self.magazine_height):
                self.canvas.itemconfig(self.fields[x][y], fill=fill_color)

    def resolutionButtonClicked(self):
        if (self.magazine_width == 32): self.magazine_width = 2
        else: self.magazine_width *= 2
        if (self.magazine_height == 32): self.magazine_height = 2
        else: self.magazine_height *= 2
        
        self.updateFieldDimensions()

        del self.fields
        self.magazine_defined = False
        self.createMagazineGrid()

        self.fillButton.config(text="All fields wall")
        self.fillButtonClicked()

        self.solved = False
        self.performAlgorithmButton.config(text="Perform algorithm")

    def algorithmParamsButtonClicked(self):
        # Create a pop-up window
        window = tk.Toplevel(width=250)
        window.title("Enter parameters")
        window.geometry("%dx%d+%d+%d" % (275, 100, self.root.winfo_x() + 100, self.root.winfo_y() + 100))
        window.grab_set()

        entryFrame = tk.Frame(window)
        entryFrame.pack()
        
        # Fill the entries with stored parameters' values
        populationSizeLabel = tk.Label(entryFrame, text="Population size: ")
        populationSizeEntry = tk.Entry(entryFrame)
        populationSizeEntry.insert(0, self.populationSize)
        iterationsLabel = tk.Label(entryFrame, text="Algorithm iterations: ")
        iterationsEntry = tk.Entry(entryFrame)
        iterationsEntry.insert(0, self.iterations)
        probabilityLabel = tk.Label(entryFrame, text="Mutation probability: ")
        probabilityEntry = tk.Entry(entryFrame)
        probabilityEntry.insert(0, "{:.4f}".format(self.mutationProbability))
        populationSizeLabel.grid(row=0, column=0)
        populationSizeEntry.grid(row=0, column=1)
        iterationsLabel.grid(row=1, column=0)
        iterationsEntry.grid(row=1, column=1)
        probabilityLabel.grid(row=2, column=0)
        probabilityEntry.grid(row=2, column=1)

        buttonFrame = tk.Frame(window)
        buttonFrame.pack()
        okButton = tk.Button(buttonFrame, text="OK", 
                             command=lambda: self.algorithmParamsOKButtonClicked(window, populationSizeEntry, 
                                                                                 iterationsEntry, probabilityEntry))
        okButton.pack()

    # Button in the pop-up window
    def algorithmParamsOKButtonClicked(self, window, populationSizeEntry, iterationsEntry, probabilityEntry):
        self.populationSize = (int)(populationSizeEntry.get())
        self.iterations = (int)(iterationsEntry.get())
        self.mutationProbability = (float)(probabilityEntry.get())
        window.destroy()

    def performAlgorithmButtonClicked(self):
        if (not self.solved): # A solution is not displayed on the grid
            magazine_shape = self.getMagazineShape()

            winner = self.solver.solve(magazine_shape, self.boxes, self.populationSize, self.iterations,
                                       self.mutationProbability)
   
            for x in range(self.magazine_width):
                for y in range(self.magazine_height):
                    if (winner[0][x][y] == "box"):
                        self.canvas.itemconfig(self.fields[x][y], fill="orange")

            msg = "Optimum filling rate: " + "{:.4f}".format(winner[1])
            messagebox.showinfo("Winner is...", msg)

            # Only block reshaping the magazine until the "Clear magazine" button is clicked 
            # if there is any box displayed in the magazine (fill factor > 0).
            if (winner[1] > 0):
                self.solved = True
                # To avoid automatical window resizing
                self.algorithmButtonsFrame.pack_propagate(False)
                
                self.performAlgorithmButton.config(text="Clear magazine")

        else: # A solution is displayed on the grid - this button is now to clear it.
            self.solved = False
            self.performAlgorithmButton.config(text="Perform algorithm")

            for x in range(self.magazine_width):
                for y in range(self.magazine_height):
                    if (self.canvas.itemcget(self.fields[x][y], "fill") == "orange"):
                        self.canvas.itemconfig(self.fields[x][y], fill="white")

    ## Other functions 

    # Get the map of empty & wall fields in the magazine for the use of the solver.
    def getMagazineShape(self):
        shape = [[0 for x in range(self.magazine_width)] for y in range (self.magazine_height)]

        for x in range(self.magazine_width):
            for y in range(self.magazine_height):
                if (self.canvas.itemcget(self.fields[x][y], "fill") == "white"):
                    shape[x][y] = "empty"
                else: shape[x][y] = "wall"

        return shape

    # Turn a wall field into an empty field after making sure that you can.
    def makeFieldEmptyIfAllowed(self, x, y):
        # Empty field can only be placed next to another empty field
        # unless there is none (magazine_defined == False).
        if (
            (not self.magazine_defined)
            or (x != 0 and self.canvas.itemcget(self.fields[x-1][y], "fill") == "white")
            or (y != 0 and self.canvas.itemcget(self.fields[x][y-1], "fill") == "white")
            or (x != self.magazine_width-1 and self.canvas.itemcget(self.fields[x+1][y], "fill") == "white")
            or (y != self.magazine_height-1 and self.canvas.itemcget(self.fields[x][y+1], "fill") == "white")
        ):
            self.magazine_defined = True
            self.canvas.itemconfig(self.fields[x][y], fill="white")

    def makeFieldWall(self, x, y):
        pass # unused