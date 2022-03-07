import tkinter as tk
from tkinter import *
import base64
from PIL import ImageTk,Image
import speech_recognition as sr
import pyttsx3
from tkinter import filedialog
import json
import requests
import wolframalpha
import pytesseract 
import urllib.request
from urllib.request import urlopen
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\Tesseract.exe'
TESSDATA_PREFIX = 'C:/Program Files (x86)/Tesseract-OCR'
converter = pyttsx3.init() 
engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
 
engine.setProperty('voice',voices[0].id)

converter.setProperty('rate',100) 
converter.setProperty('volume',.75)
app_id = "6XUGRE-3V94YQU3XV" 
root = tk.Tk()
root.title("Linear equation solver")


root.geometry("1600x800")
canvas = Canvas(root, width=800, height=600)
canvas.place(x=10, y=10)
client = wolframalpha.Client(app_id) 
def speak(text):
    engine.say(text)
    engine.runAndWait()
    
    
def takeVoiceCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=1)
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        speak("Say that again please...")  
        query=takeVoiceCommand()
    return query


def voiceCommandSolver():
    speak("speak your equation")
    query=takeVoiceCommand()
    solve(query)



def solve( output):
    # print(output)
   
    # print((','.join(output))[:-2])
    rest = client.query(output,params=(("format", "image,plaintext"),)) 
    data = {}
    try:
       for p in rest.pods:
         for s in p.subpods:
            if s.img.alt.lower() == "root plot":
              data['rootPlot'] = s.img.src
            elif s.img.alt.lower() == "number line":
              data['numberLine'] = s.img.src
            elif s.img.alt.lower()=="plot of solution set":
               data["plot"]=s.img.src   
       data['results'] = [i.texts for i in list(rest.results)][0]
    
    except:
        try:
               data['results'] = [i.texts for i in list(rest.results)][0]
        except:
               data["results"] ="Error"
    print(data) 
    if 'rootPlot' in data:
        image1_url = data['rootPlot']   
        image1_byt = urlopen(image1_url).read()
        image1_b64 = base64.encodebytes(image1_byt)
        photo1 = tk.PhotoImage(data=image1_b64)         
        canvas.photo1 = photo1
        canvas.create_image(10, 30, image=canvas.photo1, anchor='nw')
        canvas.create_text(175,40,fill="darkblue",font="Arial 10",text="graph")
    
    if 'numberLine' in data:
        image2_url = data['numberLine']
        image2_byt = urlopen(image2_url).read()
        image2_b64 = base64.encodebytes(image2_byt)
        photo2 = tk.PhotoImage(data=image2_b64)                  
        canvas.photo2 = photo2
        canvas.create_image(10, 240, image=canvas.photo2, anchor='nw')
        canvas.create_text(175,230,fill="darkblue",font="Arial 10",text="Number Line")
        
    if "plot" in data:
        image3_url=data["plot"] 
        image3_byt=urlopen(image3_url).read()
        image3_b64=base64.encodebytes(image3_byt)  
        photo3 = tk.PhotoImage(data=image3_b64)  
        canvas.photo3 = photo3
        canvas.create_image(10, 240, image=canvas.photo3, anchor='nw')
        canvas.create_text(175,230,fill="darkblue",font="Arial 10",text="intersection curve")
    canvas.create_text(175,320,fill="darkblue",font="Arial 15",text=data['results'])
    
    print(data)
     
    # print(rest.pod[2].subpod.img["@title"])
    # print(rest.pod[2].subpod.img["@src"])
def UploadAction(event=None):
 
    filename = filedialog.askopenfilename()
    output=pytesseract.image_to_string(filename)
    solve(output)
    
# def get_class():  #no need to pass arguments to functions in both cases
#     solve(var.get())

def get_entry(): 
    solve (ent.get())

# usertext =StringVar()

# usertext.set("Click Run To Give Jarvis Command")

# userFrame =LabelFrame(root ,text="User" ,font="comicsansms 10 bold")
# userFrame.pack(fill=BOTH ,expand='yes')

# message =Message(userFrame ,textvariable=usertext ,bg="#3b9895" ,fg="white")
# message.config(font="comicsansms 10 bold")
# message.pack(fill=BOTH ,expand='yes')

# button1 =Button(root ,text="Run" ,font="comicsansms 10 bold" ,bg="#4B4B4B" ,fg="white" ,command=self.clicked).pack(fill=X ,expand='no')
# button2 =Button(root ,text="Exit" ,font="comicsansms 10 bold" ,bg="black" ,fg="white" ,command=Exit).pack(fill=X,expand='no')




var = tk.StringVar()

ent = tk.Entry(root,textvariable = var)
# btn1 = tk.Button(root, text="Variable Class", command=get_class)
btn2 = tk.Button(root, text="Get Method", command=get_entry)
voiceBotton=tk.Button(root,text="Voice Command",command=voiceCommandSolver)
ent.pack()
# btn1.pack()
btn2.pack()
button = tk.Button(root, text='Take Image', command=UploadAction)
button.pack()
voiceBotton.pack()






canvas = tk.Canvas(bg='white')
canvas.config(height=600,width=1000)
canvas.pack()

root.mainloop()

    
