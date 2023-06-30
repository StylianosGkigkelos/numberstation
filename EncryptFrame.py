import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
import tkinter.ttk as ttk
import re
from main import encrypt


class EncryptFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master)

        self.pattern = '([a-zA-Z0-9\s_\\.\-\(\):])+(txt|wav)$'
        self.iteration_number = tk.IntVar()
        self.message_var = tk.StringVar()
        self.otp_var = tk.StringVar()
        self.enc_var = tk.StringVar()
        self.wav_var = tk.StringVar()

        message_label = ttk.Label(master=self, text='Message')
        message_label.grid(row=0, column=0, columnspan=1)

        message_entry = tk.Entry(master=self, textvariable=self.message_var)
        message_entry.grid(row=0, column=1, columnspan=1)

        otp_label = ttk.Label(master=self, text='One Time Pad filename')
        otp_label.grid(row=2, column=0, columnspan=1)

        # tk.filedialog.asksaveasfile()
        otp_entry = tk.Entry(master=self, textvariable=self.otp_var, state=tk.DISABLED)
        otp_entry.grid(row=2, column=1, columnspan=1)

        self.folder_image = tk.PhotoImage(file=r'resources\\folder.png')
        otp_button = ttk.Button(master=self, text='hi',
                                command=lambda t='otp_f': self.choose_target(t), image=self.folder_image)
        otp_button.grid(row=2, column=2)

        # otp_entry

        encrypt_label = ttk.Label(master=self, text='Encrypt filename')
        encrypt_label.grid(row=3, column=0, columnspan=1)

        enc_entry = tk.Entry(master=self, textvariable=self.enc_var, state=tk.DISABLED)
        enc_entry.grid(row=3, column=1, columnspan=1)

        enc_button = ttk.Button(master=self, text='hi',
                                command=lambda t='enc_f': self.choose_target(t), image=self.folder_image)
        enc_button.grid(row=3, column=2)

        wav_label = ttk.Label(master=self, text='WAV filename')
        wav_label.grid(row=4, column=0, columnspan=1)

        wav_entry = tk.Entry(master=self, textvariable=self.wav_var, state=tk.DISABLED)
        wav_entry.grid(row=4, column=1, columnspan=1)

        wav_button = ttk.Button(master=self, text='hi',
                                command=lambda t='wav_f': self.choose_target(t), image=self.folder_image)
        wav_button.grid(row=4, column=2)

        iter_label = ttk.Label(master=self, text='Number of iterations')
        iter_label.grid(row=5, column=1, columnspan=3)

        iter_frame = ttk.Frame(self)
        iter_frame.grid(row=6, column=1, columnspan=3)
        iter_listbox = tk.Listbox(master=iter_frame)
        iter1_radio = ttk.Radiobutton(iter_listbox, text='1', value=1, variable=self.iteration_number)
        iter1_radio.grid(column=0, row=0)
        iter2_radio = ttk.Radiobutton(iter_listbox, text='2', value=2, variable=self.iteration_number)
        iter2_radio.grid(column=0, row=1)
        iter3_radio = ttk.Radiobutton(iter_listbox, text='3', value=3, variable=self.iteration_number)
        iter3_radio.grid(column=0, row=2)

        iter_listbox.pack()

        enc_button = ttk.Button(master=self, text='Encrypt', command=self.enc)
        enc_button.grid(row=7, column=1, sticky='')


    def enc(self):
        if len(re.findall(self.pattern, self.otp_var.get())) == 0 \
                or len(re.findall(self.pattern, self.enc_var.get())) == 0 \
                or len(re.findall(self.pattern, self.wav_var.get())) == 0:
            tk.messagebox.showerror(title='Input Error', message='Filepath cannot be empty')
        else:
            encrypt(self.message_var.get(), self.iteration_number.get(), self.enc_var.get(), self.otp_var.get(), self.wav_var.get())

    def choose_target(self, t):
        if t == 'otp_f':
            self.otp_var.set(tk.filedialog.asksaveasfilename(defaultextension='Text .txt',
                                                             filetypes=[('Text *.txt')],
                                                             initialdir='',
                                                             title="Choose OTP Filename"
                                                             ))
        elif t == 'enc_f':
            self.enc_var.set(tk.filedialog.asksaveasfilename(defaultextension='Text .txt',
                                                             filetypes=[('Text *.txt')],
                                                             initialdir='',
                                                             title="Choose Encrypted Filename"
                                                             ))

        elif t == 'wav_f':
            self.wav_var.set(tk.filedialog.asksaveasfilename(defaultextension='WAV .wav',
                                                             filetypes=[('WAV *.wav')],
                                                             initialdir='',
                                                             title="Choose Audio Filename"
                                                             ))