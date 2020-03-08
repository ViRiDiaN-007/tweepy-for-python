# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TwitterApp.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import tweepy
import re


errorMessage=re.compile('.*\w')
##Get OAuth tokens from file. This is needed to authenticate the user
with open('auth.txt','r')as authFile:
    tokens=authFile.readlines()
    tokens= [token.strip('\n') for token in tokens]
    tokens=[token.split('=')[1]for token in tokens]
    consumer_key,consumer_secret,access_key,access_secret=tokens[0],tokens[1],tokens[2],tokens[3]
try:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key,access_secret)
    api=tweepy.API(auth)
except Exception as e:
    print(f'Error: {e}')

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 227)
        self.actionLabel = QtWidgets.QLabel(Dialog)
        self.actionLabel.setGeometry(QtCore.QRect(10, 10, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.actionLabel.setFont(font)
        self.actionLabel.setObjectName("actionLabel")
        self.usernameField = QtWidgets.QLineEdit(Dialog)
        self.usernameField.setGeometry(QtCore.QRect(120, 30, 101, 20))
        self.usernameField.setObjectName("usernameField")
        self.messageLabel = QtWidgets.QLabel(Dialog)
        self.messageLabel.setGeometry(QtCore.QRect(10, 120, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.messageLabel.setFont(font)
        self.messageLabel.setObjectName("messageLabel")
        self.usernameLabel = QtWidgets.QLabel(Dialog)
        self.usernameLabel.setGeometry(QtCore.QRect(140, 10, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setKerning(True)
        self.usernameLabel.setFont(font)
        self.usernameLabel.setObjectName("usernameLabel")
        self.messageField = QtWidgets.QTextEdit(Dialog)
        self.messageField.setGeometry(QtCore.QRect(10, 150, 221, 71))
        self.messageField.setObjectName("messageField")
        self.tweetButton = QtWidgets.QRadioButton(Dialog)
        self.tweetButton.setGeometry(QtCore.QRect(10, 40, 82, 17))
        self.tweetButton.setObjectName("tweetButton")
        self.messageButton = QtWidgets.QRadioButton(Dialog)
        self.messageButton.setGeometry(QtCore.QRect(10, 60, 101, 17))
        self.messageButton.setObjectName("messageButton")
        self.followButton = QtWidgets.QRadioButton(Dialog)
        self.followButton.setGeometry(QtCore.QRect(10, 80, 82, 17))
        self.followButton.setObjectName("followButton")
        self.unfollowButton = QtWidgets.QRadioButton(Dialog)
        self.unfollowButton.setGeometry(QtCore.QRect(10, 100, 101, 17))
        self.unfollowButton.setObjectName("unfollowButton")
        self.runButton = QtWidgets.QPushButton(Dialog)
        self.runButton.setGeometry(QtCore.QRect(240, 190, 151, 23))
        self.runButton.setObjectName("runButton")
        self.log = QtWidgets.QTextEdit(Dialog)
        self.log.setGeometry(QtCore.QRect(240, 30, 151, 151))
        font = QtGui.QFont()
        font.setPointSize(6)
        self.log.setFont(font)
        self.log.setReadOnly(True)
        self.log.setObjectName("log")
        self.logLabel = QtWidgets.QLabel(Dialog)
        self.logLabel.setGeometry(QtCore.QRect(240, 10, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.logLabel.setFont(font)
        self.logLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.logLabel.setObjectName("logLabel")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.runButton.clicked.connect(self.run)
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Awful Twitter App"))
        self.actionLabel.setText(_translate("Dialog", "Actions"))
        self.messageLabel.setText(_translate("Dialog", "Message"))
        self.usernameLabel.setText(_translate("Dialog", "Username"))
        self.messageField.setDocumentTitle(_translate("Dialog", "Send A Message"))
        self.messageField.setPlaceholderText(_translate("Dialog", "Type a tweet or message here.                                                                                   -                                                               Max. 280 Characters"))
        self.tweetButton.setText(_translate("Dialog", "Send Tweet"))
        self.messageButton.setText(_translate("Dialog", "Send Message"))
        self.followButton.setText(_translate("Dialog", "Follow User"))
        self.unfollowButton.setText(_translate("Dialog", "Unfollow User"))
        self.runButton.setText(_translate("Dialog", "Run"))
        self.logLabel.setText(_translate("Dialog", "Debug Console"))
    def getError(self,e):
        e=str(e).split(':')
        e=e[2]
        error=errorMessage.search(str(e))
        error=error.group()
        self.log.append('Error: '+str(error)+"'")
    def run(self):
        if self.tweetButton.isChecked():
            try:
                tweet=self.messageField.toPlainText()
                api.update_status(tweet)
                self.log.append('Tweet Sent!')
            except Exception as e:
                self.getError(e)
        elif self.followButton.isChecked():
            try:
                screenName=self.usernameField.text()
                screenName=screenName.strip('@')
                user=api.get_user(screen_name=screenName)
                api.create_friendship(user.id,screenName)
                self.log.append(f'Now Following @{screenName}')
            except Exception as e:
                self.getError(e)
        elif self.unfollowButton.isChecked():
            try:
                screenName=self.usernameField.text()
                screenName=screenName.strip('@')
                user=api.get_user(screen_name=screenName)
                api.destroy_friendship(user.id,screenName)
                self.log.append(f'Unfollowed @{screenName}')
            except Exception as e:
                self.getError(e)
        elif self.messageButton.isChecked():
            try:
                screenName=self.usernameField.text()
                screenName=screenName.strip('@')
                user=api.get_user(screen_name=screenName)
                message=self.messageField.toPlainText()
                api.send_direct_message(user.id,message)
                self.messageField.clear()
                self.log.append(f'Message sent')
            except Exception as e:
               self.getError(e)
                
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
