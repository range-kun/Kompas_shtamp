
from _datetime import datetime
import pythoncom
import subprocess
import sys
import transaction
import os

from PyQt4 import QtCore, QtGui
from ZODB import FileStorage, DB
from Widgets_class import MakeWidgets
from Family import fill_margin, get_kompas_api5


class Ui_MainWindow(MakeWidgets):

    def __init__(self,parent=None):
        MakeWidgets.__init__(self,parent=None)
        self.start()
        self.setupUi(self)
    def start(self):
        self.curfile=None
        self.date_today=[int(i) for i in str(datetime.date(datetime.now())).split('-')]
        self.date_list,self.date_list1,self.date_list2=[],[],[]
        self.second_name_constructor =[]
        self.second_name_checker=[]
        self.second_name_approv=[]
        self.menu_list= [
                        ('File',
                         [('Новые настройки', self.onNew),
                          ('Загрузить настройки', self.load),
                          ('Сохранить настройки', self.save),
                          ('Сохранить как', self.save_as),
                          ('Выйти', sys.exit)])]
        self.data_save=[('constructor',self.second_name_constructor),('checker',self.second_name_checker),
                        ('approver',self.second_name_approv),('construscor_date',lambda: self.date_to_list(self.date_list,self.date)),
                        ('chceker_date',lambda: self.date_to_list(self.date_list1,self.date_1)),
                        ('approv_date', lambda: self.date_to_list(self.date_list2, self.date_2)),
                        ('detail_number',lambda:self.detail_number.toPlainText()),('detail_name',lambda:self.detail_name.toPlainText()),
                        ('factory_name',lambda:self.factory_name.toPlainText()),
                        ('scale',lambda: self.scale.currentIndex())]
        self.data_load=[('constructor',self.second_name_constructor),('checker',self.second_name_checker),
                        ('approver',self.second_name_approv),('construscor_date',self.date_list),
                        ('chceker_date',self.date_list1 ),('approv_date',self.date_list2),
                        ('detail_number',lambda k: self.detail_number.setPlainText(k)),
                        ('detail_name',lambda k:self.detail_name.setPlainText(k)),
                        ('factory_name',lambda k :self.factory_name.setPlainText(k)),('scale',lambda k: self.scale.setCurrentIndex(k))]
        self.scale_list=['100:1','50:1','40:1', '20:1','10:1','5:1','4:1','2,5:1','2:1','1:1','1:2','1:2,5', '1:4',
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

        ######## 1 линия ########

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

        self.date=self.make_date(date_par=self.date_today,parent=self.centralwidget,
                                 status='По умолчанию устанавливается текущая дата')
        self.gridLayout.addWidget(self.date, 2, 4)

        ######## 2 линия ########

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

        self.date_1=self.make_date(date_par=self.date_today,parent=self.centralwidget,
                                   status='По умолчанию устанавливается текущая дата')
        self.gridLayout.addWidget(self.date_1, 3, 4)

        ########3 линия ########

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

        self.date_2=self.make_date(date_par=self.date_today,parent=self.centralwidget,
                                   status='По умолчанию устанавливается текущая дата')
        self.gridLayout.addWidget(self.date_2, 4, 4)


        self.label_2=self.make_label('Основная Надпись и Масштаб',14)
        self.gridLayout.addWidget(self.label_2,5, 0, 1, 5)

        self.detail_number=self.make_plain_text(parent=self.centralwidget,status='обозначение детали')
        self.gridLayout.addWidget(self.detail_number, 7, 0,1,5)

        self.detail_name=self.make_plain_text(parent=self.centralwidget,status='наименование детали')
        self.gridLayout.addWidget(self.detail_name, 8, 0,1,5)

        self.factory_name=self.make_plain_text(parent=self.centralwidget,status='наименование предприятия')
        self.gridLayout.addWidget(self.factory_name, 9, 0,1,5)

        self.scale=self.make_combobox("Масштаб",[130,0],self.scale_list)
        self.scale.setCurrentIndex(9)
        self.gridLayout.addWidget(self.scale, 10, 0, 1, 5)

        self.pushButton_3 = self.make_button('Применить',self.fill_stamp)
        self.gridLayout.addWidget(self.pushButton_3, 12, 0, 1, 5)

        self.make_menu() #создаю меню
        self.statusBar()#создать меню подсказки

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def fill_stamp(self):
        self.config={110:[self.comboBox.currentText(),3.5],111:[self.comboBox_2.currentText(),3.5],
                     115: [self.comboBox_3.currentText(), 3.5],130:[self.get_date_time(self.date),3.5],
                    131:[self.get_date_time(self.date_1),3.5],135:[self.get_date_time(self.date_2),3.5],
                     6:[self.scale.currentText(),3.5,],1:[self.detail_name.toPlainText(),7],
                     2:[self.detail_number.toPlainText(),7],9:[self.factory_name.toPlainText(),7]
                     }
        try:
            for k,v in self.config.items():
                fill_margin(k, v[0], v[1])
        except Exception:
            self.error("Активный 2D документ не найден")

    def get_date_time(self,date):
        return date.dateTime().toString('dd.MM')
    def onNew(self):
        self.curfile=None
        self.clear_data()

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
            self.clear_data()
            self.curfile=filename
            root,storage=self.open_storage(filename)
            for k,v in self.data_load:
                try:
                    v[:]=root[k]
                except TypeError:
                    v(root[k])
                except KeyError:
                    print(k,' data missing')
            storage.close()
            self.fill_data()
    def save(self):
        self.save_as(self.curfile)

    def save_as(self,file=None):
        filename = file or QtGui.QFileDialog.getSaveFileName(self, "Сохранить файл", ".",
                                                                "FileStorage(*.fs)")
        if filename:
            root, storage = self.open_storage(filename)
            for k, v in self.data_save:
                if type(v)==list:
                    root[k] = v
                else:
                    root[k] = v()
            transaction.commit()
            storage.close()
    def fill_data(self):
        fill_data=[(self.fill_combo_box,[self.second_name_constructor,self.comboBox]),
                   (self.fill_combo_box,[self.second_name_checker,self.comboBox_2]),
                   (self.fill_combo_box,[self.second_name_approv,self.comboBox_3]),
                   (self.set_date, [self.date_list,self.date]),(self.set_date, [self.date_list1,self.date_1]),
                   (self.set_date, [self.date_list2, self.date_2])]
        for name,item in fill_data:
            name(*item)
    def clear_data(self):
        clear_data=[(self.clear_combo_box,[self.second_name_constructor,self.comboBox]),
                    (self.clear_combo_box,[self.second_name_checker,self.comboBox_2]),
                    (self.clear_combo_box, [self.second_name_approv, self.comboBox_3]),
                    (self.set_date,[self.date_today,self.date]),(self.set_date, [self.date_today,self.date_1]),
                    (self.set_date, [self.date_today, self.date_2]),(self.detail_number.clear,[]),
                    (self.detail_name.clear,[]), (self.factory_name.clear,[]),(self.scale.setCurrentIndex,[9])]
        for name, item in clear_data:
            name(*item)
    def date_to_list(self,list,date):
        list=[int(i) for i in date.dateTime().toString('yyyy.MM.dd').split('.')]
        return list
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
    try:
        pythoncom.connect('Kompas.Application.5')  # Проверка запущен ли КОМПАС
        print('Компас запущен')
    except:
        messagebox = QtGui.QMessageBox
        qt=messagebox.question(None, '', "Компас 3D не запущен. \nЗапустить данную программу?", messagebox.Yes | messagebox.No)
        if qt==messagebox.Yes:
            module_5, kompas_object, const_5 = get_kompas_api5()
            kompas_object.Visible = True
            proba=Ui_MainWindow()
            proba.show()
            print('done')
    else:
        proba = Ui_MainWindow()
        proba.show()
    sys.exit(app.exec_())
