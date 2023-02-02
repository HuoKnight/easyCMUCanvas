from tkinter import *

    # TODO: 
    # - Create ID system so that each visual rectangle has an incremented ID, and rectangles that are created and then deleted
    #   during resizing do not effect the ID count. | DONE
    # - Include this for all shapes
    # - Add remove tool | DONE
    # - Add custom cursors to canvas; Fleur for shape resizing, pirate for removing, spraycan for color filling

class EasyCMUCanvas():
    def __init__(self):
        self.root = Tk()
        self.root.wm_title("Easy CMU Canvas")
        self.root.resizable(False, False)
        self.tool = 'rect'
        self.rect = None
        self.oval = None
        self.current_tag = -1


        self.layout = Frame(self.root)
        self.layout.grid(row=0, column=0)
        self.button_layout = Frame(self.layout)
        self.button_layout.grid(row=1, column=0)

        self.canvas = Canvas(self.layout, bg="white", height=400, width=400, cursor='fleur')
        self.canvas.bind("<Button-1>", self.getMousePos)
        self.canvas.bind("<B1-Motion>", self.mouseDrag)
        self.canvas.bind("<ButtonRelease-1>", self.mouseRelease)
        self.canvas.grid(row=1, column=1)

        self.rectButton = Button(self.button_layout, text='▮', font=('Arial', 25), width=1, height=1, command=lambda: self.selectTool('rect')).grid(row=0, column=0)   
        self.removeButton = Button(self.button_layout, text='✕', fg='red', font=('Arial', 25), width=1, height=1, command=lambda: self.selectTool('remove')).grid(row=1, column=0)
        

        self.root.mainloop()



    def selectTool(self, tool):
        self.tool = tool

    def getMousePos(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.tool != 'remove':
            self.current_tag += 1
        else:
            for shape_id in [id for id in range(self.current_tag + 1)]:
                tag = 'a' + str(shape_id)
                print(tag, ';', self.current_tag)
                if self.collides(event.x, event.y, self.canvas.coords(tag)):
                    self.canvas.delete(tag)
                    break

    def mouseDrag(self, event):
        if self.tool == 'rect':
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




