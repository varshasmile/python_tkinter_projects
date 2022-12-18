# Importing all the necessary libraries and modules:
from tkinter import *
import tkinter.messagebox as mb

from path import Path
from PyPDF4.pdf import PdfFileReader as PDFreader, PdfFileWriter as PDFwriter
import pyttsx3
from speech_recognition import Recognizer, AudioFile
from pydub import AudioSegment
import os

# Creating the Window class and the constructor method:
class Window(Tk):
    def __init__(self):
        super(Window, self).__init__()
        self.title('VB PDF 2 Audio | Audio 2 Text Converter')
        self.geometry('400x250')
        self.resizable(0, 0)
        self.config(bg='#3a8cde')

        Label(self, text='VB PDF 2 Audio | Audio 2 Text Converter', wraplength=400, bg='#3a8cde', font=('Comic sans MS', 15)).place(x=0, y=0)

        Button(self, text='Convert PDF 2 Audio', font=('Comic Sans MS', 15), bg='Tomato', command=self.pdf_2_audio, width=25).place(x=40, y=80)
        Button(self, text='Convert Audio 2 PDF', font=('Comic Sans MS', 15), bg='White', command=self.audio_2_pdf, width=25).place(x=40, y=150)
    
    # Creating the GUI windows for the conversions as methods of the class:
    def pdf_2_audio(self):
        p2a = Toplevel(self)                  #Toplevel widget is used to create a window on top of all other windows
        p2a.title('Convert PDF 2 Audio')
        p2a.geometry('500x300')
        p2a.resizable(0, 0)
        p2a.config(bg='Chocolate')

        Label(p2a, text='Convert PDF 2 Audio', font=('Comic Sans MS', 15), bg='Chocolate').place(relx=0.3, y=0)

        Label(p2a, text='Enter the PDF file location (with extension): ', bg='Chocolate', font=('Verdana', 11)).place(x=0, y=0)
        filename = Entry(p2a, width=32, font=('Verdana', 11))
        filename.place(x=10, y=90)

        Label(p2a, text='Enter the page to read from the PDF (only one page can be read): ', bg='Chocolate', font=('Verdana', 11)).place(x=10, y=140)
        page = Entry(p2a, width=15, font=('Verdana', 11))
        page.place(x=10, y=170)

        Button(p2a, text='Speak the text!', font=('Gill Sans MT', 12), bg='Snow', width=20, command=lambda: self.speak_text(filename.get(), page.get())).place(x=150, y=240)

        
    def audio_2_pdf(self):
        a2p = Toplevel(self)
        a2p.title('Convert Audio 2 PDF')
        a2p.geometry('675x300')
        a2p.resizable(0, 0)
        a2p.config(bg='FireBrick')

        Label(a2p, text='Convert Audio 2 PDF', font=('Comic Sans MS', 15), bg='FireBrick').place(relx=0.30, y=0)
        
        Label(a2p, text='Enter the AudioFile locatipn that you want to read (in .wav or .mp3 extensions only): ', bg='FireBrick', font=('Verdana', 11)).place(x=20, y=60)
        audiofile = Entry(a2p, width=58, font=('Verdana', 11))
        audiofile.place(x=20, y=90)

        Label(a2p, text='Enter the PDF file location that you want to save the text in (with extension): ', bg='FireBrick', font=('Verdana', 11)).place(x=20, y=140)
        pdffile = Entry(a2p, width=58, font=('Verdana', 11))
        pdffile.place(x=20, y=170)

        Button(a2p, text='Create PDF', bg='Snow', font=('Gill Sans MT', 12), width=20, command=lambda: self.speech_recognition(audiofile.get(), pdffile.get())).place(x=247, y=230)


    # Creating the conversion methods:
    @staticmethod
    def speak_text(filename, page):
        if not filename or not page:
            mb.showerror('Missing field!', 'Please Check your responsee, because one of the fields is missing')      #messagebox
            return

        reader = PDFreader(filename)
        engine = pyttsx3.init()           #init function to get an engine instance for the speech synthesis

        with Path(filename).open('rb'):
            page_2_read = reader.getPage(int(page)-1)
            text = page_2_read.extractText()

            engine.say(text)
            engine.runAndWait()

    @staticmethod
    def write_text(filename, text):
        writer = PDFwriter()
        writer.addBlankPage(72, 72)

        pdf_path = Path(filename)

        with pdf_path.open('ab') as output_file:
            writer.write(output_file)
            output_file.write(text)

    def speech_recognition(self, audio, pdf):
        if not audio or not pdf:
            mb.showerror('Missing Field!', 'Please check your responses, because one of the fields is missing!')
            return
        
        audio_file_name = os.path.basename(audio).split('.')[0]
        audio_file_extension = os.path.basename(audio).split('.')[1]

        if audio_file_extension != 'wav' and audio_file_extension != 'mp3':
            mb.showerror('Error!', 'The format of the audio file should only be either "wav" or "mp3"!')

        if audio_file_extension == 'mp3':
            audio_file = AudioSegment.from_file(Path(audio), format='mp3')
            audio_file.export(f'transcript.wav', format='wav')

        source_file = 'transcript.wav'

        r = Recognizer()
        with AudioFile(source_file) as source:
            
            r.pause_threshold = 5
            speech = r.record(source)
            print(type(speech))

            text = r.recognize_google(speech)

            self.write_text(pdf, text)

# Finalizing the GUI window
app = Window()

app.update()
app.mainloop()

