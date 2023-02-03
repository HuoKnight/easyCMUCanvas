import random, string
from tkinter import *
from tkinter import colorchooser
#from PIL import ImageTk, Image


    # TODO: 
    # - Create ID system so that each visual rectangle has an incremented ID, and rectangles that are created and then deleted
    #   during resizing do not effect the ID count. | DONE
    # - Add all shapes
    #   - Rectangle | DONE
    #   - Oval | DONE
    #   - Polygon | DONE
    #   - Circle
    #   - Star
    #   - Line
    #   - Label
    #   - Arc
    # - Include id system for all shapes
    # - Add remove tool | DONE
    # - Add custom cursors to canvas; Fleur for shape resizing, pirate for removing, spraycan for color filling | DONE
    # - Add fill button | DONE
    # - Make button images work | DONE
    # - Add ability to create shapes at specific coordinates
    # - ADD COMMENTS


"""The main class of the application, creates a tkinter instance
and sets up the layout and buttons of the canvas"""
class EasyCMUCanvas():
    def __init__(self):
        # Create Tkinter instance and set window title
        self.root = Tk()
        self.root.wm_title("Easy CMU Canvas")

        # Prevent resizing of window
        self.root.resizable(False, False)
        
        # Create Toplevel instance for tooltip
        self.tooltip = Toplevel(self.root)
        self.tooltip.withdraw()
        self.tooltip.overrideredirect(True)
        self.tooltip_label = Label(self.tooltip, text="", background="lightyellow", relief="solid", borderwidth=1)
        self.tooltip_label.pack()

         # Set default tool, shape, and color
        self.tool = 'shape'
        self.shape = 'rect'
        self.color = '#000'

        # Initialize variables for shapes
        self.rect = None
        self.oval = None
        self.polygon = []

        # Polygon specific variables, polyLine(s) are to keep track of the visual preview lines of the polygon
        self.first_point = False
        self.polyLine = None
        self.polyLines = []

        # List of shape ids
        self.shapeList = []

        # Set mouse_down to False as default
        self.mouse_down = False
        
        # Create menu for choosing polygon shapes
        self.polygonMenu = Menu(self.root, tearoff=0)
        self.polygonMenu.add_command(label='Rect', command=lambda: self.choosePolygon('rect'))
        self.polygonMenu.add_command(label='Oval', command=lambda: self.choosePolygon('oval'))
        self.polygonMenu.add_command(label='Custom', command=lambda: self.choosePolygon('polygon'))


        # Load images for some buttons
        self.fill_bucket_photo = PhotoImage(file='./img/fill_bucket.png')
        self.gradient_photo = PhotoImage(file='./img/gradient.png')

        # Create Frame instance for whole app layout
        self.layout = Frame(self.root)
        self.layout.grid(row=0, column=0)

        # Create Frame instance for button layout
        self.button_layout = Frame(self.layout)
        self.button_layout.grid(row=1, column=0)

        # Create canvas and bind events
        self.canvas = Canvas(self.layout, bg="white", height=400, width=400, cursor='fleur')
        self.canvas.bind("<Button-1>", self.mouseDown)
        self.canvas.bind("<B1-Motion>", self.mouseDrag)
        self.canvas.bind("<Motion>", self.mouseMove)
        self.canvas.grid(row=1, column=1)

        # Create shape button and bind events
        self.shapeButton = Button(self.button_layout, text='★', font=('Arial', 25), width=1, height=1, command=lambda: self.selectTool('shape'))
        self.shapeButton.bind("<Enter>", lambda event, text='Polygon': self.showTooltip(event, text))
        self.shapeButton.bind("<Leave>", self.hideTooltip)
        self.shapeButton.bind("<Button-3>", self.choosePolygonMenu)
        self.shapeButton.grid(row=0, column=0)

        # Create remove button and bind events
        self.removeButton = Button(self.button_layout, text='✕', fg='red', font=('Arial', 25), width=1, height=1, command=lambda: self.selectTool('remove'))
        self.removeButton.bind("<Enter>", lambda event, text='Delete': self.showTooltip(event, text))
        self.removeButton.bind("<Leave>", self.hideTooltip)
        self.removeButton.grid(row=1, column=0)

        # Create fill button and bind events
        self.fillButton = Button(self.button_layout, image=self.fill_bucket_photo, font=('Arial', 25), width=41, height=40, command=lambda: self.selectTool('fill'))
        self.fillButton.bind("<Enter>", lambda event, text='Fill': self.showTooltip(event, text))
        self.fillButton.bind("<Leave>", self.hideTooltip)
        self.fillButton.grid(row=2, column=0)

        # Create color button and bind events
        self.colorButton = Button(self.button_layout, image=self.gradient_photo, font=('Arial', 25), width=41, height=40, command=lambda: self.chooseColor())
        self.colorButton.bind("<Enter>", lambda event, text='Color Picker': self.showTooltip(event, text))
        self.colorButton.bind("<Leave>", self.hideTooltip)
        self.colorButton.grid(row=3, column=0)

        
        

        self.root.mainloop()


    def genID(self):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(10))

    def choosePolygonMenu(self, event):
        """Show menu dialogue to choose polygon type"""
        self.polygonMenu.post(event.x_root, event.y_root)
    
    def choosePolygon(self, shape):
        """Choose the polygon from the polygon menu"""
        self.shape = shape
        self.selectTool('shape')

    def chooseColor(self):
        self.color = colorchooser.askcolor(title='Color Picker')[1]
        print(self.color)

    def selectTool(self, tool):
        self.tool = tool
        if tool == 'remove':
            self.canvas.config(cursor='X_cursor')
        elif tool == 'shape':
            self.canvas.config(cursor='fleur')
        elif tool == 'fill':
            self.canvas.config(cursor='spraycan')

    def mouseDown(self, event):
        """Get the position of the mouse when the left mouse button is clicked.
        Additionally, run code for polygon shape, remove tool, or fill tool."""
        self.start_x = event.x
        self.start_y = event.y
        self.mouse_down = True
        if self.tool == 'shape' and self.shape == 'polygon':
            if self.polygon == []:
                self.first_point = True
            self.polygon.append(self.start_x)
            self.polygon.append(self.start_y)
            if self.polyLine:
                self.polyLines.append(self.canvas.create_line(self.canvas.coords(self.polyLine)))
            if (abs(self.polygon[-2] - self.polygon[0]) <= 2 and abs(self.polygon[-1] - self.polygon[1]) <= 2) and len(self.polygon) > 4:
                del self.polygon[-2:]
                self.polygon = self.polygon + [self.polygon[0], self.polygon[1]]
                id = self.genID()
                self.canvas.create_polygon(self.polygon, tags=id, fill=self.color)
                self.shapeList.append(id)
                self.first_point = False
                self.polygon = []
                for line in self.polyLines:
                    self.canvas.delete(line)
        elif self.tool == 'remove':
            self.canvas.delete('current')
        elif self.tool == 'fill':
            self.fillShape(self.canvas.type('current'), self.canvas.coords('current'))


    def mouseDrag(self, event):
        """Resize shapes like rect, oval etc on canvas."""
        if self.tool == 'shape':
            if self.shape == 'rect':
                if self.mouse_down:
                    self.mouse_down = False
                elif self.rect:
                    self.canvas.delete(self.rect)
                    self.shapeList.pop()
                id = self.genID()
                self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, tags=id, fill=self.color, outline='')
                self.shapeList.append(id)
            elif self.shape == 'oval':
                if self.mouse_down:
                    self.mouse_down = False
                elif self.oval:
                    self.canvas.delete(self.oval)
                    self.shapeList.pop()
                id = self.genID()
                self.oval = self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, tags=id, fill=self.color, outline='')
                self.shapeList.append(id)
    
    def mouseMove(self, event):
        """Used to display line going from last created point to mouse pointer while creating a polygon."""
        if self.first_point:
            if self.polyLine:
                self.canvas.delete(self.polyLine)
            self.polyLine = self.canvas.create_line(event.x, event.y, self.polygon[-2], self.polygon[-1])


    def showTooltip(self, event, text):
        """Show tooltip label with passed text under mouse."""
        cx, cy = event.x_root, event.y_root
        self.tooltip_label.config(text=text)
        self.tooltip.wm_geometry("+%d+%d" % (cx + 10, cy + 10))
        self.tooltip.update()
        self.tooltip.deiconify()
    
    def hideTooltip(self, event):
        """Hide tooltip."""
        self.tooltip.withdraw()
    
    def fillShape(self, shape, coords):
        """Deletes shape with tag `current`, given to shape mouse is currently over by tkinter automatically. It then creates a new identical shape with fill set to self.color."""
        self.canvas.delete('current')
        id = self.genID()
        self.shapeList.append(id)
        if shape == 'rectangle':
            if self.color == '#ffffff':
                self.canvas.create_rectangle(coords, tags=id, fill=self.color)
            else:
                self.canvas.create_rectangle(coords, tags=id, fill=self.color, width=0)
        elif shape == 'oval':
            if self.color == '#ffffff':
                self.canvas.create_oval(coords, tags=id, fill=self.color)
            else:
                self.canvas.create_oval(coords, tags=id, fill=self.color, width=0)
        elif shape == 'polygon':
            if self.color == '#ffffff':
                self.canvas.create_polygon(coords, tags=id, fill=self.color)
            else:
                self.canvas.create_polygon(coords, tags=id, fill=self.color, width=0)


app_window = EasyCMUCanvas()




