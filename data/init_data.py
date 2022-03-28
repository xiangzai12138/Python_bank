import sqlite3

conn = sqlite3.connect('bankdb')  # create or open db file
curs = conn.cursor()  # account表中存放用户卡号、密码、账户类型（储蓄/信用用户）、姓名、等信息
tblcmd = "create table if not exists account (card_id char(6),pw char(6),card_type char（1）,balance int(8),customer char(30),sex char(30),minzu char(30))"
curs.execute(tblcmd)
curs.executemany('insert into account values (?,?,?,?,?,?,?)',
                 [('1', '123456', 'S', 700000, '张 三', '男', '汉族'),
                  ('2', '123456', 'S', 600000, '王 老五', '男', '汉族'),
                  ('3', '123456', 'C', 0, '李 四', '女', '回族')])
conn.commit()
curs.close()
conn.close()