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

    def make_line_edit(self,text=None,status=None,parent=None):
        line = QtGui.QLineEdit(parent)
        line.setStatusTip(status)
        line.setPlaceholderText(text)
        return line

    def make_plain_text(self,*,text=None,status=None,parent=None):
        plain_text = QtGui.QPlainTextEdit(parent)
        plain_text.setStatusTip(status)
        plain_text.setPlainText(text)
        return plain_text

    def make_line(self,orientation,width=None):
        line = QtGui.QFrame(self.centralwidget)
        if orientation=='horizontal':
            line.setFrameShape(QtGui.QFrame.HLine)
        elif orientation=='vertical':
            line.setFrameShape(QtGui.QFrame.VLine)
        if width:
            line.setLineWidth(width)
            line.setMidLineWidth(width)
        return line

    def make_label(self,text,font_size=12):
        label = QtGui.QLabel(text,self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        if font_size:
            font.setPointSize(font_size)
        font.setBold(True)
        label.setFont(font)
        label.setAlignment(QtCore.Qt.AlignCenter)
        return label

    def make_date(self,*,date_par,parent=None,status=None):
        date = QtGui.QDateEdit(parent)
        self.set_date(date_par,date)
        date.setStatusTip(status)
        return date
    def set_date(self,date_par,widget):
        widget.setDate(QtCore.QDate(*date_par))

    def make_combobox(self,status=None,size=None,list=None):
        combobox=QtGui.QComboBox(self.centralwidget)
        if size:
            combobox.setMinimumSize(QtCore.QSize(*size))
        if status:
            combobox.setStatusTip(status)
        if list:
            self.fill_combo_box(list,combobox)
        return combobox

    def fill_combo_box(self,list,widget):
        for i in list:
            widget.addItem(i)

    def add_item(self,list,name,widget):
        if all(name.lower()!=i.lower() for i in list):
            name=name.lower().capitalize()
            list.append(name)
            widget.addItem(name)
        else:
            self.error('Имя уже добавлено в список')

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
