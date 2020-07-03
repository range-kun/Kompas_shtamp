
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
        self.second_name_approv=[]
        self.menu_list= [
        ('File',
         [('Новые настройки', self.onNew),
          ('Загрузить настройки', self.load),  # lambda:0 - пустая операция
          ('Сохранить настройки', self.save),
          ('Сохранить как', self.save_as),
          ('Выйти', sys.exit)])]  # здесь использовать sys, а не self
        self.data=[('constructor',self.second_name_constructor),('checker',self.second_name_checker),
                   ('approver',self.second_name_approv)]
        self.mashtab_list=[	'100:1','50:1','40:1', '20:1','10:1','5:1','4:1','2,5:1','2:1','1:1','1:2','1:2,5', '1:4',
                               '1:5', '1:10', '1:15', '1:20', '1:25','1:40','1:50', '1:75', '1:100', '1:200', '1:400',
                               '1:500', '1:800', '1:1000']

    def setupUi(self, MainWindow):
        MainWindow.resize(500, 494)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.label=self.make_label('Фамилии работников и дата',14)
        self.gridLayout.addWidget(self.label,0, 0, 1, 5)

        self.line = self.make_line('horizontal',2)
        self.gridLayout.addWidget(self.line, 1, 0, 1, 5)


        self.line = self.make_line('horizontal',2)
        self.gridLayout.addWidget(self.line, 6, 0, 1, 5)

        self.line = self.make_line('horizontal',2)
        self.gridLayout.addWidget(self.line, 11, 0, 1, 5)

        #1 линия

        self.comboBox=self.make_combobox("Фамилия конструктора",[110,0])
        self.gridLayout.addWidget(self.comboBox, 2, 0, )

        self.lineEdit=self.make_line_edit('Разработал',"Фамилия конструктора",self.centralwidget)
        self.gridLayout.addWidget(self.lineEdit, 2, 1)

        self.pushButton=self.make_button('Добавить',
                            lambda checked :self.add_item(self.second_name_constructor, self.lineEdit.text(),
                            self.comboBox),[90,16777215])
        self.gridLayout.addWidget(self.pushButton, 2, 2)

        self.pushButton_4 = self.make_button('Удалить',
                            lambda checked :self.del_item(self.second_name_constructor,
                            self.comboBox),[90,16777215])
        self.gridLayout.addWidget(self.pushButton_4, 2, 3)

        self.date=self.make_date(date_par=(1800, 1, 1),parent=self.centralwidget)
        self.gridLayout.addWidget(self.date, 2, 4)

        #2 линия

        self.comboBox_2= self.make_combobox("Фамилия проверяющего", [110, 0])
        self.gridLayout.addWidget(self.comboBox_2, 3, 0)

        self.lineEdit_2=self.make_line_edit('Проверил',"Фамилия проверяющего",self.centralwidget)
        self.gridLayout.addWidget(self.lineEdit_2, 3, 1)

        self.pushButton_2=self.make_button('Добавить',
                            lambda checked :self.add_item(self.second_name_checker, self.lineEdit_2.text(),
                            self.comboBox_2),[90,16777215],)
        self.gridLayout.addWidget(self.pushButton_2, 3, 2)

        self.pushButton_5 = self.make_button('Удалить',
                            lambda checked :self.del_item(self.second_name_checker,
                            self.comboBox_2),[90,16777215])
        self.gridLayout.addWidget(self.pushButton_5, 3, 3)

        self.date_1=self.make_date(date_par=(1800, 1, 1),parent=self.centralwidget)
        self.gridLayout.addWidget(self.date_1, 3, 4)

        #3 линия

        self.comboBox_3= self.make_combobox("Фамилия проверяющего", [110, 0])
        self.gridLayout.addWidget(self.comboBox_3, 4, 0)

        self.lineEdit_3=self.make_line_edit('Утвердил',"Фамилия начальника производства",self.centralwidget)
        self.gridLayout.addWidget(self.lineEdit_3, 4, 1)

        self.pushButton_6=self.make_button('Добавить',
                            lambda checked :self.add_item(self.second_name_approv, self.lineEdit_3.text(),
                            self.comboBox_3),[90,16777215],)
        self.gridLayout.addWidget(self.pushButton_6, 4, 2)

        self.pushButton_7 = self.make_button('Удалить',
                            lambda checked :self.del_item(self.second_name_approv,
                            self.comboBox_3),[90,16777215])
        self.gridLayout.addWidget(self.pushButton_7, 4, 3)

        self.date_2=self.make_date(date_par=(1800, 1, 1),parent=self.centralwidget)
        self.gridLayout.addWidget(self.date_2, 4, 4)


        self.label_2=self.make_label('Основная Надпись и Масштаб',14)
        self.gridLayout.addWidget(self.label_2,5, 0, 1, 5)

        self.detail_number=self.make_plain_text(parent=self.centralwidget,status='обозначение детали')
        self.gridLayout.addWidget(self.detail_number, 7, 0,1,5)

        self.detail_name=self.make_plain_text(parent=self.centralwidget,status='наименование детали')
        self.gridLayout.addWidget(self.detail_name, 8, 0,1,5)

        self.factory_name=self.make_plain_text(parent=self.centralwidget,status='наименование предприятия')
        self.gridLayout.addWidget(self.factory_name, 9, 0,1,5)

        self.mashtab=self.make_combobox("Масштаб",[130,0],self.mashtab_list)
        self.gridLayout.addWidget(self.mashtab, 10, 0, 1, 5)

        self.pushButton_3 = self.make_button('Применить',self.fill_stamp)
        self.gridLayout.addWidget(self.pushButton_3, 12, 0, 1, 5)

        self.make_menu() #создаю меню
        self.statusBar()#создать меню подсказки

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def fill_stamp(self):
        self.config={110:[self.comboBox.currentText(),3.5],111:[self.comboBox_2.currentText(),3.5],
                     115: [self.comboBox_3.currentText(), 3.5],130:[self.get_date_time(),3.5],
                    131:[self.get_date_time(),3.5],135:[self.get_date_time(),3.5],6:[self.mashtab.currentText(),3.5]
                     }
        try:
            for k,v in self.config.items():
                fill_margin(k, v[0], v[1])
        except Exception:
            self.error("Активный 2D документ не найден")

    def get_date_time(self):
        return datetime.datetime.today().strftime("%m.%d")
    def onNew(self):
        self.clear_datat()

    def clear_combo_box(self,list,widget):
        while list:
            self.del_item(list,widget)

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
                try:
                    v[:]=root[k]
                except KeyError:
                    pass
            storage.close()
            self.fill_data()
    def fill_data(self):
        fill_data=[(self.fill_combo_box,[self.second_name_constructor,self.comboBox]),
                   (self.fill_combo_box,[self.second_name_checker,self.comboBox_2]),
                   (self.fill_combo_box,[self.second_name_approv,self.comboBox_3])]
        for name,item in fill_data:
            name(*item)
    def clear_datat(self):
        clear_data=[(self.clear_combo_box,[self.second_name_constructor,self.comboBox]),
                   (self.clear_combo_box,[self.second_name_checker,self.comboBox_2]),
                    (self.clear_combo_box, [self.second_name_approv, self.comboBox_3])
                    ]
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
