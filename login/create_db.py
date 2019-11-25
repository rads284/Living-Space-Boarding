import csv, sqlite3

con = sqlite3.connect("livingspace.db")
cur = con.cursor()
cur.execute('PRAGMA foreign_keys = ON')

cur.execute("CREATE TABLE IF NOT EXISTS Warden (FullName,Id,PhoneNumber,Password,Email, PRIMARY KEY(Id));") # use your column names here
with open('Warden.txt','r',encoding="utf8") as fin: 
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['FullName'], i['Id'],i['PhoneNumber'],i['Password'],i['Email']) for i in dr]
    print("HELL")

# cur.executemany("INSERT INTO Warden (FullName,Id,PhoneNumber,Password,Email) VALUES (?, ?, ?, ?, ?);", to_db)
# con.commit()
# cur = con.cursor()
# cur.execute("SELECT * FROM user;")
# print(cur.fetchone  ())
cur.execute("CREATE TABLE IF NOT EXISTS Parent (FullName,Id,Password,Email,PhoneNumber, PRIMARY KEY(Id) );") # use your column names here
with open('Parent.txt','r',encoding="utf8") as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['FullName'], i['Id'],i['Password'],i['Email'],i['PhoneNumber']) for i in dr]
cur.executemany("INSERT INTO Parent (FullName,Id,Password,Email,PhoneNumber) VALUES (?, ?, ?, ?, ?);", to_db)
con.commit()

cur.execute("CREATE TABLE IF NOT EXISTS Student(w_id,Id,FullName,p_id,PRIMARY KEY(Id), FOREIGN KEY(w_id) REFERENCES Warden(Id) ON DELETE CASCADE ON UPDATE NO ACTION,FOREIGN KEY(p_id) REFERENCES Parent(Id) ON DELETE CASCADE ON UPDATE NO ACTION);") # use your column names here
with open('Student.txt','r',encoding="utf8") as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['w_id'], i['Id'],i['FullName'],i['p_id']) for i in dr]
cur.executemany("INSERT INTO Student (w_id,Id,FullName,p_id) VALUES (?, ?, ?, ?);", to_db)
con.commit()

cur.execute("CREATE TABLE IF NOT EXISTS Leave (id,s_id,CheckIn,CheckOut,ApprovedP,ApprovedW, PRIMARY KEY(id), FOREIGN KEY(s_id) REFERENCES Student(Id) ON DELETE CASCADE ON UPDATE NO ACTION);")

row= ('79485565','99', '19-11-2019', '21-11-2019', 'Yes', 'No')

cur.execute("INSERT INTO Leave (id,s_id,CheckIn,CheckOut,ApprovedP,ApprovedW) VALUES(?,?,?,?,?,?);",row)
# Insert only when student is absent.
cur.execute("CREATE TABLE IF NOT EXISTS Attendance (CDate, s_id, PRIMARY KEY(CDate,s_id), FOREIGN KEY(s_id) REFERENCES Student(Id) ON DELETE CASCADE ON UPDATE NO ACTION)")
con.commit()
con.close()