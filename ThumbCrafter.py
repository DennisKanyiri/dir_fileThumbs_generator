from tkinter import *
from PIL import ImageTk, Image
import os, _thread

root = Tk()
bt = Button(root, font = ('times', 20), fg = 'red')
#bt.pack(expand = NO)

fr = Frame(root, bg = 'white')
fr.pack(fill = BOTH, expand = YES)
scl = Scrollbar(fr, width = 10)
scl.pack(side = RIGHT, fill = Y)
canv = Canvas(fr, bg = 'white')
canv.pack(fill = BOTH, expand = YES)
canv.config(yscrollcommand = scl.set)
scl.config(command = canv.yview)

dir = r'C:\Users\DennisKK\Pictures\WallPps\psonal'
thumbs = [x for x in os.listdir(dir)]
ls = []
os.chdir(dir)
lock = True
mutex = _thread.allocate_lock()
itemsno = 0
thumb_size = (100, 80)

icon = "C:\\Users\\DennisKK\\Desktop\\SecProject\\AppIcons\\istockphoto-967022412-1024x1024.jpg"
mimg = Image.open(icon)
mimg.thumbnail(thumb_size)
name_val = {}
musico = ImageTk.PhotoImage(mimg)
mutex = _thread.allocate_lock()

def file_handler(file):
    abs_file = os.path.join(dir, file)
    os.startfile(abs_file)

def on_mouse_wheel(event):
    # Scroll canvas by the amount of wheel movement
    canv.yview_scroll(int(-1*(event.delta/120)), "units")


def child(mynum, myportion):
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
            print(f"child: {mynum} got: {img}")
            #mutex.acquire()
            name_val[item] = photo
            #mutex.release()
            itemsno += 1

        elif (os.path.splitext(item)[1] == '.mp3' or
            os.path.splitext(item)[1] == '.m4a'):
            #mutex.acquire()
            name_val[item] = musico
            print('music created')
            #mutex.release()
            itemsno += 1
            
        else:pass

threadnum = 0
stop = 10
start = 0
cons = 10
no_threads = len(os.listdir(dir))/cons

for x in range(int(no_threads)):
    myportion = thumbs[start:stop]
    _thread.start_new_thread(child, (threadnum, myportion))
    start += cons
    stop += cons
    print(f"parent creating thread: {threadnum}")
    #ls.append(f'parent initiating thread: {threads}')
    threadnum += 1

row = 100
column = 0
window_width = canv.winfo_width()
thumb_width = thumb_size[0]

def consumer():
    #print('print(item)')
    global row, column
    for key, val in name_val.items():
        fr1 = Frame(canv, bg = 'white')
        fr1.pack()
        bt = Button(fr1, image = val, bd = 2, relief = 'flat', bg = 'white')
        bt.config(command = lambda val = key:file_handler(val))
        bt.pack(side = TOP, expand = NO)
        lb = Message(fr1, text = key, bg = 'white')
        lb.pack(side = BOTTOM, expand = YES, fill = X)
        canv.create_window(column, row, window = fr1)
        column += 150
        if column >= window_width:
            column = 0
            row += 200
            
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

#bt.config(command = test, text = 'images')
canv.config(scrollregion = (0, 0, 20000, 1000))
fr.bind("<Configure>", lambda event: on_resize())
root.wm_minsize(width = 400, height =250)
canv.bind_all("<MouseWheel>", on_mouse_wheel)
root.mainloop()
