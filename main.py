from tkinter import *
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
from gtts import gTTS, lang
import os
from tkinter import messagebox
import speech_recognition as sr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
from difflib import SequenceMatcher

root = tk.Tk()
canvas1 = tk.Canvas(root, width=800, height=400)
canvas1.pack()

label1 = tk.Label(root, text='Data Çizdirici')
label1.config(font=('Arial', 15))
canvas1.create_window(400, 50, window=label1)

label2 = tk.Label(root,
                  text='Once Excel Dosyanızı Yüklemeniz gerekmektedir. Yükledikten sonra konuşup çizdir butonuna basmanız gerekmektedir.')
label2.config(font=('Arial', 10))
canvas1.create_window(400, 75, window=label2)

label3 = tk.Label(root, text='Söylediğiniz şey ')
label3.config(font=('Arial', 10))
canvas1.create_window(400, 100, window=label3)


def speech_to_text():
    global text
    # Recognizer tanımla
    recorder = sr.Recognizer()
    # Mikrofonu kullan
    messagebox.showinfo(message="Bu butona tıkladıktan sonra konuşmaya başlayabilirsiniz")
    with sr.Microphone() as mic:
        recorder.adjust_for_ambient_noise(mic)
        audio_input = recorder.listen(mic)
        try:  # Texte cevir
            text_output = recorder.recognize_google(audio_input, language="tr-TR")
            label3 = tk.Label(root, text='Söylediğiniz şey: ' + text_output)
            text = text_output
            label3.config(font=('Arial', 10))
            canvas1.create_window(400, 100, window=label3)
            # Outputu yazdır
            messagebox.showinfo(message="Söylediğiniz Şey:\n " + text_output)
            text = text_output

        except:
            messagebox.showerror(message="Algılayamadım.")


def getExcel():
    cond = 0
    global df
    import_file_path = filedialog.askopenfilename()
    df = pd.read_excel(import_file_path)


def clear_charts():
    try:
        bar1.get_tk_widget().pack_forget()
    except:
        print('Bar1 yok')
    try:
        bar2.get_tk_widget().pack_forget()
    except:
        print('Bar2 yok')
    try:
        bar3.get_tk_widget().pack_forget()
    except:
        print('Bar3 yok')

def plot_hist():
    try:
        global bar1
        x = df['boy']
        y = df['türler']
        figure1 = Figure(figsize=(4, 3), dpi=100)
        subplot1 = figure1.add_subplot(111)
        subplot1.hist(df, bins=10)
        try:
            subplot1.set_title('Grafik' + text)
        except:
            subplot1.set_title('Grafik')
        bar1 = FigureCanvasTkAgg(figure1, root)
        bar1.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=0)
    except:
        messagebox.showinfo(message="Söylediğiniz şey anlaşılamadı veya dosya yüklü değil", title='Hata')


def plot_pie():
    try:
        global bar2
        x = df['boy']
        y = df['türler']

        figure2 = Figure(figsize=(4, 3), dpi=100)
        subplot2 = figure2.add_subplot(111)
        try:
            try:
                subplot2.plot(df[df.columns[0]])
            except:
                try:
                    subplot2.plot(df[df.columns[1]])
                except:
                    subplot2.plot(df[df.columns[3]])
        except:
            messagebox.showinfo(message="Cizilemiyor", title='Hata')
        try:
            subplot2.set_title('Grafik' + text)
        except:
            subplot2.set_title('Grafik')
        bar2 = FigureCanvasTkAgg(figure2, root)
        bar2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=0)
    except:
        messagebox.showinfo(message="Söylediğiniz şey anlaşılamadı veya dosya yüklü değil", title='Hata')

def string_dist():
    print(text)
    str1 = str(text).split()
    print('No Eror')
    highest_plot_pie = 0
    highest_plot_hist = 0
    for i in str1:
        past = SequenceMatcher(a=i.lower(), b='çizgi'.lower())
        histo = SequenceMatcher(a=i.lower(), b='histogram'.lower())
        if highest_plot_pie < past.ratio():
            highest_plot_pie = past.ratio()
        if highest_plot_hist < histo.ratio():
            highest_plot_hist = histo.ratio()
    if highest_plot_pie < highest_plot_hist:
        print('hist')
        return 'hist'
    else:
        print('cizgi')
        return 'cizgi'

def plot():
    global bar3
    try:
        print('123')
        cond = string_dist()
        print(cond)
        if cond == 'hist':
            figure3 = Figure(figsize=(4, 3), dpi=100)
            subplot3 = figure3.add_subplot(111)
            subplot3.hist(df, bins=10)
            subplot3.set_title('Grafik Hist')
            bar3 = FigureCanvasTkAgg(figure3, root)
            bar3.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=0)
        else:
            figure3 = Figure(figsize=(4, 3), dpi=100)
            subplot3 = figure1.add_subplot(111)
            subplot3.plot(df)
            subplot3.set_title('Grafik')
            bar3 = FigureCanvasTkAgg(figure3, root)
            bar3.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=0)
    except:
        messagebox.showinfo(message="Söylediğiniz şey anlaşılamadı veya dosya yüklü değil", title='Hata')


button1 = tk.Button(text='Dosya Yükle...', command=getExcel, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(400, 180, window=button1)

button2 = tk.Button(root, text='Temizle', command=clear_charts, bg='green', font=('helvetica', 11, 'bold'))
canvas1.create_window(400, 220, window=button2)

button3 = tk.Button(root, text='Çıkış!', command=root.destroy, bg='green', font=('helvetica', 11, 'bold'))
canvas1.create_window(400, 340, window=button3)

button4 = tk.Button(root, text='Konuş', bg='green', font=('helvetica', 11, 'bold'), command=speech_to_text)
canvas1.create_window(400, 260, window=button4)

button5 = tk.Button(root, text='Çizdir', bg='green', font=('helvetica', 11, 'bold'), command=plot)
canvas1.create_window(400, 300, window=button5)

button6 = tk.Button(root, text='Histogram', bg='green', font=('helvetica', 11, 'bold'), command=plot_hist)
canvas1.create_window(440, 380, window=button6)

button7 = tk.Button(root, text='Cizgi', bg='green', font=('helvetica', 11, 'bold'), command=plot_pie)
canvas1.create_window(360, 380, window=button7)

root.mainloop()
