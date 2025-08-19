import os
import tkinter as tk
from tkinter import ttk
from tkinter import ttk,filedialog
import pyttsx3
import os
import pdfplumber
from bs4 import BeautifulSoup
import docx
import pandas as pd
from PIL import Image
import pytesseract
import sys
mn=tk.Tk()
mn.title('File reader')
mn.geometry('500x300')
if sys.platform == "win32":
    engine = pyttsx3.init(driverName="sapi5")
elif sys.platform == "darwin":
    engine = pyttsx3.init(driverName="nsss")
else:
    engine = pyttsx3.init(driverName="espeak")
unsupported_extensions = [".mp4", ".mkv", ".avi", ".mov", ".mp3", ".wav", ".flac",  ".exe", ".bin", ".dll"]
def read_file_text():
    file_path=filedialog.askopenfilename(title="Chose file to read")
    if file_path:
        ext = os.path.splitext(file_path)[1].lower()
        # if ext == ".txt":
        #     with open(file_path, "r", encoding="utf-8") as f: 
        #         engine.say(f.read())
        #         engine.runAndWait()
        #     return
        if ext == ".pdf":
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            engine.say(text)
            engine.runAndWait()
            return
        elif ext == ".html":
            with open(file_path, "r", encoding="utf-8") as f:
                html = f.read()
            soup = BeautifulSoup(html, "html.parser")
            engine.say(soup.get_text())
            engine.runAndWait()
            return
        elif ext == ".docx":
            doc = docx.Document(file_path)
            engine.say("\n".join([p.text for p in doc.paragraphs]))
            engine.runAndWait()
            return
        elif ext in [".csv", ".xlsx"]:
            if ext == ".csv":
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path) 
            engine.say(df.to_string())
            engine.runAndWait()
            return
        elif ext in [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".webp", ".heic"]:
            text = pytesseract.image_to_string(Image.open(file_path))
            engine.say(text)
            engine.runAndWait()
            return
        else:
            if ext in unsupported_extensions:
                engine.say(f"Unsupported file type: {ext}")
                engine.runAndWait()
                return
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    engine.say(f.read())
                    engine.runAndWait()
                    return
            except UnicodeDecodeError:
                with open(file_path, "r", encoding="latin-1") as f:
                    engine.say(f.read())
                    engine.runAndWait()
                    return
    else:
        return
b=tk.Button(mn,text="Choose file",command=lambda:read_file_text(),cursor="hand2")
b.place(x=200,y=75)
mn.mainloop()