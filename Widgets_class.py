from PyQt4 import QtCore, QtGui
class MakeWidgets(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QMainWindow.__init__(self,parent=None)
    def make_button(self,text,command,size=None):
        button=QtGui.QPushButton(self.centralwidget)
        if size:
            button.setMaximumSize(QtCore.QSize(*size))
        button.clicked.connect(command)
        button.setText(text)
        return button
    def make_line(self,text,status=None,parent=None):
        line = QtGui.QLineEdit(parent)
        if status:
            line.setStatusTip(status)
        line.setText(text)
        return line
    def make_comobox(self,status=None,size=None):
        comobox=QtGui.QComboBox(self.centralwidget)
        if size:
            comobox.setMinimumSize(QtCore.QSize(*size))
        if status:
            comobox.setStatusTip(status)
        return comobox
    def make_menu(self):
        menu=self.menuBar()
        for name, items in self.menu_list:
            pulldown=menu.addMenu(name)
            self.addMenuItems(pulldown, items)

    def addMenuItems(self,pulldown, items):
        for item in items:
            command=QtGui.QAction(item[0],self)
            self.connect(command, QtCore.SIGNAL('triggered()'), item[1])
            pulldown.addAction(command)
    def error(self,message):
        self.error_dialog = QtGui.QErrorMessage()
        self.error_dialog.showMessage(message)
