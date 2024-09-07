#DEVELOPED BY <PRIYANSHUL SHARMA>
#Webpage Priyanshul.is-a.dev
#Contact piyanshul1307@gmail.com
from tkinter import *
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import random



window= Tk()
window.title("Chatbot")
bubbles = [] #empty list to store all instances of chat bubble (message)

#creating canvas for adding controls
canvas = Canvas(window, width=350, height=500,bg="sky blue")
canvas.grid(row=0,column=0,columnspan=3)


bot=ChatBot("bot",logicAdp=["chatterbot.logic.BestMatch"])
#first lest train our bot with some data
trainer=ListTrainer(bot)
#default respnce
def_res=open("default_response.txt","r").readlines()
#train using some selected conversation statement
files=["chat.txt","mickey.txt"]
for file in files:
    conversation=open(file,"r").readlines()

    trainer.train(conversation)
    
#-------------------------------------------------------------------------------------
#creating chatbubble
class chatBubble:
    def __init__(self,master,user,message=""):
        #user 1 is bot
        if user==1:
            colour="SpringGreen2"
            x=50
            y=450
            col=1
        else:#human
            colour="coral"
            x=200
            y=450
            col=2

        #activating master object for main window
        self.master=master
        #bubble formed by label+triangle at its bottom left corner
        #frame has label and window
        self.frame=Frame(master)
        
        lbl=Label(self.frame,text=message,bg=colour,wraplength=600,anchor=W)
        lbl.pack()#add the control to canvas
        self.window=self.master.create_window(x,y,anchor=SW,window=self.frame)#placeing canvas on window

        #window has triangel se
        self.master.create_polygon(self.draw_triangle(self.window),fill=colour)

    def draw_triangle(self,widget):
        x1,y1,x2,y2=self.master.bbox(widget)#boundbox return the xy pos of bound box

        return x1, y2 - 15, x1 - 25, y2 + 10, x1, y2

def send_message(user,message):
    if bubbles:
        #move the existing bubbles upward
        canvas.move(ALL,0,-35)
    a=chatBubble(canvas,user,message)   
    bubbles.append(a)

name=""
def send():
    global name#global is acces specifier we can use name variabel in programe
    message=entry.get()
    send_message(2,entry.get())
    entry.delete(0,END)
    #assuming first responce from user will be name once bot asked for it
    if name =="":
        name=message
        send_message(1,"hello "+name+" how are you doing")
    else:
        if message.strip().lower()!="bye":
            reply=bot.get_response(message)
            if reply.confidence<0.1:
                send_message(1,random.choice(def_res).strip())
            else:
                send_message(1,str(reply).strip())
        else:
            send_message(1,"nice talking to you")
            send_message(1,"BYE")
            
#bot starts the conversation
send_message(1,"Welcome")
send_message(1,"what is your name")
            
entry = Entry(window,width=50)
entry.grid(row=1,column=0,columnspan=2)
Button(window,text="Send",width=5,command=send).grid(row=1,column=2)
window.mainloop()
