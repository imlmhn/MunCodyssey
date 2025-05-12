import sys
import re

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
        self.buttonLayout.setHorizontalSpacing(3)
        self.buttonLayout.setVerticalSpacing(9)

        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['', '0', '.', '=']
        ]

        top_buttons = ['AC', '+/-', '%']
        right_buttons = ['÷', '×', '-', '+', '=']

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
                    btn.setFixedWidth(210)
                    self.buttonLayout.addWidget(btn, row + 1, col - 1, 1, 2)
                elif btn_text == '=' and len(row_values) == 3:
                    self.buttonLayout.addWidget(btn, row + 1, col + 1)
                elif btn_text != '0':
                    self.buttonLayout.addWidget(btn, row + 1, col)

                btn.clicked.connect(self.onButtonClick)

        self.layout.addLayout(self.buttonLayout)
        self.setLayout(self.layout)
        self.expression = ""
        self.reset_next_input = False

    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b
    def divide(self, a, b): return a / b if b != 0 else "Error"

    def format_number(self, num_str):
        try:
            if num_str.endswith('.'):
                return num_str
            if '.' in num_str:
                num = float(num_str)
                return f"{num:,.10g}"
            else:
                num = int(num_str)
                return f"{num:,}"
        except:
            return num_str


    def adjust_font_size(self, text):
        length = len(text)
        if length <= 8:
            size = 80
        elif length <= 12:
            size = 60
        elif length <= 18:
            size = 40
        else:
            size = 30

        self.display.setStyleSheet(f"""
            QLineEdit {{
                color : white;
                font-size : {size}px;
                border : none;
            }}                           
        """)

    def safe_eval(self, expr):
        try:
            # 1. '×'를 '*'로, '÷'를 '/'로 변환하여 Python 연산자가 사용될 수 있도록 수정
            expr = expr.replace('×', '*').replace('÷', '/')

            # 2. *와 / 연산자부터 먼저 처리 (우선순위)
            while re.search(r'\d+(\.\d+)?\s*[\*/]\s*-?\d+(\.\d+)?', expr):
                expr = re.sub(r'(\d+(\.\d+)?)\s*([\*/])\s*(-?\d+(\.\d+)?)', self._compute_mul_div, expr, count=1)

            # 3. +와 - 연산자 처리
            while re.search(r'-?\d+(\.\d+)?\s*[\+-]\s*-?\d+(\.\d+)?', expr):
                expr = re.sub(r'(-?\d+(\.\d+)?)\s*([\+-])\s*(-?\d+(\.\d+)?)', self._compute_add_sub, expr, count=1)

            result = float(expr)  # 문자열을 실수로 변환
            result = round(result, 6)  # 6자리 반올림

            return str(result) 
        
        except:
            return "Error"

    def _compute_mul_div(self, match):
        a, op, b = float(match.group(1)), match.group(3), float(match.group(4))
        if op == '*':
            return str(self.multiply(a, b))
        elif op == '/':
            result = self.divide(a, b)
            return str(result) if result != "Error" else "Error"

    def _compute_add_sub(self, match):
        a, op, b = float(match.group(1)), match.group(3), float(match.group(4))
        if op == '+':
            return str(self.add(a, b))
        elif op == '-':
            return str(self.subtract(a, b))

    def onButtonClick(self):
        button = self.sender()
        text = button.text()

        if text in '0123456789':
            if self.display.text() == "0" or self.reset_next_input or self.display.text() == "Error":
                self.expression = text
                self.reset_next_input = False
            else:
                self.expression += text

        elif text == '.':
            if self.reset_next_input or self.expression == "":
                self.expression = "0."
                self.reset_next_input = False
            else:
                tokens = re.split(r'[+\-×÷]', self.expression)
                if '.' not in tokens[-1]:
                    self.expression += '.'

        elif text in '+-×÷':
            if self.expression and self.expression[-1] not in '+-×÷':
                self.expression += text
                self.reset_next_input = False

        elif text == '=':
            result = self.safe_eval(self.expression)
            if result != "Error":
                self.expression = result
                self.reset_next_input = True
            else:
                self.expression = "Error"

        elif text == 'AC':
            self.expression = '0'
            self.reset_next_input = False

        elif text == '+/-':
            if self.expression.startswith('-'):
                self.expression = self.expression[1:]
            elif self.expression and self.expression[0].isdigit():
                self.expression = '-' + self.expression

        elif text == '%':
            try:
                value = self.safe_eval(self.expression)
                if value != "Error":
                    self.expression = str(float(value) / 100)
                    self.reset_next_input = True
                else:
                    self.expression = "Error"
            except:
                self.expression = "Error"

        # 결과 표시 및 폰트 크기 조절
        if self.expression not in ['Error', '']:
            if self.expression[-1] in '+-×÷':
                self.display.setText(self.expression)
                self.adjust_font_size(self.expression)
            else:
                formatted = self.format_number(self.expression)
                self.display.setText(formatted)
                self.adjust_font_size(formatted)
        else:
            self.display.setText(self.expression)
            self.adjust_font_size(self.expression)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())
