# https://stackoverflow.com/questions/29789554/tkinter-draw-rectangle-using-a-mouse
from   .InputFrame import InputFrame
from   PIL         import ImageTk
from   tkinter     import *    
import sctg.globals


class EditWindow(Tk):
    def __init__(self, image, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x = self.y = 0
        self.attributes('-fullscreen', True          )
        self.bind      ('<Escape>'   , self.abort_win)
        self.bind      ('<Return>'   , self.close_win)

        self.menu = Menu(self, tearoff = 0)
        self.menu.add_command(label="Box")
        self.menu.add_command(label="Text")
        self.menu.add_command(label="Draw")
        self.menu.add_command(label="Arrow")
        self.menu.add_separator()
        self.menu.add_command(label="Select")
        self.menu.add_command(label="Add Tags", command=self.add_tags, accelerator="Ctrl+T")
        self.menu.bind_all('<Control-t>', self.add_tags)

        self.canvas = Canvas(self,  cursor="cross")
        self.canvas.bind("<ButtonPress-1>"  , self.on_button_press  )
        self.canvas.bind("<B1-Motion>"      , self.on_move_press    )
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<Button-3>"       , self.show_popup_menu  )
        
        self.rect      = None
        self.start_x   = None
        self.start_y   = None
        self.curX      = None
        self.curY      = None
        self.selection = None

        self.image = image
        self.tk_im = ImageTk.PhotoImage(image)
        self.canvas.create_image(0,0,anchor="nw",image=self.tk_im)   
        
        self.canvas.pack(fill=BOTH, expand=True)


    def add_tags(self, event=None):
        InputFrame(master=self)
        # iw = InputFrame() # provide callback to MainWindow so that it can return results to MyFrame
        # iw.set_callback(self.set_label)


    def close_win(self, event):
        if not sctg.globals.input_frame_exists:
            self.quit()
        sctg.globals.input_frame_exists = False


    def abort_win(self, event):
        if not sctg.globals.input_frame_exists:
            print(sctg.globals.InputFrmTXT)
            self.image = None
            self.quit()
        sctg.globals.input_frame_exists = False


    def show_popup_menu(self, event):
        try    : self.menu.tk_popup(event.x_root, event.y_root)
        finally: self.menu.grab_release()


    def on_button_press(self, event):
        self.menu.unpost()
        self.start_x = self.canvas.canvasx(event.x) # save mouse drag start position
        self.start_y = self.canvas.canvasy(event.y)
        if not self.rect: # create rectangle if not yet exist
            self.rect = self.canvas.create_rectangle(self.x, self.y, 1,1, outline='gray', dash=(4,6), width=4) # https://www.delftstack.com/howto/python-tkinter/tkinter-rectangle/


    def on_move_press(self, event):
        self.curX = self.canvas.canvasx(event.x)
        self.curY = self.canvas.canvasy(event.y)
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY) # expand rectangle as you drag the mouse


    def on_button_release(self, event):
        if self.curX and self.curY:
            if self.start_x == event.x or self.start_y == event.y:
                self.canvas.coords(self.rect,0,0,0,0) 
            x1 = self.start_x if self.start_x < self.curX else self.curX 
            y1 = self.start_y if self.start_y < self.curY else self.curY
            x2 = self.start_x if self.start_x > self.curX else self.curX
            y2 = self.start_y if self.start_y > self.curY else self.curY
            self.image = self.image.crop((x1, y1, x2, y2))



# if __name__ == "__main__":
#     root = CropWindow()
#     root.mainloop()
