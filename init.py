from queries import SocialNetwork
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import QFile, QTextStream, Qt
from sys import argv

social = SocialNetwork()

try:
    social.create_user("bob@example.com")
    social.create_user("alice@example.com")
    social.create_user("charlie@example.com")
    social.create_user("david@example.com")
    social.create_user("eve@example.com")

    social.create_account("bob@example.com", "bob123")
    social.create_account("alice@example.com", "alice456")
    social.create_account("charlie@example.com", "charlie789")
    social.create_account("david@example.com", "david000")
    social.create_account("eve@example.com", "eve999")

    social.create_post(1,"Just watched the sunset over the city. Sometimes, you gotta stop and appreciate the little things.")       # Bob(ID 1)
    social.create_post(2,"Anyone else feel like time moves too fast these days? One minute it's morning, next thing you know it's midnight.")     # Alice(ID 2)
    social.create_post(3,"Finally finished that book everyone's been talking about. No spoilers, but wow... that ending.")   # Charlie(ID 3)
    social.create_post(4,"Tried making homemade ramen today. It was either a masterpiece or a disaster—no in-between.")     # David(ID 4)

    social.add_like(2, 1)# Alice Bob
    social.add_like(3, 2)# Charlie Alice
    social.add_like(2, 2)# Alice Alice
    social.add_like(4, 3)# David Charlie
    social.add_like(5, 1)# Eve David

    social.create_follow(1,2)
    social.create_follow(1,3)

    print("\nLike Numbers:")
    social.print_bacon_like_numbers("bob123",5)

    print("\nbob123's feed:")
    social.get_user_feed("bob123")

    social.create_mute(1,2)
    print("\nbob123's feed after muting alice436:")
    social.get_user_feed("bob123")

    social.close()
except Exception as e:
    raise e
    
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() 
        uic.loadUi('main.ui', self)
        self.show()
        self.terminal_output = self.findChild(QtWidgets.QTextEdit, 'TerminalOutput')
        self.user_email = self.findChild(QtWidgets.QPlainTextEdit, 'Email_input')
        self.user_create_button = self.findChild(QtWidgets.QPushButton, 'user_create_button')
        self.user_create_button.clicked.connect(self.create_user)
        
    
    def create_user(self):
        output = social.create_user(self.user_email.toPlainText())
        self.terminal_output.setPlainText("\n" + output)

def main():
    app = QtWidgets.QApplication(argv)
    window = Ui()
    app.exec_()
    

main()