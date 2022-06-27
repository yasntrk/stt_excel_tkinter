from tkinter import *
from tkinter import ttk
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
from itertools import groupby
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
from difflib import SequenceMatcher
import tkinter
import customtkinter
global text
from pydub import AudioSegment
from pydub.playback import play
import time
from numpy import array
from numpy import argmax
import sklearn
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import seaborn as sns
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OneHotEncoder
from re import I

##Sample text

# uzunluk ortalama içeriyorsa dahil et
# renkler yeşilse çıkart
# histogram uzunluk tür

# nokta renkler ve uzunluk
# pasta renkler
# pasta

global text
text = 'pasta renkler'
global root
global FirstData
global SecondData

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")
root = customtkinter.CTk()  # create CTk window like the Tk window
root.geometry("1920x1080")

root.title('Data Çizdirici')
label1 = customtkinter.CTkLabel(root, text='Data Çizdirici')
label1.config(font=('Arial', 30))
label1.place(x=1000, y=90)

label5 = customtkinter.CTkLabel(root, text='Konsol')
label5.config(font=('Arial', 15))
label5.place(x=500, y=130)

label3 = customtkinter.CTkLabel(root, text='Söylediğiniz şey ')

# canvas1.create_window(400, 100, window=label3)

def speech_to_text():
    global text
    # Recognizer tanımla
    recorder = sr.Recognizer()
    # Mikrofonu kullan
    messagebox.showinfo(message="Bu butona tıkladıktan sonra konuşmaya başlayabilirsiniz")
    with sr.Microphone() as mic:
        recorder.adjust_for_ambient_noise(mic)
        audio_input = recorder.listen(mic,timeout=2, phrase_time_limit=5)
        try:  # Texte cevir
            text_output = recorder.recognize_google(audio_input, language="tr-TR")
            label3 = customtkinter.CTkLabel(text='Söylediğiniz şey: ' + text_output)
            text = text_output
            label3.place(x=480, y=150)
            # Outputu yazdır
            messagebox.showinfo(message="Söylediğiniz Şey:\n " + text_output)
            text = text_output
        except:
            messagebox.showerror(message="Algılayamadım.")
def reg():
    global bar5
    data = pd.read_excel('cicekler.xlsx')

    # Converting type of columns to category
    data['renkler'] = data['renkler'].astype('category')
    data['uzunluk'] = data['uzunluk'].astype('category')
    data['türler'] = data['türler'].astype('category')

    # Assigning numerical values and storing it in another columns
    data['renkler_new'] = data['renkler'].cat.codes
    data['uzunluk_new'] = data['uzunluk'].cat.codes
    data['turler_new'] = data['türler'].cat.codes

    # Create an instance of One-hot-encoder
    enc = OneHotEncoder()

    # Passing encoded columns
    enc_data = pd.DataFrame(enc.fit_transform(data[['uzunluk_new', 'renkler_new', 'turler_new']]).toarray())

    # Merge with main
    New_df = data.join(enc_data)
    New_df.to_excel("New_df.xlsx")
    readNew_df = pd.read_excel("New_df.xlsx")

    useData = pd.DataFrame(
        {'uzunluk': New_df['uzunluk_new'], 'renkler': New_df['renkler_new'], 'turler': New_df['turler_new'],
         'boy': data['boy']})

    useData.to_excel("data.xlsx")

    newData = pd.read_excel("data.xlsx")

    colors = newData[FirstData]
    length = newData[SecondData]

    x_train, x_test, y_train, y_test = train_test_split(colors, length, test_size=0.33, random_state=1234)
    lr = LinearRegression()

    x_train = pd.DataFrame(x_train)

    x_test = pd.DataFrame(x_test)

    lr.fit(x_train, y_train)
    prediction = lr.predict(x_test)

    x_train = x_train.sort_index()
    y_train = y_train.sort_index()

    figure3 = Figure(figsize=(4, 3), dpi=100)
    subplot3 = figure3.add_subplot(111)
    subplot3.plot(x_train, y_train)
    subplot3.set_title('Grafik Hist')
    subplot3.plot(x_test, lr.predict(x_test))
    subplot3.set_xlabel(FirstData)
    subplot3.set_ylabel(SecondData)
    bar5 = FigureCanvasTkAgg(figure3, frame_left4)
    bar5.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=0)

def getExcel():
    global df
    import_file_path = filedialog.askopenfilename()
    df = pd.read_excel(import_file_path)

def plot_Excel():
    cols = list(df.columns)
    global tree
    tree = ttk.Treeview(frame_left2)
    tree.pack()
    tree["columns"] = cols
    for i in cols:
        tree.column(i, anchor="w")
        tree.heading(i, text=i, anchor='w')
    for index, row in df.iterrows():
        tree.insert("", 0, text=index, values=list(row))

# Filtreleme ve sıraya dizme fonksiyonu
def bolum_karsilastir(filtreler, siralama_kolonu):
    # Girdinin kendisini bozmamak için kopyalayalım
    global filt_data_frame
    global  df
    filt_data_frame = df
    # Filtreleme
    for kolon, metin, durum, islem in filtreler:
        if islem == 'dahil et':
            print(kolon, 'kolonunda ', metin, 'içeren veriler alındı')
            if durum == "iceriyorsa":
                filt_data_frame = filt_data_frame[filt_data_frame[kolon].str.contains(metin)]
            elif durum == "eşitse":
                filt_data_frame = filt_data_frame[filt_data_frame[kolon] == metin]
            else:
                print(durum, 'anlaşılamadı')
        elif islem == 'çıkart':
            print(kolon, 'kolonunda ', metin, 'içeren veriler dışarıda bırakıldı')
            if durum == "iceriyorsa":
                filt_data_frame = filt_data_frame[~filt_data_frame[kolon].str.contains(metin)]
            elif durum == "eşitse":
                filt_data_frame = filt_data_frame[filt_data_frame[kolon] != metin]
            else:
                print(durum, 'anlaşılamadı')
        else:
            print('Filtre içeriği anlaşılamadı ve uygulanmadı: ', kolon, metin, durum, islem)
    df = filt_data_frame.sort_values(by=[siralama_kolonu], ascending=False)
    return df

def filter_maker():
    global filter,filter1
    columns = df.columns
    for col_names in columns:
        for texts in text.split():
            filter_ratio = SequenceMatcher(a=col_names.lower(), b=texts.lower())
            if filter_ratio.ratio() > 0.7:
                filter1 = col_names

    arr = df[filter1].value_counts().index  # Takes Cols Automaticly
    print(arr)
    for spices in arr:
        for texts in text.split():
            filter2_ratio = SequenceMatcher(a=spices.lower(), b=str(texts).lower())
            if filter2_ratio.ratio() > 0.55:
                filter2 = spices
    str1 = str(text).split()
    cikart = 0
    dahil_et = 0
    iceriyorsa = 0
    esitse = 0
    for i in str1:
        cikart_filter = SequenceMatcher(a=i.lower(), b="çıkart".lower())
        if cikart_filter.ratio() > cikart:
            cikart = cikart_filter.ratio()

        dahil_et_filter = SequenceMatcher(a=i.lower(), b="dahil et".lower())
        if dahil_et_filter.ratio() > dahil_et:
            dahil_et = dahil_et_filter.ratio()
        iceriyorsa_filter = SequenceMatcher(a=i.lower(), b='içeriyorsa'.lower())
        if iceriyorsa_filter.ratio() >iceriyorsa:
            iceriyorsa = iceriyorsa_filter.ratio()

        esitse_filter = SequenceMatcher(a=i.lower(), b='eşitse'.lower())
        if esitse_filter.ratio() > esitse:
            esitse = esitse_filter.ratio()

        if cikart > dahil_et:  # Check conditions
            filter4 = "çıkart"
        else:
            filter4 = "dahil et"
        if iceriyorsa > esitse:
            filter3 = "iceriyorsa"
        else:
            filter3 = "eşitse"
        filter = [(filter1, filter2, filter3, filter4)]

def do_filter():
    filter_maker()
    bolum_karsilastir(filter, filter1)
# ----------------------------------------------------------------
def clear_charts():
    try:
        bar1.get_tk_widget().pack_forget()
        root.update()
        frame_left3.update()
        frame_left2.update()
        frame_left.update()
        frame_left4.update()
    except:
        print('Bar1 yok')
    try:
        bar2.get_tk_widget().pack_forget()
        root.update()
        frame_left3.update()
        frame_left2.update()
        frame_left.update()
        frame_left4.update()
    except:
        print('Bar2 yok')
    try:
        bar3.get_tk_widget().pack_forget()
        root.update()
        frame_left3.update()
        frame_left2.update()
        frame_left.update()
        frame_left4.update()

    except:
        print('Bar3 yok')
    try:
        tree.pack_forget()
        root.update()
        tree.update()

        frame_left3.update()
        frame_left2.update()
        frame_left.update()
        frame_left4.update()

    except:
        print('Tree yok')
    try:
        for widgets in frame_left3.winfo_children():
            widgets.destroy()
    except:
        print('Olmadı')
    try:
        bar5.get_tk_widget().pack_forget()
        root.update()
        frame_left3.update()
        frame_left2.update()
        frame_left.update()
        frame_left4.update()

    except:
        pass

def change_mode():
    if switch_2.get() == 1:
        customtkinter.set_appearance_mode("light")
    else:
        customtkinter.set_appearance_mode("dark")

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
        bar2 = FigureCanvasTkAgg(figure2, frame_left3)
        bar2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=0)
    except:
        messagebox.showinfo(message="Söylediğiniz şey anlaşılamadı veya dosya yüklü değil", title='Hata')

def string_dist():
    print(text)
    str1 = str(text).split()
    print('No Error')
    highest_plot_pie = 0
    highest_plot_hist = 0
    highest_plot_plot = 0
    highest_plot_kor = 0
    arr_finder = [0, 0, 0, 0]
    for i in str1:
        cizgi = SequenceMatcher(a=i.lower(), b='çizgi'.lower())
        histo = SequenceMatcher(a=i.lower(), b='histogram'.lower())
        past = SequenceMatcher(a=i.lower(), b='pasta'.lower())
        kor = SequenceMatcher(a=i.lower(), b='nokta'.lower())
        if arr_finder[0] < past.ratio():
            arr_finder[0] = past.ratio()
        if arr_finder[1] < histo.ratio():
            arr_finder[1] = histo.ratio()
        if arr_finder[2] < cizgi.ratio():
            arr_finder[2] = cizgi.ratio()
        if arr_finder[3] < kor.ratio():
            arr_finder[3] = kor.ratio()
    max_value = max(arr_finder)
    max_index = arr_finder.index(max_value)
    print(max_index)
    if max_index == 2:
        return 'cizgi'
    elif max_index == 1:
        return 'hist'
    elif max_index == 0:
        return 'pasta'
    elif max_index == 3:
        return 'nokta'

def give_cols():
    global array2
    global new_df
    global df
    new_df = pd.DataFrame()
    array2 = []
    cols = list(df.columns)
    x = str(text)
    str2 = x.split()
    for str23 in str2:
        for col in cols:
            ration = SequenceMatcher(a=str23.lower(), b=col.lower())
            print(float(ration.ratio()) + 5)
            if float(ration.ratio()) > 0.65:
                array2.append(col)
                new_df[col] = df[col]

def plot():
    global bar3
    cond = string_dist()
    give_cols()
    print(cond)
    if cond == 'hist':
        figure3 = Figure(figsize=(4, 3), dpi=100)
        subplot3 = figure3.add_subplot(111)
        subplot3.hist(new_df, bins=10)
        subplot3.set_title('Grafik Hist')
        bar3 = FigureCanvasTkAgg(figure3, frame_left3)
        bar3.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=0)
    elif cond == 'cizgi':
        figure3 = Figure(figsize=(4, 3), dpi=100)
        subplot3 = figure3.add_subplot(111)
        subplot3.plot(new_df)
        subplot3.set_title('Grafik')
        bar3 = FigureCanvasTkAgg(figure3, frame_left3)
        bar3.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=0)
    elif cond == 'pasta':
        try:
            new_df_cols = new_df.columns
            labels = df[new_df_cols[0]].unique()
            values = new_df.value_counts()
            figure3 = Figure(figsize=(4, 3), dpi=100)
            subplot3 = figure3.add_subplot(111)
            subplot3.pie(values,labels = labels)
            subplot3.set_title('Grafik')
            bar3 = FigureCanvasTkAgg(figure3, frame_left3)
            bar3.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=0)
        except:
            pass
    elif cond == 'nokta':
        new_df_cols = new_df.columns
        labels = df[new_df_cols[0]].unique()
        values = new_df.value_counts()
        figure3 = Figure(figsize=(4, 3), dpi=100)
        subplot3 = figure3.add_subplot(111)
        subplot3.stem(values)
        subplot3.set_title('Grafik')
        bar3 = FigureCanvasTkAgg(figure3, frame_left3)
        bar3.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=0)

def get_data1():
    global text
    text = entry.get()

def get_data2():
    global FirstData
    FirstData = entry2.get()

def get_data3():
    global SecondData
    SecondData = entry3.get()

button1 = customtkinter.CTkButton(text='Dosya Yükle...', command=getExcel)
button1.place(x=505, y=200)

button2 = customtkinter.CTkButton(root, text='Temizle', command=clear_charts)
button2.place(x=505, y=240)

button3 = customtkinter.CTkButton(root, text='Yazdır', command=plot_Excel)
button3.place(x=505, y=280)

button4 = customtkinter.CTkButton(root, text='Konuş', command=speech_to_text)
button4.place(x=575, y=320)

button5 = customtkinter.CTkButton(root, text='Çizdir', bg='green', command=plot)
button5.place(x=445, y=360)

button6 = customtkinter.CTkButton(root, text='Filtrele', bg='green', command=do_filter)
button6.place(x=575, y=360)

button7 = customtkinter.CTkButton(root, text='Çıkış!', bg='green', command=root.destroy)
button7.place(x=505, y=400)
button7.place(x=505, y=400)

button8 = customtkinter.CTkButton(root, text='Regresyon', bg='green', command=reg)
button8.place(x=445, y=320)

entry = customtkinter.CTkEntry(root,width=120, text='', placeholder_text= 'Çiz')
entry.grid(row=8, column=0, columnspan=2, pady=20, padx=20)

ent1 = customtkinter.CTkButton(text='Oku', command=get_data1)
ent1.place(x=150, y=58)

ent2 = customtkinter.CTkButton(text='Oku', command=get_data2)
ent2.place(x=150, y=128)

ent3 = customtkinter.CTkButton(text='Oku', command=get_data3)
ent3.place(x=150, y=198)


entry2 = customtkinter.CTkEntry(root,width=120, placeholder_text = 'Reg X')
entry2.grid(row=9, column=0, columnspan=2, pady=20, padx=20)

entry3 = customtkinter.CTkEntry(root,width=120, placeholder_text = 'Reg Y')
entry3.grid(row=10, column=0, columnspan=2, pady=20, padx=20)


frame_left = customtkinter.CTkFrame(root,width=180,corner_radius=0)
frame_left.grid(row=0, column=0, sticky="nswe")

frame_left2 = customtkinter.CTkFrame(root,width=0,corner_radius=0)
frame_left2.place(x=850, y=200)

frame_left3 = customtkinter.CTkFrame(root,width=0,corner_radius=0)
frame_left3.place(x=350, y=450)

switch_2 = customtkinter.CTkSwitch(master=frame_left,text="Dark Mode",command=change_mode)
switch_2.grid(row=10, column=0, pady=10, padx=20, sticky="w")

frame_left4 = customtkinter.CTkFrame(root,width=0,corner_radius=0)
frame_left4.place(x=1050, y=450)

root.mainloop()
