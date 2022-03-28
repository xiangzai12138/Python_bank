import sys
sys.path.append("../domain")
from account import *
class Customer:
    def __init__(self,fname,lname,sex,minzu):
        self.firstName=fname
        self.lastName=lname
        self.accounts=list()
        self.sex = sex
        self.minzu=minzu
    def getFirsName(self):
        return self.firstName
    def getLastName(self):
        return self.lastName
    def getSex(self):
        return self.sex
    def getMinzu(self):
        return self.minzu
    def __str__(self):
        return self.firstName.title()+' '+self.lastName.title()
    def addAccount(self,acct):
        self.accounts.append(acct)
    def getNumOfAccounts(self):
        return self.accounts.size()
    def getAccount(self,account_index):
        return self.accounts[account_index]