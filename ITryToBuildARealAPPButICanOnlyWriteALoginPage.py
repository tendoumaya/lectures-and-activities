import sys
from matplotlib import pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
################################################
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Waste Processing Tracking and Statisting System(Beta)')

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.Layout = QVBoxLayout(self.centralwidget)

        self.topwidget = QWidget()
        self.Layout.addWidget(self.topwidget)
        self.buttonLayout = QHBoxLayout(self.topwidget)

        self.pushButton_Trac=QPushButton()
        self.pushButton_Trac.setText("Tracking")
        self.buttonLayout.addWidget(self.pushButton_Trac)

        self.pushButton_Stat=QPushButton()
        self.pushButton_Stat.setText("Statistics")
        self.buttonLayout.addWidget(self.pushButton_Stat)

        self.pushButton_Trac.clicked.connect(self.on_pushButton_Trac_clicked)
        self.pushButton_Stat.clicked.connect(self.on_pushButton_Stat_clicked)

    def on_pushButton_Trac_clicked(self):
        plt.figure
        plt.title('Function availbe in later version',fontsize=20)
        plt.show()
        

    def on_pushButton_Stat_clicked(self):
        plt.figure()
        labels='Biodegradable','Other','Recycling','Hazardous'
        sizes=5,6,7,8
        colors='lightgreen','grey','lightskyblue','lightcoral'
        explode=0,0,0,0
        plt.pie(sizes,explode=explode,labels=labels,
        colors=colors,autopct='%1.1f%%',shadow=True,startangle=50)
        plt.axis('equal')
        plt.title('Annual Report',{'fontsize': 18})
        plt.show()
        

    

################################################
class logindialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Log-in')
        self.resize(200, 200)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        #
        self.frame = QFrame(self)
        self.verticalLayout = QVBoxLayout(self.frame)

        self.lineEdit_account = QLineEdit()
        self.lineEdit_account.setPlaceholderText("Your user id(114514)")
        self.verticalLayout.addWidget(self.lineEdit_account)

        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText("Password(1919810)")
        self.verticalLayout.addWidget(self.lineEdit_password)

        self.pushButton_enter = QPushButton()
        self.pushButton_enter.setText("Next")
        self.verticalLayout.addWidget(self.pushButton_enter)

        self.pushButton_quit = QPushButton()
        self.pushButton_quit.setText("Cancel")
        self.verticalLayout.addWidget(self.pushButton_quit)

        #botton movement
        self.pushButton_enter.clicked.connect(self.on_pushButton_enter_clicked)
        self.pushButton_quit.clicked.connect(self.ext)

        
    def on_pushButton_enter_clicked(self):
        # account
        if self.lineEdit_account.text() == "114514" and self.lineEdit_password.text() == "1919810":
            # pass and return 1
            self.accept()
            return 
        else:
            print('Unidentified user-id or password')

    def ext(self):
        sys.quit()


################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = logindialog()
    if  dialog.exec_()==QDialog.Accepted:
        the_window = MainWindow()
        the_window.show()
        sys.exit(app.exec_())
