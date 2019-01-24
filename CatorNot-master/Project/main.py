from tkinter import *
from PyHook3 import HookManager, HookConstants
from tkinter.messagebox import showinfo
from random import randint
import PIL.Image
import PIL.ImageTk
from os import listdir
from os.path import isfile, join
from random import choice
from datetime import date
from Project.database import *

from Project.popupy import PopUp

class App:
    def __init__(self, root):
        self.root = root
        self.root.configure(background='purple')

        self.point_history = list()
        self.TEAM_ONE = '-1'
        self.TEAM_TWO = '1'

        self.fun_list = ''
        self.FUN_CAT = '1'
        self.FUN_NOCAT = '-1'

        self.today = str(date.today()) #data dzisiejsza
        
        #tworzy path do obrazków
        mypath = 'cats/'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        gospodarze_img = choice(onlyfiles)
        onlyfiles.remove(gospodarze_img)
        gospodarze_img_path = join(mypath, gospodarze_img)
        goscie_img_path = join(mypath, choice(onlyfiles))

        print(onlyfiles)
        #tutaj tworzą się wszystkie widgety
        #ta linijka zapewnia że okienko jest zawsze na wierzchu
        root.attributes("-topmost", True)

        root.wm_title("KotCzyNie?")
        #tutaj tworzymy fonta dla wszystkich label w __init__, można zmienić na globalną później w sumie
        font_name = 'times'
        font_size = 40
        label_font = '{0} {1}'.format(font_name, font_size)

        #HookManager odpowiada za zbieranie eventów z klawiatury gdy aplikacja jest w tle
        self.my_hook_manager = HookManager()
        self.my_hook_manager.KeyUp = self.on_keyboard_event
        self.my_hook_manager.HookKeyboard()

        #sekcja tworzenia widgetów dla gospodarzy
        gospodarze_name_string = 'Gospodarze   '
        gospodarze_name = StringVar()
        self.gospodarze_score_str = StringVar()
        self.gospodarze_score_int = 0
        gospodarze_name.set(gospodarze_name_string)
        self.gospodarze_score_str.set(str(self.gospodarze_score_int))

        gospodarze_name_label = Label(root, textvariable=gospodarze_name, font=label_font)
        gospodarze_score_label = Label(root, textvariable=self.gospodarze_score_str, font=label_font)

        #dodaje obrazek dla gospodarzy
        gospodarze_cats_picture = PIL.Image.open(gospodarze_img_path)
        gospodarze_cats_picture = gospodarze_cats_picture.resize((100, 100), PIL.Image.ANTIALIAS)
        gospodarze_cats_picture = PIL.ImageTk.PhotoImage(gospodarze_cats_picture)
        gospodarze_cat_label = Label(root, image=gospodarze_cats_picture)
        gospodarze_cat_label.image = gospodarze_cats_picture

        #separator musi mieć swój własny widget, tak chyba jest najwygodniej
        separetor_raw_string = '  -  '
        separator_tk_string = StringVar()
        separator_tk_string.set(separetor_raw_string)
        separator_label = Label(root, textvariable=separator_tk_string, font=label_font)


        #sekcja tworzenia widgetów dla gości
        goscie_name_string = '   Goście'
        goscie_name = StringVar()
        self.goscie_score_str = StringVar()
        self.goscie_score_int = 0
        goscie_name.set(goscie_name_string)
        self.goscie_score_str.set(str(self.goscie_score_int))

        #tworzenie obrazka dla gosci
        goscie_cats_picture = PIL.Image.open(goscie_img_path).transpose(PIL.Image.FLIP_LEFT_RIGHT)
        goscie_cats_picture = goscie_cats_picture.resize((100, 100), PIL.Image.ANTIALIAS)
        goscie_cats_picture = PIL.ImageTk.PhotoImage(goscie_cats_picture)
        goscie_cat_label = Label(root, image=goscie_cats_picture)
        goscie_cat_label.image = goscie_cats_picture

        goscie_name_label = Label(root, textvariable=goscie_name, font=label_font)
        goscie_score_label = Label(root, textvariable=self.goscie_score_str, font=label_font)

        gospodarze_cat_label.grid(column=0, row=0)
        gospodarze_name_label.grid(column=1, row=0)
        gospodarze_score_label.grid(column=2, row=0)

        separator_label.grid(column=3, row=0)

        goscie_score_label.grid(column=4, row=0)
        goscie_name_label.grid(column=5, row=0)
        goscie_cat_label.grid(column=6, row=0)

    def add_point_to_gospodarze(self):
        self.gospodarze_score_int += 1
        self.gospodarze_score_str.set(str(self.gospodarze_score_int))
        self.point_history.append(self.TEAM_ONE)

    def add_point_to_goscie(self):
        self.goscie_score_int += 1
        self.goscie_score_str.set(str(self.goscie_score_int))
        self.point_history.append(self.TEAM_TWO)

    def subtract_point_from_gospodarze(self):
        self.gospodarze_score_int -= 1
        self.gospodarze_score_str.set(str(self.gospodarze_score_int))

    def subtract_point_from_goscie(self):
        self.goscie_score_int -= 1
        self.goscie_score_str.set(str(self.goscie_score_int))

    def check_if_cat(self):
        #losowanie czy kot czy nie
        answer_positive = 'To jest kot'
        answer_negative = 'To nie jest kot'
        answer_string_raw = ''

        if self.fun_list == '':
            random_number = randint(1, 1000)

            if random_number <= 500:
                answer_string_raw = answer_positive
            else:
                answer_string_raw = answer_negative
        elif self.fun_list == self.FUN_CAT:
            answer_string_raw = answer_positive
        elif self.fun_list == self.FUN_NOCAT:
            answer_string_raw = answer_negative

        self.fun_list = ''

        PopUp(answer_string_raw, 1000)

    def delete_point(self):
        try:
            team = self.point_history.pop()
            if team == self.TEAM_ONE:
                self.subtract_point_from_gospodarze()
            if team == self.TEAM_TWO:
                self.subtract_point_from_goscie()
        except IndexError:
            pass

    def how_many_points(self): #zliczanie punktow
        self.goscie_points = 0
        self.gospodarze_points = 0
        for item in self.point_history:
            if int(item) == 1:
                self.goscie_points = self.goscie_points + 1
            else :
                self.gospodarze_points = self.gospodarze_points +1
        return self.gospodarze_points, self.goscie_points

    def on_keyboard_event(self, event):
        #hookmanager i jego eventy, te printy są dla debugowania, żeby wiedzieć jakie przyciski mają KeyId
        print('MessageName:', event.MessageName)
        print('Ascii:', repr(event.Ascii), repr(chr(event.Ascii)))
        print('Key:', repr(event.Key))
        print('KeyID:', repr(event.KeyID))
        print( 'ScanCode:', repr(event.ScanCode))
        print('---')
        print(self.point_history)
        print('----')
        print(self.gospodarze_score_int)

        try:
            # J
            if event.KeyID == 74:
                self.add_point_to_gospodarze()
            # L
            if event.KeyID == 76:
                self.add_point_to_goscie()
            # I
            if event.KeyID == 73:
                self.check_if_cat()
            # K
            if event.KeyID == 75:
                self.delete_point()
            # U
            if event.KeyID == 85:
                self.fun_list = self.FUN_CAT
            # O
            if event.KeyID == 79:
                self.fun_list = self.FUN_NOCAT
            # ;
            if event.KeyID == 186:
                self.fun_list = ''

            if event.KeyID == 83: #s zapis do bazy
                print(self.point_history)
                gospodarze, goscie = self.how_many_points()
                print(self.how_many_points())
                db.add(self.today, gospodarze, goscie)
            if event.KeyID == 87: # w odczyt z bazy
                db.show_score()
        finally:
            return True

db = Database()
root = Tk()
app = App(root)
root.mainloop()



