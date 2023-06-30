import tkinter as tk
import tkinter.ttk as ttk
from DecryptFrame import DecryptFrame
from EncryptFrame import EncryptFrame


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.pattern = '([a-zA-Z0-9\s_\\.\-\(\):])+(txt)$'
        self.wm_title('Number Station')
        self.minsize(400, 400)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.current_frame = EncryptFrame(self)
        self.current_frame.grid(row=0,column=0)
        self.mode_button = ttk.Button(master=self, text='Mode', command=self.switch_mode)
        self.mode_button.grid(row=0, column=1)

    def switch_mode(self):
        if isinstance(self.current_frame, EncryptFrame):
            self.current_frame.destroy()
            self.current_frame = DecryptFrame(self)
            self.current_frame.grid(row=0, column=0, padx=20, pady=20, ipadx=20, ipady=20, sticky='')
        elif isinstance(self.current_frame, DecryptFrame):
            self.current_frame.destroy()
            self.current_frame = EncryptFrame(self)
            self.current_frame.grid(row=0, column=0, padx=20, pady=20, ipadx=20, ipady=20, sticky='')


if __name__ == '__main__':
    gui = App()
    gui.mainloop()

