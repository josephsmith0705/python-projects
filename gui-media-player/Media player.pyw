from pygame import mixer  #Imports the module mixer from pygame, which will be used to play the music
from tkinter import filedialog #Imports the module filedialog from tkinter, which handles selecting a file manually
from tkinter import *
import mutagen #Imports the module we will use for handling audio file metadata

class Player:
    def __init__(self, master):
        self.master=master #Sets the 'master' (main) window of the program
        global pauseText
        global muteText
        global songName #Makes the variable global, so it can be manipulated outside of the class
        global songLength
        muteText = StringVar() #Specifies these variables are Tkinter variables, so they can be used within labels and buttons
        pauseText = StringVar()
        songName = StringVar()
        songLength = StringVar()
        muteText.set("🔇")
        pauseText.set("⏸")
        self.master.title("Media Player") #Sets the title of the window
        self.master.configure(background="#FFEDF2")
        self.button=Button(text="📁", command=browseFile, font="verdana", bg="#F23269", fg="white", activebackground="#FF497D", activeforeground="white", height=1, width=6, bd=0, highlightthickness=5) #Creates the browse button
        self.button.place(relx=0.025, rely=0.5, anchor=W)#positions the button centre-left
        self.button=Button(textvariable=muteText, command=mute, font="verdana", bg="#F23269", fg="white", activebackground="#FF497D", activeforeground="white", height=1, width=6, bd=0, highlightthickness=5) #Creates the browse button
        self.button.place(relx=0.975, rely=0.5, anchor=E)#positions the button centre-left
        self.button=Button(textvariable=pauseText, command=pauseToggle, font="verdana 20", bg="#F23269", fg="white", activebackground="#FF497D", activeforeground="white", height=1, width=4, highlightthickness=6, bd=0)
        self.button.place(relx=0.5, rely=0.5, anchor=CENTER) #positions the button centre
        self.button=Button(text="+", command=volumeUp, font="verdana", bg="#F23269", fg="white", activebackground="#FF497D", activeforeground="white", height=1, width=6, bd=0)
        self.button.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.button=Button(text="-", command=volumeDown, font="verdana", bg="#F23269", fg="white", activebackground="#FF497D", activeforeground="white", height=1, width=6, bd=0)
        self.button.place(relx=0.5, rely=0.7, anchor=CENTER)
        self.label=Label(textvariable=songName, font="verdana", bg="#FFEDF2")
        self.label.place(relx=0.5, rely=0.1, anchor=CENTER)
        
def browseFile(): #Creates a function for browseFile
    global musicRunning
    fileName = filedialog.askopenfilename(filetypes = (("mp3 files",".mp3"),("wav files",".wav"))) #Opens a file dialog that allows the user to select mp3 or wav files
    try: #Tries to load fileName
        mixer.music.load(fileName) #Loads the fetched file into the mixer
        mixer.music.play()
        musicRunning=True
        metadata=mutagen.File(fileName, easy=True) #Fetches the metadata of the audio file into a dictionary
        artist=str(metadata['artist'])[2:-2]
        title=str(metadata['title'])[2:-2]#Fetches the variables from the dictionary, and slices the first and last 2 characters - as these are the square brackets
        songName.set(artist+" - "+title) #Sets the song name as these new variables
    except: #If the program can't load the file, this may be because the user has cancelled the file dialog box. So, allow this error.
        pass

def pauseToggle():
    global musicRunning
    global fileName
    if musicRunning==True:
        mixer.music.pause()
        musicRunning=False
        pauseText.set("►")
    elif musicRunning==False: 
        mixer.music.unpause()
        musicRunning=True
        pauseText.set("⏸")

def volumeUp():
    volume=mixer.music.get_volume()
    volume=volume+0.1
    mixer.music.set_volume(volume)

def volumeDown():
    volume=mixer.music.get_volume() 
    volume=volume-0.1
    mixer.music.set_volume(volume)

def mute():
    global volume
    global musicMuted
    if musicMuted==True:
        mixer.music.set_volume(volume)
        musicMuted=False
        muteText.set("🔇")
    elif musicMuted==False: 
        volume=mixer.music.get_volume()
        mixer.music.set_volume(0)
        musicMuted=True
        muteText.set("🔊")

musicMuted=False #Creates the variable to tell if the music is muted or not, and sets it as false
musicRunning=False
mixer.init() #Initialises the mixer    
root = Tk() #Creates the Tkinter window
root.geometry("300x220") #Specifies the window size
app = Player(root) #Creates the instance of Tkinter
root.resizable(0,0) #Removes the maximise button
browseFile() #Runs the browseFile method
root.mainloop() #Opens the Tkinter window


