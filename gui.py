import tkinter as tk
from tkinter import *
from tkinter import simpledialog
import speech_recognition as sr
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
import nltk
import playsound
import keras_nlp

translator = Translator()
mw = tk.Tk()
myquery = ''
myoption = 0

mw.title('MediBot')
#You can set the geometry attribute to change the root windows size
mw.geometry("1000x600") #You want the size of the app to be 500x500
mw.resizable(0, 0) #Don't allow resizing in the x or y direction

back = tk.Frame(mw)
#back.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
back.pack(fill=tk.BOTH, expand=1) #Expand the frame to fill the root window
background_image=tk.PhotoImage(file = 'medical.png')
background_label = tk.Label(back, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
# scrollbar = Scrollbar(back)
# scrollbar.pack(side=RIGHT, fill=Y)
# listbox = Listbox(back, bd=0, yscrollcommand=scrollbar.set)
# listbox.pack()
# scrollbar.config(command=back.yview)

class ButtonChoose:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        top.geometry("200x100")

        self.mySubmitButton = tk.Button(top, text='Yes', command=self.send)
        self.mySubmitButton.pack(side=TOP)

        self.mySubmitButton1 = tk.Button(top, text='No', command=self.send2)
        self.mySubmitButton1.pack(side=TOP)

        self.mySubmitButton2 = tk.Button(top, text='I dont know', command=self.send3)
        self.mySubmitButton2.pack(side=TOP)


    def send(self):
        global myoption
        myoption = 1
        self.top.destroy()

    def send2(self):
        global myoption
        myoption = 0
        self.top.destroy()

    def send3(self):
        global myoption
        myoption = -1
        self.top.destroy()

class MyText:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        top.geometry("500x140")

        self.myLabel = tk.Label(top, text='Please write here', font=("Courier", 15))
        self.myLabel.pack(fill=X)

        self.myEntryBox = tk.Entry(top,width=80)
        self.myEntryBox.pack(fill=X)

        self.mySubmitButton = tk.Button(top, text='Submit', command=self.send)
        self.mySubmitButton.pack()

        self.mySubmitButton = tk.Button(top, text='Record hindi', command=self.record_hindi)
        self.mySubmitButton.pack()

        self.mySubmitButton = tk.Button(top, text='Record english', command=self.record_english)
        self.mySubmitButton.pack()

    def send(self):
        global myquery
        myquery = self.myEntryBox.get()
        self.top.destroy()

    def record_hindi(self):
        global myquery
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Say Something:')
            audio = r.listen(source)
            print('Done!')
        try:
            text = r.recognize_google(audio,language='hi-IN')
            if (tk.messagebox.askquestion('Correct Type', 'Have you typed? ' + text) == 'yes'):
                myquery =  translator.translate(text,dest='en',src='hi').text
                self.top.destroy()
        except:
            tk.messagebox.showinfo("Corrupt Text","Sorry we didnt get you ")

    def record_english(self):
        global myquery
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Say Something:')
            audio = r.listen(source)
            print('Done!')
        try:
            text = r.recognize_google(audio)
            if (tk.messagebox.askquestion('Correct Type', 'Have you typed? ' + text) == 'yes'):
                myquery =  translator.translate(text,dest='en').text
                self.top.destroy()
        except:
            tk.messagebox.showinfo("Corrupt Text","Sorry we didnt get you ")



text_list = ["Hello, I am H.I.M. How can I help You? "]
label_list = []
i = 1

def chooseOption():
    global myoption
    inputDialog = ButtonChoose(back)
    back.wait_window(inputDialog.top)
    print('Choose: ', myoption)

lst=None
last_response = 'Z'
symptom_no = []
dis_lst = None
last_response_index = None

positive_wrds = ['yes','yeah','yup']
negative_wrds = ['no','not','naah','naa']

def response():
    global myquery, label_list, answer_button, i, text_list, lst, last_response, symptom_no, dis_lst, last_response_index
    inputDialog = MyText(back)
    back.wait_window(inputDialog.top)
    text_list.append(myquery)
    label_list.append(Label(back, text=text_list[-1], font=("Courier", 15), width=75, bg='light gray'))
    label_list[-1].place(x=40, y=40*i)
    answer_button.destroy()
    if( myquery == '' ):
        if(tk.messagebox.askquestion ('Exit Application','Are you sure you want to exit the application',icon = 'warning') == 'yes'):
            exit(0)
    print('Username: ', myquery)
    i += 1
    if i%12 == 0:
        for x in label_list:
            x.destroy()
        i = 1
        label_list = []
        text_list = []
    if lst is None:
        lst, dis_lst = keras_nlp.test(myquery)
        for x in lst:
            symptom_no.append(len([y for y in x if y is not None]))
    print(lst)
    if( any( x in myquery.lower().strip().split(' ') for x in positive_wrds) ):
        last_response = 'Y'
    if (any(x in myquery.lower().strip().split(' ') for x in negative_wrds)):
        last_response = 'N'
    flag = 0
    for disease in range(len(lst)):
        if( lst[disease].count('Y') / symptom_no[disease] > .8 ):
            tk.messagebox.showinfo("Final Answer", "Probably You have "+str(dis_lst[disease])+" but I am sometimes wrong. Please go to a doctor")
            myobj = gTTS(text=str(dis_lst[disease]), lang='hi', slow=False)
            myobj.save("welcome.mp3")
            playsound.playsound('welcome.mp3', True)
            exit(0)
        for symptom in range(len(lst[disease])):
            if lst[disease][symptom] is not None and lst[disease][symptom] != 'Y' and lst[disease][symptom] != 'N' :
                myquery = 'Well, have you also faced ' + lst[disease][symptom]
                print(lst[disease][symptom])
                if( last_response != 'Z'):
                    lst[disease][symptom] = last_response
                last_response_index = (disease, symptom)
                flag = 1
                break
        if( flag == 1 ):
            break
    flag = 0
    text_list.append(myquery)
    label_list.append(Label(back, text=text_list[-1], font=("Courier", 15), width=75, bg='white'))
    label_list[-1].place(x=40, y=40 * i)
    i += 1
    answer_button = tk.Button(back, text='Type Query', command=response)
    answer_button.place(x=40, y=40*i)
    #print(i)

label_list.append(Label(back, text=text_list[-1], font=("Courier", 15), width=75, bg='white'))
label_list[-1].place(x=40,y=5)
answer_button = tk.Button(back, text='Type Query', command=response)
answer_button.place(x=40,y=40)

mw.mainloop()
