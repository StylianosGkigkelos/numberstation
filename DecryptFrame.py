import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
import tkinter.ttk as ttk
import re
from main import decrypt


class DecryptFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.pattern = '([a-zA-Z0-9\s_\\.\-\(\):])+(txt)$'
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.otp_var = tk.StringVar()
        self.enc_var = tk.StringVar()

        otp_label = ttk.Label(master=self, text='One Time Pad filename')
        otp_label.grid(row=0, column=0, columnspan=1)

        otp_entry = tk.Entry(master=self, textvariable=self.otp_var, state=tk.DISABLED)
        otp_entry.grid(row=0, column=1, columnspan=1)

        self.folder_image = tk.PhotoImage(file=r'resources\\folder.png')
        otp_button = ttk.Button(master=self, text='hi',
                                command=lambda t='otp_f': self.choose_target(t), image=self.folder_image)
        otp_button.grid(row=0, column=2)

        enc_label = ttk.Label(master=self, text='Encrypted filename')
        enc_label.grid(row=1, column=0, columnspan=1)

        enc_entry = tk.Entry(master=self, textvariable=self.enc_var, state=tk.DISABLED)
        enc_entry.grid(row=1, column=1, columnspan=1)

        enc_button = ttk.Button(master=self, text='hi',
                                command=lambda t='enc_f': self.choose_target(t), image=self.folder_image)
        enc_button.grid(row=1, column=2)

        dec_button = ttk.Button(master=self, text='Decrypt', command=self.dec)
        dec_button.grid(row=2, column=1)

    def dec(self):
        if len(re.findall(self.pattern, self.otp_var.get())) == 0 \
                or len(re.findall(self.pattern, self.enc_var.get())) == 0:
            tk.messagebox.showerror(title='Input Error', message='Filepath cannot be empty')
        else:
            message = decrypt(self.enc_var.get(), self.otp_var.get())
            tkinter.messagebox.showinfo('Decrypted Message', message)

    def choose_target(self, t):
        if t == 'otp_f':
            self.otp_var.set(tk.filedialog.askopenfilename(defaultextension='Text .txt',
                                                             filetypes=[('Text *.txt')],
                                                             initialdir='',
                                                             title="Choose OTP Filename"
                                                             ))
        elif t == 'enc_f':
            self.enc_var.set(tk.filedialog.askopenfilename(defaultextension='Text .txt',
                                                             filetypes=[('Text *.txt')],
                                                             initialdir='',
                                                             title="Choose Encrypted Filename"
                                                             ))
