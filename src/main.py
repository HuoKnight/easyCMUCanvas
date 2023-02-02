from tkinter import *
from tkinter import colorchooser
#from PIL import ImageTk, Image


    # TODO: 
    # - Create ID system so that each visual rectangle has an incremented ID, and rectangles that are created and then deleted
    #   during resizing do not effect the ID count. | DONE
    # - Add all shapes
    # - Include id system for all shapes
    # - Add remove tool | DONE
    # - Add custom cursors to canvas; Fleur for shape resizing, pirate for removing, spraycan for color filling
    # - Add fill button | DONE
    # - Make button images work | Done

class EasyCMUCanvas():
    def __init__(self):
        self.root = Tk()
        self.root.wm_title("Easy CMU Canvas")
        self.root.resizable(False, False)
        self.tool = 'shape'
        self.rect = None
        self.oval = None
        self.current_tag = -1
        self.shape = 'rect'
        self.color = '#000000'

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
        self.canvas.grid(row=1, column=1)

        self.rectButton = Button(self.button_layout, text='▮', font=('Arial', 25), width=1, height=1, command=lambda: self.selectTool('shape')).grid(row=0, column=0)   
        self.removeButton = Button(self.button_layout, text='✕', fg='red', font=('Arial', 25), width=1, height=1, command=lambda: self.selectTool('remove')).grid(row=1, column=0)
        self.fillButton = Button(self.button_layout, image=self.fill_bucket_photo, font=('Arial', 25), width=41, height=40, command=lambda: self.selectTool('fill')).grid(row=2, column=0)
        self.colorButton = Button(self.button_layout, image=self.gradient_photo, font=('Arial', 25), width=41, height=40, command=lambda: self.chooseColor()).grid(row=3, column=0)

        
        

        self.root.mainloop()


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
                    shape_size = self.canvas.coords(tag)
                    self.canvas.delete(tag)
                    self.canvas.create_rectangle(shape_size[0], shape_size[1], shape_size[2], shape_size[3], tags=tag, fill=self.color)
                    break

    def mouseDrag(self, event):
        if self.tool == 'shape':
            if self.rect:
                print(self.current_tag, ';', self.canvas.coords('a' + str(self.current_tag)))
                self.canvas.delete('a' + str(self.current_tag))
            current_x = event.x
            current_y = event.y
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, current_x, current_y, tags='a' + str(self.current_tag))
            
    
    def mouseRelease(self, event):
        if self.tool == 'rect':
            self.rect = None

    def collides(self, mouse_x, mouse_y, coords):
        print(coords, ';', mouse_x, ',', mouse_y)
        if coords != []:
            if (mouse_x >= coords[0] and mouse_x <= coords[2]) and (mouse_y >= coords[1] and mouse_y <= coords[3]):
                return True
        return False
        

        
    



app_window = EasyCMUCanvas()




