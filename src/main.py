from tkinter import *

    # TODO: 
    # - Create ID system so that each visual rectangle has an incremented ID, and rectangles that are created and then deleted
    #   during resizing do not effect the ID count.
    # - Include this for all shapes
    # - Add remove tool
    # - Add custom cursors to canvas

class EasyCMUCanvas():
    def __init__(self):
        self.root = Tk()
        self.root.wm_title("Easy CMU Canvas")
        self.root.resizable(False, False)
        self.tool = 'rect'
        self.rect = None
        self.current_id = 0


        self.layout = Frame(self.root)
        self.layout.grid(row=0, column=0)
        self.button_layout = Frame(self.layout)
        self.button_layout.grid(row=1, column=0)

        self.canvas = Canvas(self.layout, bg="white", height=400, width=400)
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
            self.current_id += 1

    def mouseDrag(self, event):
        if self.tool == 'rect':
            if self.rect:
                self.current_id -= 1
                print(self.current_id, ';', self.rect)
                self.canvas.delete(self.rect)
            current_x = event.x
            current_y = event.y
            self.current_id += 1
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, current_x, current_y, tag=self.current_id)
            
    
    def mouseRelease(self, event):
        if self.tool == 'rect':
            self.rect = None
        
    



app_window = EasyCMUCanvas()




