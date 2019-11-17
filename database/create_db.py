import csv, sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE Warden (FullName,Id,PhoneNumber,Password,Email, PRIMARY KEY(Id));") # use your column names here
with open('User_Parent.csv','r',encoding="utf8") as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['FullName'], i['Id'],i['PhoneNumber'],i['Password'],i['Email']) for i in dr]
cur.executemany("INSERT INTO Warden (FullName,Id,PhoneNumber,Password,Email) VALUES (?, ?, ?, ?, ?);", to_db)
con.commit()
# cur = con.cursor()
# cur.execute("SELECT * FROM user;")
# print(cur.fetchone  ())

cur.execute("CREATE TABLE Student(w_id,Id,FullName, FOREIGN KEY(w_id) REFERENCES Warden(Id) ON DELETE CASCADE ON UPDATE NO ACTION);") # use your column names here
with open('Student.txt','r',encoding="utf8") as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['w_id'], i['Id'],i['FullName']) for i in dr]
cur.executemany("INSERT INTO Student (w_id,Id,FullName) VALUES (?, ?, ?);", to_db)
con.commit()

cur.execute("CREATE TABLE Parent (FullName,Id,s_id,Password,Email,PhoneNumber, PRIMARY KEY(Id), FOREIGN KEY(s_id) REFERENCES Student(Id) ON DELETE CASCADE ON UPDATE NO ACTION );") # use your column names here
with open('Parent.txt','r',encoding="utf8") as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['FullName'], i['Id'],i['s_id'],i['Password'],i['Email'],i['PhoneNumber']) for i in dr]
cur.executemany("INSERT INTO Parent (FullName,Id,s_id,Password,Email,PhoneNumber) VALUES (?, ?, ?, ?, ?, ?);", to_db)
con.commit()

cur.execute("CREATE TABLE Leave (id,s_id,w_id,p_id,CheckIn,CheckOut,ApprovedP,ApprovedW, PRIMARY KEY(id), FOREIGN KEY(s_id) REFERENCES Student(Id) ON DELETE CASCADE ON UPDATE NO ACTION, FOREIGN KEY(w_id) REFERENCES Warden(Id) ON DELETE CASCADE ON UPDATE NO ACTION, FOREIGN KEY(p_id) REFERENCES Parent(Id) ON DELETE CASCADE ON UPDATE NO ACTION );") # use your column names here
con.commit()
# Insert only when student is absent.
cur.execute("CREATE TABLE Attendance (CDate, s_id, PRIMARY KEY(CDate,s_id), FOREIGN KEY(s_id) REFERENCES Student(Id) ON DELETE CASCADE ON UPDATE NO ACTION)")
con.commit()
con.close()