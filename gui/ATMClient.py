import sys
import PySimpleGUI as sg

sys.path.append("../domain")
from account import *
from customer import *
import tkinter as tk
from tkinter.simpledialog import askinteger


def conndb(dbfile):
    import sqlite3
    conn = sqlite3.connect(dbfile)  # 创建或打开dbfile
    curs = conn.cursor()
    return conn, curs


class Login(tk.Toplevel):  # 弹窗
    def __init__(self):
        super().__init__()
        self.title('登录')
        self.setup_UI()

    def setup_UI(self):
        row1 = tk.Frame(self)
        row1.pack(fill="x")
        tk.Label(row1, text='卡号', width=14).pack(side=tk.LEFT)
        self.card = tk.StringVar(value='')#初始化卡号
        tk.Entry(row1, textvariable=self.card, width=20).pack(side=tk.LEFT)

        row2 = tk.Frame(self)
        row2.pack(fill="x", ipadx=1, ipady=1)
        tk.Label(row2, text='密码', width=14).pack(side=tk.LEFT)
        self.pw = tk.IntVar(value='123456')#初始化密码
        tk.Entry(row2, text='', textvariable=self.pw, show='*', width=20).pack(side=tk.LEFT)

        row3 = tk.Frame(self)
        row3.pack(fill="x")
        tk.Button(row3, text="取消", command=self.cancel).pack(side=tk.RIGHT)
        tk.Button(row3, text="确定", command=self.ok).pack(side=tk.RIGHT)

    def ok(self):
        self.userinfo = [self.card.get(), self.pw.get()]
        self.destroy()

    def cancel(self):
        self.userinfo = None
        self.destroy()


# 主窗
class ATM(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('用户信息')
        # 程序参数/数据
        self.card = ''
        self.pw = 30
        # 程序界面
        self.conn, self.curs = conndb('../data/bankdb')
        self.setupUI()
        self.enable_btns('disabled')
        self.setup_config()

    def setupUI(self):
        rows = []
        self.btns = []
        for i in range(6):
            rows.append(tk.Frame(self))
            rows[i].pack(side=tk.TOP)
        btn_txts = ['个人信息', '余额查询', '存钱', '取钱', '退出登录']
        btn_commands = [self.imformation, self.get_balance, self.deposite, self.withdraw, self.logout]
        for i in range(5):
            self.btns.append(tk.Button(rows[i], text=btn_txts[i], command=btn_commands[i], width=12))
            self.btns[i].pack(side=tk.LEFT)
        self.statusLabel = tk.Label(rows[5], text='', width=40)
        self.statusLabel.pack(side=tk.LEFT)

    def enable_btns(self, stat):
        for i in range(5):
            self.btns[i].config(state=stat)

    def imformation(self):#自定义的读取显示用户对应个人信息的功能模块
        self.curs.execute('select balance from account where card_id =' +str(self.account.ID))
        self.statusLabel.config(text='姓名：' + str(self.customer) + '   ' + '性别：' + self.customer.getSex() + '   ' + '民族：' + self.customer.getMinzu())

    def get_balance(self):
        self.curs.execute('select balance from account where card_id = ' + str(self.account.ID))
        self.statusLabel.config(text='您的账户余额为：' + str(self.account.getBalance()))

    def deposite(self):
        try:
            amount = askinteger('存款', '输入存款金额:')
            if amount:
                self.account.deposit(amount)
                altstr = 'update account set balance =' + str(self.account.getBalance()) + ' where card_id =' + str(
                    self.account.ID)
                self.curs.execute(altstr)
                self.conn.commit()

                # 自定义的进度条显示窗口，运用PySimpleGUI库
                for i in range(1000):
                    sg.one_line_progress_meter(
                        '正在存入您的账户，请稍后...',
                        i+1,
                        1000,
                        orientation='h',
                        bar_color=('green', 'white'),
                    )
                sg.popup_auto_close('成功存入！',auto_close_duration=1)
                self.statusLabel.config(text="您的" + str(amount) + "元已成功存入！")
        except:
            self.statusLabel.config("请输入正确数据!")

    def withdraw(self):
        try:
            amount = askinteger('取款', '输入取款金额:')
            if amount:
                try:
                    self.account.withdraw(amount)
                    altstr = 'update account set balance = ' + str(
                        self.account.getBalance()) + ' where card_id = ' + str(
                        self.account.ID)
                    self.curs.execute(altstr)
                    self.conn.commit()

                    #自定义的进度条显示窗口，运用PySimpleGUI库
                    for i in range(500):
                        sg.one_line_progress_meter(
                            '正在取钱并结算余额，请稍后...',
                            i + 1,
                            500,
                            orientation='h',
                            bar_color=('red', 'white'),
                        )
                    sg.popup_auto_close('成功取出！', auto_close_duration=1)

                    self.statusLabel.config(text="您的" + str(amount) + "元已成功取出")
                except OverdraftException:
                    self.statusLabel.config(text="余额不足!")
        except:
            self.statusLabel.config("请输入正确数据！")

    def logout(self):#自定义的退出登录(退出当前账户，返回登录其他账户)功能模块
        sg.popup_auto_close('谢谢使用！', auto_close_duration=1.5)
        self.userinfo = None
        self.destroy()
        app = ATM()
        app.mainloop()#等价 self.__init__(); self.setupUI(); self.OK(); self.cancle()


    def setup_config(self):
        info = self.ask_userinfo()
        self.card, self.pw = info
        if self.card and self.pw:
            print('select * from account where card_id = ' + str(self.card) + ' and pw = ' + str(self.pw))
            self.curs.execute('select * from account where card_id = ' + str(self.card) + ' and pw = ' + str(self.pw))
            rec = self.curs.fetchone()
            if rec:
                firstname, lastname = rec[4].split(' ')
                sex = rec[5]
                minzu = rec[6]#定义新建数据库变量
                self.customer = Customer(firstname, lastname, sex, minzu)
                card_id, balance = rec[0], rec[3]
                if rec[2] == 's' or rec[2] == 'S':
                    self.account = SavingAccount(card_id, balance)
                elif rec[2] == 'c' or rec[2] == 'C':
                    self.account = CheckingAccount(card_id, balance, 6000)###################################参数三 自定义信用额度
                else:
                    self.statusLabel.config(text='非法账户')

                #sg.popup_auto_close('登录成功！')
                sg.popup_auto_close('欢迎回来！'+ str(self.customer), auto_close_duration=1)
                #self.statusLabel.config(text='欢迎回来! ' + str(self.customer))
                self.enable_btns('normal')  #用处???????
            else:
                self.statusLabel.config(text='卡号或密码错误，请重新输入!')
                self.setup_config()
        else:
            self.statusLabel.config(text='请输入卡号!')
            self.setup_config()

    def ask_userinfo(self):
        inputDialog = Login()
        self.wait_window(inputDialog)
        return inputDialog.userinfo

if __name__ == '__main__':
    app = ATM()
    app.mainloop()
