from enum import Enum
from datetime import datetime

OPEN_PROFILE = "ALL"

class Message():
    messageString = ""
    openableBy = OPEN_PROFILE
    sender = ""
    recipient = ""
    time = 0

    def __init__(self, msg, opnb, sndr, rcpt) -> None:
        self.messageString = msg
        self.openableBy = opnb
        self.sender = sndr
        self.recipient = rcpt
        self.setTimeNow()
    
    def setTimeNow(self):
        self.time = datetime.now()

class ProfileName(str, Enum):
    profileA = "red"
    profileB = "blue"
    profileC = "green"
    profileD = "yellow"
    profileE = "purple"
    profileF = "black"
    profileG = "white"
    profileH = "brown"
    profileI = "orange"