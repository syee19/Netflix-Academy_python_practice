from PySide2 import QtWidgets, QtCore, QtUiTools
from PySide2.QtGui import QDropEvent, QDragEnterEvent
import sys
import os
import dark_renamer


class ExplorerList(QtWidgets.QListWidget):
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)
        self.setObjectName('explorer_list')


class BasketList(QtWidgets.QListWidget):
    def __init__(self, renamer):
        super().__init__()
        self.renamer = renamer
        self.setAcceptDrops(True)
        self.setObjectName('basket_list')

    def dropEvent(self, event):
        text = event.source().currentItem().text()
        if self.renamer.add_file(text):
            self.addItem(ExplorerListItem(text, False))
            self.parent().findChild(QtWidgets.QLabel, 'basket_count').setText(str(self.count()) + '개')


class ExplorerListItem(QtWidgets.QListWidgetItem):
    def __init__(self, name, is_drag_enabled):
        super().__init__()
        self.setText(name)
        self.setSizeHint(QtCore.QSize(100, 25))
        # 파일만 Drag 가능하도록
        if not is_drag_enabled:
            flags = self.flags()
            flags ^= QtCore.Qt.ItemIsDragEnabled
            self.setFlags(flags)


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.dir_list = None
        self.renamer = dark_renamer.DarkRenamer(os.path.expanduser('~/rename_dir'))
        # set ui
        ui_path = os.path.expanduser('./dark_renamer.ui')
        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()
        self.ui.show()

        # self.ex = ExplorerList()
        self.ex = self.ui.explorer_list
        self.ui.explorer.addWidget(self.ex)
        self.bsk = BasketList(self.renamer)
        self.ui.basket.addWidget(self.bsk)
        self.ui.root_path.setText(self.renamer.path)

        self.update_explorer()
        self.ex.itemDoubleClicked.connect(self.clicked)

    def clicked(self, item):
        index = self.ex.row(item)
        if not self.dir_list[index]['is_file']:
            dir_name = self.dir_list[index]['name']
            self.renamer.move_pointer(dir_name)
            self.update_explorer()

    def update_explorer(self):
        self.ui.pointer.setText(self.renamer.pointer)
        for i in range(self.ex.count()):
            self.ex.takeItem(0)
        self.dir_list = self.renamer.get_dir_list()
        for i in range(len(self.dir_list)):
            self.ex.addItem(ExplorerListItem(self.dir_list[i]['name'], self.dir_list[i]['is_file']))


def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication()
    my_app = MyApp()
    # my_app.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
