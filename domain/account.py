import sys

sys.path.append("../domain")  # 添加路径，方便导入其他文件夹下的模板，下同
from OverdraftException import *


# Account类定义查询余额，存款和收款基本操作
class Account:
    def __init__(self, ID, initBalance):
        self.balance = initBalance
        self.ID = ID

    def getBalance(self):
        return self.balance

    def deposit(self, amt):
        self.balance += amt

    def withdraw(self, amt):
        result = False  # asusume operation failure
        if amt <= self.balance:
            self.balance -= amt
        else:
            raise OverdraftException("资金不足", amt - self.balance)


# SavingAccount继承Account类,定义储蓄账户
class SavingAccount(Account):
    def __init__(self, ID, initBalance, interestRate=0.05):
        Account.__init__(self, ID, initBalance)
        self.interestRate = interestRate

    def accumulateInterest(self):
        self.balance += (self.balance * self.interestRate)


# CheckingAccount类继承Account类，定义信用账户，允许在信用额度内超支


class CheckingAccount(Account):
    def __init__(self, initBalance, initID, overdraftAmount=5000):
        Account.__init__(self, initBalance, initID)
        self.maxOverdraftAmount = overdraftAmount
        if self.balance >= 0:
            self.overdraftAmount = self.maxOverdraftAmount
        else:
            self.overdraftAmount = self.maxOverdraftAmount + self.balance

    def withdraw(self, amount):#需要取的钱(amount)
        if self.balance < amount:#判断余额够不够取
            if self.balance > 0:
                overdraftNeeded = amount - self.balance#当余额还剩时，需要透支(取钱-余额)
            else:
                overdraftNeeded = amount#当本身已经没有余额了，直接需要透支 取的额度

            if self.overdraftAmount < overdraftNeeded:#如果信用额度不够用了，抛出异常
                raise OverdraftException("透支保护资金不足", overdraftNeeded)
            else:#如果信用额度够用即能够透支，
                self.overdraftAmount -= overdraftNeeded#则直接扣除信用额度
        self.balance -= amount#扣除余额，返回值

        # if self.balance < amount:#当amount(要取的钱)比balance(余额)大
        #     overdraftNeeded = amount - self.balance#overdraftNeeded(需要透支的钱)
        #     if self.overdraftAmount < overdraftNeeded:#overdraftAmount(当信用额度)不足以需要透支的钱
        #         raise OverdraftException("透支保护资金不足", overdraftNeeded)
        #     else:#当可以透支
        #         self.balance = self.balance +
        #         self.overdraftAmount -= overdraftNeeded#信用额度扣除
        # else:
        #     self.balance = self.balance - amount
    def deposit(self, amt):
        self.balance += amt
        if self.balance >= 0:
            self.overdraftAmount = self.maxOverdraftAmount
        else:
            self.overdraftAmount = self.maxOverdraftAmount+self.balance


