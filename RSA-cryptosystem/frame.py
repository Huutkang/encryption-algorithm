# -*- coding: utf-8 -*-

# Tệp giao diện được tạo tự động từ tệp 'main.ui'
# Được tạo bởi: PyQt5 UI code generator 5.15.4
# CẢNH BÁO: Không chỉnh sửa trực tiếp tệp này nếu không cần thiết, vì các thay đổi sẽ bị mất khi chạy lại lệnh `pyuic5`.

from PyQt5 import QtCore, QtGui, QtWidgets
from rsa import RSA  # Thư viện RSA được sử dụng cho mã hóa/giải mã

# Lớp giao diện chính của ứng dụng
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Cài đặt thuộc tính cơ bản cho cửa sổ chính
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(630, 600)

        # Tạo widget trung tâm
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Nút "Generate" (Phát sinh khóa)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(270, 165, 101, 41))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.result)  # Kết nối sự kiện bấm nút với hàm `result`

        # Các nhãn (labels) hiển thị thông tin
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 110, 51, 16))
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 210, 47, 13))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 240, 47, 13))
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 270, 47, 13))
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 310, 47, 13))
        self.label_5.setObjectName("label_5")

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 340, 47, 13))
        self.label_6.setObjectName("label_6")

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(10, 390, 47, 13))
        self.label_7.setObjectName("label_7")

        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(10, 470, 47, 13))
        self.label_8.setObjectName("label_8")

        # Các trường nhập liệu và kết quả
        self.message = QtWidgets.QTextEdit(self.centralwidget)  # Nhập tin nhắn
        self.message.setGeometry(QtCore.QRect(110, 110, 441, 50))
        self.message.setObjectName("message")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)  # Hiển thị thông tin RSA
        self.textEdit.setGeometry(QtCore.QRect(220, 10, 161, 51))
        self.textEdit.setObjectName("textEdit")

        self.p1 = QtWidgets.QLineEdit(self.centralwidget)  # Nhập giá trị p
        self.p1.setGeometry(QtCore.QRect(70, 210, 481, 20))
        self.p1.setObjectName("p1")

        self.q1 = QtWidgets.QLineEdit(self.centralwidget)  # Nhập giá trị q
        self.q1.setGeometry(QtCore.QRect(70, 240, 481, 20))
        self.q1.setObjectName("q1")

        self.e1 = QtWidgets.QLineEdit(self.centralwidget)  # Hiển thị giá trị e
        self.e1.setGeometry(QtCore.QRect(70, 270, 481, 20))
        self.e1.setObjectName("e1")

        self.d1 = QtWidgets.QLineEdit(self.centralwidget)  # Hiển thị giá trị d
        self.d1.setGeometry(QtCore.QRect(70, 310, 481, 20))
        self.d1.setObjectName("d1")

        self.N1 = QtWidgets.QLineEdit(self.centralwidget)  # Hiển thị giá trị N
        self.N1.setGeometry(QtCore.QRect(70, 340, 481, 20))
        self.N1.setObjectName("N1")

        self.enc1 = QtWidgets.QTextEdit(self.centralwidget)  # Hiển thị tin nhắn đã mã hóa
        self.enc1.setGeometry(QtCore.QRect(70, 390, 481, 60))
        self.enc1.setObjectName("enc1")
        self.enc1.setReadOnly = True  # Chỉ cho phép đọc

        self.dec1 = QtWidgets.QLineEdit(self.centralwidget)  # Hiển thị tin nhắn sau khi giải mã
        self.dec1.setGeometry(QtCore.QRect(70, 470, 481, 20))
        self.dec1.setObjectName("dec1")

        MainWindow.setCentralWidget(self.centralwidget)

        # Thanh menu và thanh trạng thái
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)  # Kết nối các tín hiệu với slot tương ứng

    # Hàm xử lý sự kiện nút Generate
    def result(self):
        self.rsa = RSA(keysize=32)  # Tạo hệ thống mã hóa RSA với độ dài khóa là 32 bit
        msg = self.message.toPlainText()  # Lấy nội dung tin nhắn từ trường nhập

        enc = self.rsa.encrypt(msg)  # Mã hóa tin nhắn
        dec = self.rsa.decrypt(enc)  # Giải mã tin nhắn
        self.enc1.setText(str(enc))  # Hiển thị tin nhắn đã mã hóa
        self.dec1.setText(str(dec))  # Hiển thị tin nhắn đã giải mã
        self.p1.setText(str(self.rsa.p))  # Hiển thị giá trị p
        self.q1.setText(str(self.rsa.q))  # Hiển thị giá trị q
        self.d1.setText(str(self.rsa.d))  # Hiển thị giá trị d
        self.e1.setText(str(self.rsa.e))  # Hiển thị giá trị e
        self.N1.setText(str(self.rsa.N))  # Hiển thị giá trị N

    # Hàm cài đặt các nhãn và văn bản hiển thị
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hệ mật RSA"))
        self.pushButton.setText(_translate("MainWindow", "Generate"))
        self.label.setText(_translate("MainWindow", "Message"))
        self.label_2.setText(_translate("MainWindow", "p"))
        self.label_3.setText(_translate("MainWindow", "q"))
        self.label_4.setText(_translate("MainWindow", "e"))
        self.label_5.setText(_translate("MainWindow", "d"))
        self.label_6.setText(_translate("MainWindow", "N"))
        self.label_7.setText(_translate("MainWindow", "Enc"))
        self.label_8.setText(_translate("MainWindow", "Dec"))

# Điểm bắt đầu của chương trình
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)  # Tạo ứng dụng PyQt5
    MainWindow = QtWidgets.QMainWindow()  # Tạo cửa sổ chính
    ui = Ui_MainWindow()  # Khởi tạo giao diện
    ui.setupUi(MainWindow)
    MainWindow.show()  # Hiển thị cửa sổ
    sys.exit(app.exec_())  # Thoát chương trình khi cửa sổ đóng
