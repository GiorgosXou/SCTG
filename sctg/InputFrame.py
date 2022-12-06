import tkinter  as     tk
import sctg.globals


class InputFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.place(relx=.5, rely=.5, anchor="center")
        self.myLabel = tk.Label(self, text='Enter tags seperated by space')
        self.myLabel.pack()
        self.myEntryBox = tk.Entry(self)
        self.myEntryBox.focus_set()
        self.myEntryBox.bind('<Return>', self.set_value)
        self.myEntryBox.bind('<Escape>', self.abort_frm)
        self.myEntryBox.pack()
        self.mySubmitButton = tk.Button(self, text='OK', command=self.set_value)
        sctg.globals.input_frame_exists = True
        self.mySubmitButton.pack()


    def abort_frm(self, event):
        sctg.globals.InputFrmTXT = ''
        self.destroy()


    def set_value(self,event=None):
        sctg.globals.InputFrmTXT = self.myEntryBox.get()
        if event == None : sctg.globals.input_frame_exists=False # lolwhatam i doing 
        self.destroy()


    def set_callback(self, a_func):
        self.callback = a_func
