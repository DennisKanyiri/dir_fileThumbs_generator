from tkinter import *
from PIL import ImageTk, Image
import os, _thread
import time

root = Tk()
bt = Button(root, font = ('times', 20), fg = 'red')
bt.pack(expand = NO)

fr = Frame(root)
fr.pack(fill = BOTH, expand = YES)
scl = Scrollbar(fr, width = 10)
scl.pack(side = RIGHT, fill = Y)
canv = Canvas(fr)
canv.pack(fill = BOTH, expand = YES)
canv.config(yscrollcommand = scl.set)
scl.config(command = canv.yview)

dir = r'F:\MultiMedia\Music\Music\Mp3Juice'
thumbs = [x for x in os.listdir(dir)]
ls = []
os.chdir(dir)
lock = True
mutex = _thread.allocate_lock()
itemsno = 0
thumb_size = (100, 80)

icon = "C:\\Users\\DennisKK\\Desktop\\SecProject\\AppIcons\\istockphoto-1049430556-1024x1024.jpg"
mimg = Image.open(icon)
mimg.thumbnail(thumb_size)
musico = ImageTk.PhotoImage(mimg)
mutex = _thread.allocate_lock()

def child(thds, myportion):
    global lock, itemsno
    if not myportion:return None
    for item in myportion:
        if (os.path.splitext(item)[1] == '.jpg' or
            os.path.splitext(item)[1] == '.png' or
            os.path.splitext(item)[1] == '.jpeg'):
            img = Image.open(item)
            #img = img.rotate(-90)
            img.thumbnail(thumb_size, resample = Image.Resampling.BILINEAR)
            photo = ImageTk.PhotoImage(image = img)
            #print(f"child: {thds} got: {img}")
            mutex.acquire()
            ls.append(photo)
            mutex.release()
            itemsno += 1

        elif (os.path.splitext(item)[1] == '.mp3' or
            os.path.splitext(item)[1] == '.m4a'):
            mutex.acquire()
            ls.append(musico)
            print('music created')
            mutex.release()
            itemsno += 1
        else:pass

threads = 0
stop = 10
start = 0
cons = 10
no_threads = len(os.listdir(dir))/cons

for x in range(int(no_threads)):
    myportion = thumbs[start:stop]
    _thread.start_new_thread(child, (threads, myportion))
    start += cons
    stop += cons
    print(f"parent creating thread: {threads}")
    #ls.append(f'parent initiating thread: {threads}')
    threads += 1

row = 100
column = 0
window_width = canv.winfo_width()
thumb_width = thumb_size[0]

def consumer():
    #print('print(item)')
    global row, column
    for itm in ls:
        fr1 = Frame(canv, width = 200, height = 300)
        fr1.pack()
        bt = Button(fr1, image = itm, bd = 2, relief = 'flat', bg = 'white')
        bt.pack(side = TOP, expand = NO)
        lb = Label(fr1, text = "image")
        lb.pack(side = BOTTOM, expand = YES, fill = X)
        canv.create_window(column, row, window = fr1)
        column += 150
        if column >= window_width:
            column = 0
            row += 100
            
    #print(itemsno)

#current_width = 150
def on_resize():
    global window_width
    global column, row
    width = canv.winfo_width() #height = canv.winfo_height()
    displacement = width - window_width
    print(f"width = {width},\ndisplacement = {displacement}")
    if displacement >= thumb_width:
        window_width = width
        canv.delete('all')
        column = 0 
        row = 100
        consumer()
        print('+ve block')
    elif thumb_width >= displacement:
        window_width = width
        canv.delete('all')
        column = 0 
        row = 100
        consumer()
        print('-ve block')

bt.config(command = lambda: _thread.start_new_thread(consumer, ()), text = 'images')
canv.config(scrollregion = (0, 0, row, 1000))
#fr.bind("<Configure>", lambda event: on_resize())
root.wm_minsize(width = 400, height =250)
#root.protocol("WM_DELETE_WINDOW", root.destroy)
root.mainloop()