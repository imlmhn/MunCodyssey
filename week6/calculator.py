# calculator.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
)
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPhone 스타일 계산기")
        self.setFixedSize(500, 900)
        self.setStyleSheet("background-color: #000000;")
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.display = QLineEdit("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(235)
        self.display.setFixedWidth(430)
        self.display.setContentsMargins(0, 150, 0, 0)
        self.display.setStyleSheet("""
            QLineEdit {
                color : white;
                font-size : 80px;
                border : none;
            }                           
        """)
        

        self.layout.addWidget(self.display)
        self.buttonLayout = QGridLayout()
        self.buttonLayout.setHorizontalSpacing(3)   # 가로 간격
        self.buttonLayout.setVerticalSpacing(9)     # 세로 간격
        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['', '0', '.', '=']
        ]
        # 맨 위 4개 버튼
        top_buttons = ['AC', '+/-', '%']
        # 오른쪽 세로 버튼
        right_buttons = ['÷', '×', '-', '+', '=']
        # 버튼 생성 및 레이아웃 배치
        for row, row_values in enumerate(buttons):
            for col, btn_text in enumerate(row_values):
                btn = QPushButton(btn_text)
                btn.setFixedHeight(100)
                btn.setFixedWidth(100)
                if btn_text in top_buttons:
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #A5A5A5;
                            color: white;
                            font-size: 40px;
                            font-weight : bold;
                            border-radius: 50px;
                        }
                    """)
                elif btn_text in right_buttons:
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: orange;
                            color: white;
                            font-size: 40px;
                            font-weight : bold;
                            border-radius: 50px;
                        }
                    """)
                else:
                    # 기본 숫자 버튼
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #333;
                            color: white;
                            font-size: 40px;
                            font-weight : bold;
                            border-radius: 50px;
                        }
                    """)
                    
                if btn_text == '0':
                    # btn = QPushButton(btn_text)
                    # btn.setFixedHeight(80)
                    # btn.setFixedWidth(150)
                    self.buttonLayout.addWidget(btn, row + 1, col)
                elif btn_text == '=' and len(row_values) == 3:
                    # btn = QPushButton(btn_text)
                    # btn.setFixedHeight(80)
                    self.buttonLayout.addWidget(btn, row + 1, col + 1)
                elif btn_text != '0':
                    # btn = QPushButton(btn_text)
                    # btn.setFixedSize(70, 80)
                    self.buttonLayout.addWidget(btn, row + 1, col)
                
                btn.clicked.connect(self.onButtonClick)

        self.layout.addLayout(self.buttonLayout)
        self.setLayout(self.layout)
        self.expression = ""

    def onButtonClick(self):
        button = self.sender()
        text = button.text()

        if text == 'AC':
            self.expression = ""
        elif text == '+/-':
            if self.expression:
                if self.expression.startswith('-'):
                    self.expression = self.expression[1:]
                else:
                    self.expression = '-' + self.expression
        elif text == '%':
            try:
                self.expression = str(float(self.expression) / 100)
            except:
                self.expression = "Error"
        elif text == '=':
            try:
                expression = self.expression.replace('×', '*').replace('÷', '/')
                self.expression = str(eval(expression))
            except:
                self.expression = "Error"
        else:
            self.expression += text

        self.display.setText(self.expression)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())
