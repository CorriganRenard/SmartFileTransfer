
#import necessary modules
from datetime import datetime, timedelta, time
from tkinter import * 
from tkinter import messagebox
from tkinter import filedialog
import sqlite3
import shutil
import os

#create connection and cursor
conn = sqlite3.connect('file_transfer.db')
c = conn.cursor()

#create new table if it does not exist already
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS transfer_time(ROWID integer primary key, transfer_at TEXT)')
    conn.commit()
    c.execute('SELECT transfer_at FROM transfer_time')
    data = c.fetchone()
    last_db_time = data
    if last_db_time == None: 
        today_time = datetime.today()
        time_delay = timedelta(days=1)
        current_time = today_time - time_delay
        c.execute('INSERT INTO transfer_time(transfer_at) VALUES(?)',(current_time,))
        conn.commit()
   

#function to update table with current time from move_files function
def update_table():
    current_time = datetime.today()
    c.execute('INSERT INTO transfer_time(transfer_at) VALUES(?)',(current_time,))
    conn.commit()



#create window
win = Tk()
#declare source and dest variables
source = "C://"
dest = "C://"


#create table in db
create_table()


#get current database time for last transfer
c.execute('SELECT transfer_at FROM transfer_time')
data = c.fetchone()
last_db_time = data

#function to get last transfer time from database and assign it to global variable last_db_time
def select_table():
    global last_db_time
    #sql to select latest row from db
    c.execute('SELECT transfer_at FROM transfer_time ORDER BY ROWID DESC LIMIT 1')
    #sent the row to variable 'data'
    data = c.fetchone()
    #convert the retrieved tuple into datetime with strptime constructor
    dt = datetime.strptime(data[0], "%Y-%m-%d %H:%M:%S.%f")
    #assign this time to the global variable last_db_time
    last_db_time = dt


select_table()

#function to open folder dialog and set global source variable to selected folder
def src_dialog():
    global source
    global win
    source = filedialog.askdirectory(parent=win, initialdir="C:/Users/Cory/Desktop", )
    #refresh the window to show current folder path
    win.destroy()
    win = Tk()
    main_gui_setup()
 
#function to open folder dialog and set global dest variable to selected folder
def dest_dialog():
    global dest
    global win
    dest = filedialog.askdirectory(parent=win, initialdir="C:/Users/Cory/Desktop")
    #refresh the window to show current folder path
    win.destroy()
    win = Tk()
    main_gui_setup()

#Set up the tkinter GUI
def main_gui_setup():

    w = 400 # width for the Tk window
    h = 150 # height for the Tk window

    # get screen width and height
    ws = win.winfo_screenwidth() # width of the screen
    hs = win.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    win.geometry('%dx%d+%d+%d' % (w, h, x, y))

    #make frame1 and insert label
    frame1 = Frame(win)
    frame1.pack()
    Label(frame1, text="Choose your source and destination folders, then click 'Move Files'.").grid(row=1, column=0, sticky=W)
    
    #make frame2
    frame2 = Frame(win)
    frame2.pack()
   
    #create label to show last transfer date and time
    Label(frame2, text="Last Transfer:").grid(row=2, column=0, sticky=E)
    last_modified_label = Label(frame2, text=last_db_time)
    last_modified_label.grid(row=2, column=1, sticky=E)
    
    #Create labels to show the current filepath for the move_files function
    src_label = Label(frame2, text=source)
    dest_label = Label(frame2, text=dest)
    #pack filespath labels
    src_label.grid(row=4, column=1, sticky=W)
    dest_label.grid(row=5, column=1, sticky=W)

    #creat buttons for move, set source and set dest functions
    b = Button(frame2, text = 'Move Files', command=move_files)
    b_get_source = Button(frame2, text = "Set Source Folder", command=src_dialog)
    b_get_dest = Button(frame2, text = "Set Destination Folder", command=dest_dialog)

    #pack buttons
    b.grid(row=3, column=0, columnspan=2)
    b_get_source.grid(row=4, column=0, sticky=E)
    b_get_dest.grid(row=5, column=0, sticky=E)
  
    #loop through the window waiting for button press
    win.mainloop()


#function to move files 
def move_files():
    
    #globalize last_db_time variable to allow modification by this function
    global last_db_time
    #set file transfer counter to 0
    counter = 0
    #set the current time
    
    
    # set previous transfer as the time cutoff

    last_time = last_db_time
    
    #update the database with the current file transfer time
    update_table()
    
    #change working directory to c:\\ 
    os.chdir('C:\\')
       
    #using os.listdir make a list of the items in the source folder and loop through
    #each item, moving it to the destination folder 
    try:
        
        for file in os.listdir(source):          
            #get mod time for each file
            mtime = os.path.getmtime(source + '\\' + file)
            last_modified_date = datetime.fromtimestamp(mtime)
            #compare file times to last transfer time
            if last_modified_date > last_time and file.endswith('.txt'):
                #move files from source to dest
                shutil.move(source +'\\'+ file,dest)
                print(file + ' was transferred')
                counter += 1 #count each file
        #set the last_db_time variable to the new time
        select_table()
    except FileNotFoundError: 
        messagebox.showinfo("Transfer Error!", 'There was an error processing the files: \n File not found.')
    
    #messagebox how many files were moved
    messagebox.showinfo("Transfer complete!", str(counter)+ ' files moved successfully!')
    
    #refresh the window to show new time
    global win
    win.destroy()
    win = Tk()
    main_gui_setup()




#create main GUI
main_gui_setup()