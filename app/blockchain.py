from web3 import Web3, HTTPProvider
from solc import compile_source
from web3.contract import ConciseContract
from app import db
from .models import User, AddressBook
import string
import random
from eth_utils import decode_hex


class BlockchainTransact:

    def __init__(self):
        self.parentAccount = "0x001ebfeb4539388ede520f6374fab6f91200f89d"
        self.parentPass = "cwTYyo2oFX5c52MbnEAuPpDCoCNwQPolIUYx5lJH"
        self.w3 = Web3(HTTPProvider('http://18.220.176.148:8545'))
        f = open("/var/www/Backend/app/Betrc.sol")
        cc = f.read()
        f.close()
        self.cCode = compile_source(cc)
        contract_interface = self.cCode['<stdin>:BetrC']
        self.contractInstance = self.w3.eth.contract(contract_interface['abi'], "0xb5385899d02975fd7f5618f4a7d0a0ca691d27eb", ContractFactoryClass=ConciseContract)

    def generate_random_passkey(self, N):
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N))

    def unlock_master(self):
        unlockcRes = self.w3.personal.unlockAccount(self.parentAccount, self.parentPass)
        return unlockcRes

    def unlock_user(self, account_hex, bc_passphrase):
        unlockRes = self.w3.personal.unlockAccount(account_hex, bc_passphrase)
        return unlockRes

    def make_new_account(self, userID):
        newkey = self.generate_random_passkey(40)
        newAcc = self.w3.personal.newAccount(newkey)
        newAdbook = AddressBook(userID, newAcc, newkey)
        db.session.add(newAdbook)
        db.session.commit()
        return newAcc

    def newPayment(self, email, amount):
        user = db.session.query(User).filter_by(email=email).first()
        if user is None:
            return False
        bcAddr = db.session.query(AddressBook).filter_by(user_id=user.id).first()
        if bcAddr is None:
            newAcc = self.make_new_account(user.id)
            unlockres = self.unlock_master()
            if unlockres:
                txHash = self.contractInstance.transfer(decode_hex(newAcc), int(amount), transact={'from' : self.parentAccount})
                return True, txHash
            return False
        accHex = bcAddr.account_hex
        print("accHex: ", accHex)
        unlockres = self.unlock_master()
        if unlockres:
            txHash = self.contractInstance.transfer(decode_hex(accHex), int(amount), transact={'from' : self.parentAccount})
            return True, txHash
        return False

    def newPayment_with_uid(self, userID, amount):
        bcAddr = db.session.query(AddressBook).filter_by(user_id=userID).first()
        if bcAddr is None:
            newAcc = self.make_new_account(user.id)
            unlockres = self.unlock_master()
            if unlockres:
                txHash = self.contractInstance.transfer(decode_hex(newAcc), int(amount), transact={'from' : self.parentAccount})
                return True, txHash
            return False
        accHex = bcAddr.account_hex
        unlockres = self.unlock_master()
        if unlockres:
            txHash = self.contractInstance.transfer(decode_hex(accHex), int(amount), transact={'from' : self.parentAccount})
            return True, txHash
        return False

    def withdraw_from_user(self, userID, amount):
        bcAddr = db.session.query(AddressBook).filter_by(user_id=userID).first()
        if bcAddr is None:
            return False
        accHex = str(bcAddr.account_hex)
        unlockPhr = bcAddr.bc_passphrase
        unlockRes = self.unlock_user(accHex, unlockPhr)
        if unlockRes:
            #successful unlock of account
            txHash = self.contractInstance.transfer(self.parentAccount, int(amount), transact={'from' : accHex})
            return True, txHash
        else:
            return False
        return False

    def getBalance(self, email):
        user = db.session.query(User).filter_by(email=email).first()
        if user is None:
            return False
        bcAddr = db.session.query(AddressBook).filter_by(user_id=user.id).first()
        if bcAddr is None:
            newAcc = self.make_new_account(user.id)
            return 0
        accHex = bcAddr.account_hex
        account_balance = self.contractInstance.balanceOf(decode_hex(accHex))
        return account_balance

    def getBalance_from_uid(self, userID):
        user = db.session.query(User).filter_by(id=userID).first()
        if user is None:
            return False
        bcAddr = db.session.query(AddressBook).filter_by(user_id=user.id).first()
        if bcAddr is None:
            newAcc = self.make_new_account(user.id)
            return 0
        accHex = bcAddr.account_hex
        account_balance = self.contractInstance.balanceOf(decode_hex(accHex))
        return account_balance

    def verify_payout(self, email, requestedAmt):
        availableFunds = self.getBalance(email)
        if requestedAmt > availableFunds:
            return False
        return True
