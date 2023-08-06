"""
The MIT License (MIT)

Copyright (c) 2016 pystockhub

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from Kiwoom import *

form_class =uic.loadUiType("./resource/ui/pytrader.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.kiwoom = Kiwoom()
        self.kiwoom.comm_connect() # Todo: 그냥 종료 눌렀을 경우 루프 탈출 불가 문제

        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeout)

        self.stock_code_input.textChanged.connect(self.code_changed)

        self.init_account_selector()
        self.send_order_button.clicked.connect(self.send_order)

    def init_account_selector(self):
        accounts_num = int(self.kiwoom.get_login_info("ACCOUNT_CNT"))
        accounts = self.kiwoom.get_login_info("ACCNO")
        accounts_list = accounts.split(';')[:accounts_num]
        self.account_selector.addItems(accounts_list)
    
    def timeout(self):
        current_time = QTime.currentTime()
        text_time = current_time.toString("hh:mm:ss")
        time_msg = "현재시간: " + text_time

        state = self.kiwoom.GetConnectState()
        if state == 1:
            state_msg = "Connected"
        else:
            state_msg = "Disconnected"
        
        self.statusBar().showMessage(state_msg + " | " + time_msg)

    def code_changed(self):
        code = self.stock_code_input.text()
        name = self.kiwoom.get_master_code_name(code)
        self.stock_name_printer.setText(name)

    def send_order(self):
        order_type_lookup = {"신규매수" : 1, "신규매도" : 2, "매수취소" : 3, "매도취소" : 4}
        hoga_lookup = {"지정가" : "00", "시장가" : "03"}

        account = self.account_selector.currentText()
        order_type = self.order_type_selector.currentText()
        code = self.stock_code_input.text()
        hoga = self.hoga_selector.currentText()
        num = self.order_stock_num_input.value()
        price = self.order_stock_price_input.value()

        self.kiwoom.send_order("send_order_req", "0101", account, order_type_lookup[order_type], code, num, price, hoga_lookup[hoga], "")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()