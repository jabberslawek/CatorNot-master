import sqlite3


class Database:
    def __init__(self):
        self.db = sqlite3.connect("database.db")
        self.cursor = self.db.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS score(data VARCHAR(255), wynik_gospodarze INT, wynik_goscie INT)''')
    def add(self, data, gospodarze_score, goscie_score):

        self.cursor.execute('''INSERT INTO score(data, wynik_gospodarze, wynik_goscie)
                  VALUES(?,?,?)''', (data, gospodarze_score, goscie_score))
        self.db.commit()
    def show_score(self):

        self.cursor.execute('''SELECT data, wynik_gospodarze, wynik_goscie FROM score''')
        for row in self.cursor:
            print('DATA: {0} : Gospodarze {1}, Goście {2}'.format(row[0], row[1], row[2]))
