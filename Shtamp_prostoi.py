
import datetime
import subprocess
import sys
import shelve
import transaction

from PyQt4 import QtCore, QtGui
from ZODB import FileStorage, DB
from Widgets_class import MakeWidgets
from Family import fill_margin


class Ui_MainWindow(MakeWidgets):

    def __init__(self,parent=None):
        MakeWidgets.__init__(self,parent=None)
        self.start()
        self.setupUi(self)
    def start(self):
        self.second_name_constructor =[]
        self.second_name_checker=[]
        self.menu_list= [
        ('File',
         [('Новые настройки', self.onNew),
          ('Загрузить настройки', self.load),  # lambda:0 - пустая операция
          ('Сохранить настройки', self.save),
          ('Сохранить как', self.save_as),
          ('Выйти', sys.exit)])]  # здесь использовать sys, а не self
        self.data=[('constructor',self.second_name_constructor),
                   ('checker',self.second_name_checker)]

    def setupUi(self, MainWindow):
        MainWindow.resize(504, 140)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)

        self.lineEdit=self.make_line('Разработал',"Фамилия конструктора",self.centralwidget)
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.comboBox=self.make_comobox("Фамилия конструктора",[130,0])
        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 1)

        self.pushButton=self.make_button('Добавить',
                            lambda checked :self.add_item(self.second_name_constructor, self.lineEdit.text(),
                            self.comboBox),[90,16777215])
        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)

        self.pushButton_4 = self.make_button('Удалить',
                            lambda checked :self.del_item(self.second_name_constructor,
                            self.comboBox),[90,16777215])
        self.gridLayout.addWidget(self.pushButton_4, 0, 3)

        self.lineEdit_2=self.make_line('Проверил',"Фамилия проверяющего",self.centralwidget)
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)

        self.comboBox_2= self.make_comobox("Фамилия проверяющего", [130, 0])
        self.gridLayout.addWidget(self.comboBox_2, 1, 0, 1, 1)

        self.pushButton_2=self.make_button('Добавить',
                            lambda checked :self.add_item(self.second_name_checker, self.lineEdit_2.text(),
                            self.comboBox_2),[90,16777215],)
        self.gridLayout.addWidget(self.pushButton_2, 1, 2, 1, 1)

        self.pushButton_5 = self.make_button('Удалить',
                            lambda checked :self.del_item(self.second_name_checker,
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
                     130:[self.get_date_time(),3.5],131:[self.get_date_time(),3.5]}
        try:
            for k,v in self.config.items():
                fill_margin(k, v[0], v[1])
        except Exception:
            self.error("Активный 2D документ не найден")

    def get_date_time_tame(self):
        return datetime.datetime.today().strftime("%m.%d")
    def onNew(self):
        self.clear_datat()

    def fill_como_box(self,list,widget):
        for i in list:
            widget.addItem(i)
    def clear_combo_box(self,list,widget):
        while list:
            self.del_item(list,widget)

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

    def load(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,"Выбрать файл",".",
                             "FileStorage(*.fs);;All Files(*.*)")
        if filename:
            self.clear_datat()
            self.curfile=filename
            root,storage=self.open_storage(filename)
            for k,v in self.data:
                v[:]=root[k]
            storage.close()
            self.fill_data()
    def fill_data(self):
        fill_data=[(self.fill_como_box,[self.second_name_constructor,self.comboBox]),
                   (self.fill_como_box,[self.second_name_checker,self.comboBox_2])]
        for name,item in fill_data:
            name(*item)
    def clear_datat(self):
        clear_data=[(self.clear_combo_box,[self.second_name_constructor,self.comboBox]),
                   (self.clear_combo_box,[self.second_name_checker,self.comboBox_2])]
        for name, item in clear_data:
            name(*item)

    def save(self):
        self.save_as(self.curfile)

    def save_as(self,file=None):
        filename = file or QtGui.QFileDialog.getSaveFileName(self, "Сохранить файл", ".",
                                                     "FileStorage(*.fs)")
        if filename:
            root, storage = self.open_storage(filename)
            for k, v in self.data:
                root[k] = v
            transaction.commit()
            storage.close()
    def open_storage(self,filename):
        storage = FileStorage.FileStorage(filename)
        db = DB(storage)
        connection = db.open()
        root = connection.root()
        return root,storage


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
