
from PyQt4 import QtCore, QtGui
from Widgets_class import MakeWidgets
from Family import fill_margin
import sys, datetime, subprocess

SECOND_NAME_CONSTRUCTOR = ['Головин', 'Дугин']
SECOND_NAME_CHECKER = ['Власов', 'Трусов']

class Ui_MainWindow(MakeWidgets):

    def __init__(self,parent=None):
        MakeWidgets.__init__(self,parent=None)
        self.start()
        self.setupUi(self)
    def start(self):
        self.menu_list= [
        ('File',
         [('Open', lambda: 0),  # lambda:0 - пустая операция
          ('Quit', sys.exit)]),  # здесь использовать sys, а не self
        ('Edit',
         [('Cut', lambda: 0),
          ('Paste', lambda: 0)])]

    def setupUi(self, MainWindow):
        MainWindow.resize(504, 140)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)

        self.lineEdit=self.make_line('Разработал',"Фамилия конструктора",self.centralwidget)
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.comboBox=self.make_comobox(SECOND_NAME_CONSTRUCTOR,"Фамилия конструктора",[130,0])
        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 1)

        self.pushButton=self.make_button('Добавить',
                            lambda checked :self.add_item(SECOND_NAME_CONSTRUCTOR, self.lineEdit.text(),
                            self.comboBox),[90,16777215])
        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)

        self.pushButton_4 = self.make_button('Удалить',
                            lambda checked :self.del_item(SECOND_NAME_CONSTRUCTOR,
                            self.comboBox),[90,16777215])
        self.gridLayout.addWidget(self.pushButton_4, 0, 3)

        self.lineEdit_2=self.make_line('Проверил',"Фамилия проверяющего",self.centralwidget)
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)

        self.comboBox_2= self.make_comobox(SECOND_NAME_CHECKER, "Фамилия проверяющего", [130, 0])
        self.gridLayout.addWidget(self.comboBox_2, 1, 0, 1, 1)

        self.pushButton_2=self.make_button('Добавить',
                            lambda checked :self.add_item(SECOND_NAME_CHECKER, self.lineEdit_2.text(),
                            self.comboBox_2),[90,16777215],)
        self.gridLayout.addWidget(self.pushButton_2, 1, 2, 1, 1)

        self.pushButton_5 = self.make_button('Удалить',
                            lambda checked :self.del_item(SECOND_NAME_CHECKER,
                            self.comboBox_2),[90,16777215])
        self.gridLayout.addWidget(self.pushButton_5, 1, 3)

        self.pushButton_3 = self.make_button('Применить',self.fill_stamp)
        self.gridLayout.addWidget(self.pushButton_3, 2, 2, 1, 1)

        self.make_menu() #создаю меню
        self.statusBar()

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def fill_stamp(self):
        self.config={110:[self.comboBox.currentText(),3.5],111:[self.comboBox_2.currentText(),3.5],
                     130:[self.get_date(),3.5],131:[self.get_date(),3.5]}
        try:
            for k,v in self.config.items():
                fill_margin(k, v[0], v[1])
                print(k,v[0],v[1])
        except Exception:
            self.error("Активный документ не найден")

    def get_date(self):
        return datetime.datetime.today().strftime("%m.%d")
    def add_item(self,list,name,widget):
        if all(name.lower()!=i.lower() for i in list):
            name=name.lower().capitalize()
            list.append(name)
            widget.addItem(name)
        else:
            self.error('Имя уже добавлено в список')
    def del_item(self,list,widget):
        index=list.index(widget.currentText())
        list.remove(widget.currentText())
        widget.removeItem(index)


def is_running(process_name):
    call = 'TASKLIST','/NH', '/FI', 'imagename eq %s' % process_name
    output = subprocess.check_output(call).decode('cp866')
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(process_name.lower()[:-1])


if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    if is_running('KOMPAS*'):
         proba = Ui_MainWindow()
         proba.show()
    else:
        error=QtGui.QErrorMessage()
        error.showMessage('KOMPAS не запушен')
    sys.exit(app.exec_())
