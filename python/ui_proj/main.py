import sys
import os
from PySide2 import QtWidgets, QtCore, QtUiTools


class MyCalc(QtWidgets.QMainWindow):
    input_text = ''

    def __init__(self):
        super().__init__()

        # set ui
        ui_path = os.path.expanduser('~/my_calc.ui')
        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()
        self.ui.show()

        # connect button
        # central_widget = self.ui.findChild(QtWidgets.QWidget, 'centralwidget')
        # for child in central_widget.findChildren(QtWidgets.QPushButton):
        for child in self.ui.findChildren(QtWidgets.QPushButton):
            child.clicked.connect(self.apply_value)

        # 아래 코드들을 위처럼 줄여 쓸 수 있음
        # append_input: 식의 맨 앞에 올 수 있음
        # self.ui.btn_1.clicked.connect(lambda: self.append_input('1'))
        # self.ui.btn_2.clicked.connect(lambda: self.append_input('2'))
        # self.ui.btn_3.clicked.connect(lambda: self.append_input('3'))
        # self.ui.btn_4.clicked.connect(lambda: self.append_input('4'))
        # self.ui.btn_5.clicked.connect(lambda: self.append_input('5'))
        # self.ui.btn_6.clicked.connect(lambda: self.append_input('6'))
        # self.ui.btn_7.clicked.connect(lambda: self.append_input('7'))
        # self.ui.btn_8.clicked.connect(lambda: self.append_input('8'))
        # self.ui.btn_9.clicked.connect(lambda: self.append_input('9'))
        # self.ui.btn_0.clicked.connect(lambda: self.append_input('0'))

        # append_commend: 식의 맨 앞에 올 수 없음
        # self.ui.btn_point.clicked.connect(lambda: self.append_commend('.'))
        # self.ui.op_add.clicked.connect(lambda: self.append_commend('+'))
        # self.ui.op_sub.clicked.connect(lambda: self.append_commend('-'))
        # self.ui.op_mul.clicked.connect(lambda: self.append_commend('×'))
        # self.ui.op_div.clicked.connect(lambda: self.append_commend('÷'))
        # self.ui.op_mod.clicked.connect(lambda: self.append_commend('mod'))
        # self.ui.op_cube.clicked.connect(lambda: self.append_commend('²'))

        # self.ui.cmd_reset.clicked.connect(self.reset)
        # self.ui.cmd_del.clicked.connect(self.delete)
        # self.ui.cmd_calc.clicked.connect(self.calc)

    def apply_value(self):
        # sender(): 시그널을 보낸 widget을 반환
        button = self.sender()
        if button.objectName().startswith('btn_'):
            self.append_input(button.accessibleName())
        elif button.objectName().startswith('op_'):
            self.append_commend(button.accessibleName())
        elif button.objectName().endswith('_calc'):
            self.calc()
        elif button.objectName().endswith('_del'):
            self.delete()
        elif button.objectName().endswith('_reset'):
            self.reset()

    def reset(self):
        self.input_text = ''
        self.ui.input.setText(self.input_text)
        self.ui.result.display(0)
        return

    def delete(self):
        if self.input_text == '':
            return
        if self.input_text[-1] == 'd':
            # 'mod'는 한 번에 지워지도록
            self.input_text = self.input_text[:-3]
        else:
            self.input_text = self.input_text[:-1]
        self.ui.input.setText(self.input_text)
        return

    def parse(self):
        parsed_string = ''
        for i in self.input_text:
            if i == '×':
                parsed_string += '*'
                continue
            if i == '÷':
                parsed_string += '/'
                continue
            if i == 'm':
                # 'mod'는 한 번에 파싱
                parsed_string += '%'
                continue
            if i == 'o' or i == 'd':
                continue
            if i == '²':
                parsed_string += '**2'
                continue
            parsed_string += i
        return eval(parsed_string)

    def calc(self):
        if self.input_text == '' or not self.input_text[-1].isdigit():
            return
        res = self.parse()
        if len(str(res)) >= 8:
            res = str(res)[:8]
        self.input_text = ''
        self.ui.input.setText(self.input_text)
        self.ui.result.display(res)
        return

    def point_avail(self):
        # 지금까지 작성한 수식을 뒤에서부터 추적하며, 현재 소수점을 추가할 수 있는지 확인
        avail = False
        for i in self.input_text[::-1]:
            if i in ['+', '-', '×', '÷', 'd']:
                avail = True
                continue
            if not avail and i == '.':
                return False
        return True

    def remove_zero(self):
        # self.input_text의 뒤부터 시작해 계산 기호 전까지의 숫자를 분리
        num = ''
        for i in self.input_text[::-1]:
            if i in ['+', '-', '×', '÷', 'd', '²']:
                break
            num = i + num
        if num == '0':
            self.input_text = self.input_text[:-1]
            return True
        return True

    def append_commend(self, cmd):
        if not len(self.input_text):
            return
        # 놀랍게도 '²'.isdigit()은 True...
        if cmd == '²' and self.input_text[-1] == '²':
            return
        if cmd == '.' and not self.point_avail():
            return
        if len(self.input_text) and self.input_text[-1].isdigit():
            self.append_input(cmd)
        return

    def append_input(self, char):
        if len(self.input_text) >= 13:
            return
        if char == '0' and len(self.input_text) and self.input_text[-1] in ['÷', 'd']:
            # 0으로 나누기 방지
            return
        if char not in ['.', '+', '-', '×', '÷', 'mod', '²']:
            self.remove_zero()
        self.input_text = str(self.input_text) + char
        self.ui.input.text = self.input_text
        self.ui.input.setText(self.input_text)
        return


def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication()
    my_calc = MyCalc()
    sys.exit((app.exec_()))


if __name__ == '__main__':
    main()
