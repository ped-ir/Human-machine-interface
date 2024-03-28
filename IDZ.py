from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QPixmap
import pymsgbox
import sys
import math
import matplotlib.pyplot as plt
import numpy as np
import datetime
import time
import threading


Form, Window = uic.loadUiType("idz.ui")
class Ui(QtWidgets.QMainWindow,Form):
    def __init__(self):
        super(Ui,self).__init__()
        self.setupUi(self)
        self.AddButt.clicked.connect(self.AddEdit)
        self.tasks=[]
        self.taskId=0
        self.run=True
    def Err(self,text):
        pymsgbox.alert(title="Ошибка",text=text)
    def  AddEdit(self):
        Edit=self.Edit.toPlainText()
        if len(Edit)==0:
            self.Err("Не введено событие")
            return
        
        date=self.Date.text()
        if len(date)==0:
            D=False
        else:
            D=True
        try:
            promptTime=int(self.Prompts.text())
        except:
            self.Err("не верные даные в поле prompt")
            return
        
        ch=self.prompt.checkState()
        if ch==0:
            prompt=False # not checked
            P=False
            if promptTime!=0:
                self.Err("Prompt не включен, поставте галочку")
        else:
            prompt=True # checked
            P=True
            if promptTime==0:
                self.Err("Не указано время в поле рrompt")
        houre=self.EditTime.time().hour()
        minute=self.EditTime.time().minute()
        T=True
        
        task_time = datetime.datetime.strptime(str(f'{houre}:{minute}'), "%H:%M")
        if not D:    
            self.tasks.append([self.taskId,task_time,0,promptTime,prompt, Edit,D,P,T,True])
        else:
            self.tasks.append([self.taskId,task_time,date,promptTime,prompt, Edit,D,P,T])
        self.__setTaskInTable(self.taskId)

        self.taskId+=1
        
        self.__start_check_tasks_thread()
    
    def __setTaskInTable(self,taskId):
        self.EditsTabel.setRowCount(self.taskId+1)
        task=self.tasks[taskId]
        self.EditsTabel.setItem(taskId, 0, QtWidgets.QTableWidgetItem(str(task[5])))
        self.EditsTabel.setItem(taskId, 1, QtWidgets.QTableWidgetItem(str(task[2])))
        self.EditsTabel.setItem(taskId, 2, QtWidgets.QTableWidgetItem(task[1].strftime("%H:%M")))
        self.EditsTabel.setItem(taskId, 3, QtWidgets.QTableWidgetItem(str(task[3])))
        self.EditsTabel.setItem(taskId, 4, QtWidgets.QTableWidgetItem(str(task[4])))
    
    def check_tasks(self):
        while self.run:
            now = datetime.datetime.now() # get cur time and date
            for tid , task_datetime, date,promptTime,prompt, task_text,D,P,T,comp in self.tasks:
                if not comp:
                    continue
                if D and not P and T: #only date det
                    datetime_object = datetime.datetime.strptime(date, '%d.%m.%y')
                    if now.date()==datetime_object.date():
                        pymsgbox.alert(title="Напоминание",text=task_text)
                        self.tasks[tid][9]=False
                        self.EditsTabel.removeRow(tid)
                        self.EditsTabel.removeRow(tid)
                        continue
                if not D and P and T: #only prompt det
                    if promptTime==0:
                        pymsgbox.alert(title="Напоминание",text=task_text)
                        self.tasks[tid][3]-=1
                        self.tasks[tid][9]=False
                        self.EditsTabel.removeRow(tid)
                        continue
                    else:
                        self.tasks[tid][3]-=1
                if not D and not P and T: # only time det
                    dt1_str = task_datetime.strftime('%H:%M')
                    dt2_str = now.strftime('%H:%M')
                    if dt1_str == dt2_str: 
                        pymsgbox.alert(title="Напоминание",text=task_text)
                        self.tasks[tid][9]=False
                        self.EditsTabel.removeRow(tid)
                        continue
                    
            time.sleep(1)
    
    def __start_check_tasks_thread(self):
        check_tasks_thread = threading.Thread(target=self.check_tasks)
        check_tasks_thread.daemon = True
        check_tasks_thread.start()
        
def main():
    app = QtWidgets.QApplication([])
    window = Ui()
    window.show()
    sys.exit( app.exec())
if __name__=="__main__":
    main()
