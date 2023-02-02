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
    # - Add custom cursors to canvas; Fleur for shape resizing, pirate for removing, spraycan for color filling | Done
    # - Add fill button | DONE
    # - Make button images work | DONE
    # - Add ability to create shapes at specific coordinates

class EasyCMUCanvas():
    def __init__(self):
        self.root = Tk()
        self.root.wm_title("Easy CMU Canvas")
        self.root.resizable(False, False)
        self.tooltip = Toplevel(self.root)
        self.tooltip.withdraw()
        self.tooltip.overrideredirect(True)
        self.tooltip_label = Label(self.tooltip, text="", background="lightyellow", relief="solid", borderwidth=1)
        self.tooltip_label.pack()

        self.tool = 'shape'
        self.shape = 'rect'
        self.color = '#000000'

        self.rect = None
        self.oval = None
        self.polygon = []
        self.first_point = False
        self.polyLine = None
        self.polyLines = []

        self.current_tag = -1
        
        

        self.polygonMenu = Menu(self.root, tearoff=0)
        self.polygonMenu.add_command(label='Rect', command=lambda: self.choosePolygon('rect'))
        self.polygonMenu.add_command(label='Oval', command=lambda: self.choosePolygon('oval'))
        self.polygonMenu.add_command(label='Polygon', command=lambda: self.choosePolygon('polygon'))

        self.fill_bucket_photo = PhotoImage(file='./img/fill_bucket.png')
        self.gradient_photo = PhotoImage(file='./img/gradient.png')

        self.layout = Frame(self.root)
        self.layout.grid(row=0, column=0)
        self.button_layout = Frame(self.layout)
        self.button_layout.grid(row=1, column=0)

        self.canvas = Canvas(self.layout, bg="white", height=400, width=400, cursor='fleur')
        self.canvas.bind("<Button-1>", self.getMousePos)
        self.canvas.bind("<B1-Motion>", self.mouseDrag)
        self.canvas.bind("<ButtonRelease-1>", self.mouseRelease)
        self.canvas.bind("<Motion>", self.mouseMove)
        self.canvas.grid(row=1, column=1)

        self.shapeButton = Button(self.button_layout, text='★', font=('Arial', 25), width=1, height=1, command=lambda: self.selectTool('shape'))
        self.shapeButton.bind("<Enter>", lambda event, text='Polygon': self.showTooltip(event, text))
        self.shapeButton.bind("<Leave>", self.hideTooltip)
        self.shapeButton.bind("<Button-3>", self.choosePolygonMenu)
        self.shapeButton.grid(row=0, column=0)

        self.removeButton = Button(self.button_layout, text='✕', fg='red', font=('Arial', 25), width=1, height=1, command=lambda: self.selectTool('remove'))
        self.removeButton.bind("<Enter>", lambda event, text='Delete': self.showTooltip(event, text))
        self.removeButton.bind("<Leave>", self.hideTooltip)
        self.removeButton.grid(row=1, column=0)

        self.fillButton = Button(self.button_layout, image=self.fill_bucket_photo, font=('Arial', 25), width=41, height=40, command=lambda: self.selectTool('fill'))
        self.fillButton.bind("<Enter>", lambda event, text='Fill': self.showTooltip(event, text))
        self.fillButton.bind("<Leave>", self.hideTooltip)
        self.fillButton.grid(row=2, column=0)

        self.colorButton = Button(self.button_layout, image=self.gradient_photo, font=('Arial', 25), width=41, height=40, command=lambda: self.chooseColor())
        self.colorButton.bind("<Enter>", lambda event, text='Color Picker': self.showTooltip(event, text))
        self.colorButton.bind("<Leave>", self.hideTooltip)
        self.colorButton.grid(row=3, column=0)

        
        

        self.root.mainloop()


    def choosePolygonMenu(self, event):
        self.polygonMenu.post(event.x_root, event.y_root)
    
    def choosePolygon(self, shape):
        self.shape = shape

    def chooseColor(self):
        self.color = colorchooser.askcolor(title='Color Picker')[1]
        print(self.color)

    def selectTool(self, tool):
        self.tool = tool
        if tool == 'remove':
            self.canvas.config(cursor='pirate')
        elif tool == 'shape':
            self.canvas.config(cursor='fleur')
        elif tool == 'fill':
            self.canvas.config(cursor='spraycan')

    def getMousePos(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.tool == 'shape':
            self.current_tag += 1
            if self.shape == 'polygon':
                if self.polygon == []:
                    self.first_point = True
                self.polygon.append(self.start_x)
                self.polygon.append(self.start_y)
                if self.polyLine:
                    self.polyLines.append(self.canvas.create_line(self.canvas.coords(self.polyLine)))
                if ((self.polygon[-2] - self.polygon[0]) <= 2 and (self.polygon[-1] - self.polygon[1]) <= 2) and len(self.polygon) > 4:
                    self.canvas.create_polygon(self.polygon, tags='a' + str(self.current_tag))
                    self.first_point = False
                    self.polygon = []
                    for line in self.polyLines:
                        self.canvas.delete(line)
        elif self.tool == 'remove':
            for shape_id in [id for id in range(self.current_tag + 1)]:
                tag = 'a' + str(shape_id)
                print(tag, ';', self.current_tag)
                if self.collides(event.x, event.y, self.canvas.coords(tag)):
                    self.canvas.delete(tag)
                    break
        elif self.tool == 'fill':
            for shape_id in [id for id in range(self.current_tag + 1)]:
                tag = 'a' + str(shape_id)
                if self.collides(event.x, event.y, self.canvas.coords(tag)):
                    self.fillShape(self.canvas.type(tag), self.canvas.coords(tag), tag)
                    break

    def mouseDrag(self, event):
        if self.tool == 'shape':
            if self.shape == 'rect':
                if self.rect:
                    print(self.current_tag, ';', self.canvas.coords('a' + str(self.current_tag)))
                    self.canvas.delete('a' + str(self.current_tag))
                self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, tags='a' + str(self.current_tag))
            elif self.shape == 'oval':
                if self.oval:
                    self.canvas.delete('a' + str(self.current_tag))
                self.oval = self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, tags='a' + str(self.current_tag))
    
    def mouseMove(self, event):
        if self.first_point:
            if self.polyLine:
                self.canvas.delete(self.polyLine)
            self.polyLine = self.canvas.create_line(event.x, event.y, self.polygon[-2], self.polygon[-1])
        
            
    
    def mouseRelease(self, event):
        if self.tool == 'rect':
            self.rect = None

    def collides(self, mouse_x, mouse_y, coords):
        #print(coords, ';', mouse_x, ',', mouse_y)
        if coords != []:
            if (mouse_x >= coords[0] and mouse_x <= coords[2]) and (mouse_y >= coords[1] and mouse_y <= coords[3]):
                return True
        return False


    def showTooltip(self, event, text):
        cx, cy = event.x_root, event.y_root
        self.tooltip_label.config(text=text)
        self.tooltip.wm_geometry("+%d+%d" % (cx + 10, cy + 10))
        self.tooltip.update()
        self.tooltip.deiconify()
    
    def hideTooltip(self, event):
        self.tooltip.withdraw()
    
    def fillShape(self, shape, coords, tag):
        print(shape, ';', coords)
        self.canvas.delete(tag)
        if shape == 'rectangle':
            if self.color == '#ffffff':
                self.canvas.create_rectangle(coords, tags=tag, fill=self.color)
            else:
                self.canvas.create_rectangle(coords, tags=tag, fill=self.color, width=0)
        elif shape == 'oval':
            if self.color == '#ffffff':
                self.canvas.create_oval(coords, tags=tag, fill=self.color)
            else:
                self.canvas.create_oval(coords, tags=tag, fill=self.color, width=0)
        elif shape == 'polygon':
            if self.color == '#ffffff':
                self.canvas.create_polygon(coords, tags=tag, fill=self.color)
            else:
                self.canvas.create_polygon(coords, tags=tag, fill=self.color, width=0)


        

        
    



app_window = EasyCMUCanvas()




