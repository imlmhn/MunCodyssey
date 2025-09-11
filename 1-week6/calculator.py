import sys
import ast
import operator
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
        self.layout = QVBoxLayout() # 위에서부터 수직으로 요소를 붙이는 레이아웃
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

    def format_number(self, num_str):
        try:
            if '.' in num_str:
                num = float(num_str)
                return f"{num:,.10g}"
            else:
                num = int(num_str)
                return f"{num:,}"
        except:
            return num_str

    def safe_eval(self, expr):
        try:
            expr = expr.replace('×', '*').replace('÷', '/')
            tree = ast.parse(expr, mode='eval')

            def _eval(node):
                if isinstance(node, ast.Expression):
                    return _eval(node.body)
                elif isinstance(node, ast.BinOp):
                    left = _eval(node.left)
                    right = _eval(node.right)
                    ops = {
                        ast.Add: operator.add,
                        ast.Sub: operator.sub,
                        ast.Mult: operator.mul,
                        ast.Div: operator.truediv,
                    }
                    return ops[type(node.op)](left, right)
                elif isinstance(node, ast.UnaryOp):
                    if isinstance(node.op, ast.USub):
                        return -_eval(node.operand)
                elif isinstance(node, ast.Num):
                    return node.n
                elif isinstance(node, ast.Constant):
                    return node.value
                else:
                    raise TypeError("Unsupported type")
            return str(_eval(tree))
        except:
            return "Error"

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
            if self.reset_next_input:
                self.expression = '0.'
                self.reset_next_input = False
            elif '.' not in self.expression.split()[-1]:
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
                self.expression = result

        elif text == 'AC':
            self.expression = ""
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

        # 표시 형식 적용
        if self.expression not in ['Error', '']:
            if self.expression[-1] in '+-×÷':
                self.display.setText(self.expression)
            else:
                self.display.setText(self.format_number(self.expression))
        else:
            self.display.setText(self.expression)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())
