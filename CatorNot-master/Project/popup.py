from tkinter import *


class PopUp:
    def __init__(self, message, timer):
        #chyba mamy nasz pierwszy legacy code, zajebałem wszystko z neta i nie wiem co do czego służy xD
        win = Toplevel()
        win.wm_title("Window")
        win.resizable(False, False)
        win.overrideredirect(True)
        win.attributes("-topmost", True)
        win.configure(background='pink')
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(500, 100, x, y))
        win.deiconify()

        message_label = Label(win, text=message, font='times 40', background='pink')
        message_label.pack()

        win.after(timer, lambda: win.destroy())
        win.mainloop()


if __name__ == '__main__':
    PopUp('test', 4000)