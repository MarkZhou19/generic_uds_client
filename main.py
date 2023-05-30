from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

from Ui_untitled import Ui_MainWindow

import sys
import threading
import os
import glob
import cantools
from PyQt5 import QtWidgets

def remove_layout(layout: QtWidgets.QLayout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        sub_layout = item.layout()
        
        if widget:
            widget.setParent(None)
            del widget
        elif sub_layout:
            remove_layout(sub_layout)
        
        del item
    
    del layout

def findDBCFiles(path):
    files = []
    # get all the files in the directory
    # for each file, check if it is a dbc file
    # if it is, add it to the list
    for file in glob.glob(path + "/**/*.dbc", recursive=True):
        files.append(file)
    return files



class MyMainWindow(QMainWindow):
    active_dbc_db = None
    def button_clicked(self):
        pass

    def removeAllLayoutInParamsLayout(self):
        for i in reversed(range(self.ui.paramsLayout.count())):
            remove_layout(self.ui.paramsLayout.itemAt(i).layout())


    def on_comboBox_selected(self, index):
        self.removeAllLayoutInParamsLayout()
        self.active_dbc_db = cantools.database.load_file(self.ui.comboBox.currentText())
        if self.active_dbc_db != None:
            self.ui.appListWidget.clear()
            for message in self.active_dbc_db.messages:
                self.ui.appListWidget.addItem(message.name)
    
    def on_appListWidget_selected(self, current, previous):
        self.removeAllLayoutInParamsLayout()
        if self.active_dbc_db != None:
            for message in self.active_dbc_db.messages:
                if current != None and current.text() == message.name:
                    dict = {}
                    
                    for signal in message.signals:
                        layout = QtWidgets.QHBoxLayout()
                        edit = QtWidgets.QLineEdit()
                        lable = QtWidgets.QLabel()
                        lable.setText(signal.name)
                        layout.addWidget(lable)
                        layout.addWidget(edit)
                        self.ui.paramsLayout.addLayout(layout)
                        if signal.maximum != None:
                            edit.setText(str(signal.maximum))
                        else:
                            edit.setText("0")
                        dict[signal.name] = float(edit.text())
                    print(dict)
                    try:
                        can_message = self.active_dbc_db.encode_message(message.name, dict)
                        self.ui.canMsgTextEdit.clear()
                        self.ui.canMsgTextEdit.setText(''.join(format(byte, ' 02x') for byte in can_message))
                    except:
                        self.ui.canMsgTextEdit.clear()
                        self.ui.canMsgTextEdit.setText("Error")
                    

                    

                    # print(''.join(format(byte, ' 02x') for byte in can_message))
                    

    def __init__(self):
        super().__init__()
        
        # Set up the user interface from the loaded UI file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Connect signals and slots here (if needed)
        # Example: self.ui.button.clicked.connect(self.button_clicked)
        
        self.ui.pushButton.clicked.connect(self.button_clicked)
        self.ui.comboBox.currentIndexChanged.connect(self.on_comboBox_selected)
        self.ui.appListWidget.currentItemChanged.connect(self.on_appListWidget_selected)

        # Additional initialization code




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    dbcFile = findDBCFiles("DamonCANbus")
    print(len(dbcFile))
    window.ui.comboBox.addItems(dbcFile)
    
    sys.exit(app.exec_())