'''
    This file is part of meisterPlotter.

    meisterPlotter is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    meisterPlotter is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with meisterPlotter.  If not, see <https://www.gnu.org/licenses/>.
'''

__title__ = 'meisterPlotter'
__version__ = '0.1b'
__author__ = 'Kekollons'
__license__ = 'GPLv3'
__copyright__ = 'Esta obra está licenciada bajo la Licencia Creative Commons Atribución-NoComercial-SinDerivadas 4.0 Internacional.Para ver una copia de esta licencia, visite http://creativecommons.org/licenses/by-nc-nd/4.0/ o envíe una carta a Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.'

import sys, os, time
import subprocess
import psutil
import json
import chiainfo, newplot

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt6.QtCore import QTimer, QObject, QThread, QThreadPool, pyqtSignal, QDateTime

rutatxt = open ('rutaChia.txt','r')
ruta_chia = rutatxt.read()

python3_path = 'python' 
newplotfile = 'newplot.cfg' 
estado_nodo, estado_cartera, estado_granja = '', '', ''
dinero = ['0', '0', '0']
plotsdirectory = []
llavero = ['', '']
comprobar_cambio = []

class ConsultarEstado(QObject):
    finished = pyqtSignal()
    #signal_nodo = pyqtSignal(str)
    #signal_cartera = pyqtSignal(str)
    #signal_granja = pyqtSignal(str)
    #signal_dinero = pyqtSignal(list)
    
    def run(self):
        global estado_nodo, estado_cartera, estado_granja, dinero, plotsdirectory, llavero
        try:
            estado_nodo, estado_cartera, estado_granja, dinero, plotsdirectory, llavero = chiainfo.info()
        #self.signal_nodo.emit(estado_nodo)
        #self.signal_cartera.emit(estado_cartera)
        #self.signal_granja.emit(estado_granja)
        #self.signal_dinero.emit(dinero)
            self.finished.emit()
        except:
            pass
        
class Principal(QMainWindow):
    
    def __init__(self):
        super().__init__()
        uic.loadUi('principal.ui', self)
        self.comprobar_hardware()
        self.dt_startat.setDateTime(QDateTime.currentDateTime())
        
        self.timer = QTimer()
        self.timer.setInterval(7000)
        self.timer.timeout.connect(self.update_info)    
        self.timer.start()
        
        self.thread = QThread()
        self.thread_estado = ConsultarEstado()
        self.thread_estado.moveToThread(self.thread)
        self.thread.started.connect(self.thread_estado.run)
        self.thread_estado.finished.connect(self.thread.quit)
        self.thread.start()

    def comprobar_hardware(self):
        hilos = psutil.cpu_count(logical=True)
        hilos_list = list(range(hilos))
        # memoria = psutil.virtual_memory()
        for hilo in hilos_list:
            self.cmb_hilos.addItem(str(hilo+1))
            
    def update_info(self):
        global comprobar_cambio

        if plotsdirectory == comprobar_cambio:
            pass
        else:
            self.txt_plotdir.clear()
            for direc in plotsdirectory:
                self.txt_plotdir.append(direc)
            comprobar_cambio = plotsdirectory
        
        self.lbl_estado_bc.setText(estado_nodo)
        self.lbl_estado_granja.setText(estado_granja)
        self.lbl_estado_cartera.setText(estado_cartera)
        
        self.lbl_totalxch.setText('Total: ' + dinero[0])
        self.lbl_spendablexch.setText('Spendable: ' + dinero[2])
        self.lbl_pendingxch.setText('Pending: ' + dinero[1])
        
        self.thread.start()
        
        if estado_nodo == 'Sincronizado':
            self.lbl_estado_bc.setStyleSheet("background-color: limegreen; border: 1px solid black;")
        elif estado_nodo == 'No sincronizado':
            self.lbl_estado_bc.setStyleSheet("background-color: orange; border: 1px solid black;")
        else:
            #estado_nodo = 'ERROR'
            self.lbl_estado_bc.setStyleSheet("background-color: red; border: 1px solid black;")
        
        if estado_granja == 'Farmeando':
            self.lbl_estado_granja.setStyleSheet("background-color: limegreen; border: 1px solid black;")
        elif estado_granja == 'Sincronizando':
            self.lbl_estado_granja.setStyleSheet("background-color: gold; border: 1px solid black;")
        elif estado_granja == 'No sincronizado':
            self.lbl_estado_granja.setStyleSheet("background-color: orange; border: 1px solid black;")
        else:
            #estado_granja = 'ERROR'
            self.lbl_estado_granja.setStyleSheet("background-color: red; border: 1px solid black;")

        if estado_cartera == 'Sincronizado':
            self.lbl_estado_cartera.setStyleSheet("background-color: limegreen; border: 1px solid black;")
        elif estado_cartera == 'No sincronizado':
            self.lbl_estado_cartera.setStyleSheet("background-color: orange; border: 1px solid black;")
        else:
            #estado_cartera = 'ERROR'
            self.lbl_estado_cartera.setStyleSheet("background-color: red; border: 1px solid black;")
        
    def clk_btn_iniciar(self):
        subprocess.run(['start', 'cmd', '/k', 'chia', 'start', 'all'], cwd=ruta_chia, shell=True)
    
    def clk_btn_reiniciar(self):
        subprocess.run(['start', 'cmd', '/k', 'chia', 'start', 'farmer', '-r'], cwd=ruta_chia, shell=True)
        
    def clk_btn_parar(self):
        subprocess.run(['start', 'cmd', '/k', 'chia', 'stop', 'all'], cwd=ruta_chia, shell=True)
        
    def clk_btn_matarprocesos(self):
        subprocess.run(['start', 'cmd', '/k', 'chiakillprocess.bat'], shell=True)
        
    def clk_cmb_parallel_plots(self):
        valor = self.cmb_plots_paralelo.currentIndex() + 1 
        self.spin_plots_total.setMinimum(valor)
        
        self.spin_sched_2.setEnabled(True)
        self.spin_sched_3.setEnabled(False)
        self.spin_sched_4.setEnabled(False)
        self.spin_sched_5.setEnabled(False)
        self.spin_sched_6.setEnabled(False)
        self.spin_sched_7.setEnabled(False)
        self.spin_sched_8.setEnabled(False)
        self.spin_sched_9.setEnabled(False)
        self.spin_sched_10.setEnabled(False)
        self.spin_sched_11.setEnabled(False)
        self.spin_sched_12.setEnabled(False)
        if valor == 2:
            self.spin_sched_2.setEnabled(True)
            self.spin_sched_3.setEnabled(False)
            self.spin_sched_4.setEnabled(False)
            self.spin_sched_5.setEnabled(False)
            self.spin_sched_6.setEnabled(False)
            self.spin_sched_7.setEnabled(False)
            self.spin_sched_8.setEnabled(False)
            self.spin_sched_9.setEnabled(False)
            self.spin_sched_10.setEnabled(False)
            self.spin_sched_11.setEnabled(False)
            self.spin_sched_12.setEnabled(False)
        elif valor == 3:
            self.spin_sched_2.setEnabled(True)
            self.spin_sched_3.setEnabled(True)
            self.spin_sched_4.setEnabled(False)
            self.spin_sched_5.setEnabled(False)
            self.spin_sched_6.setEnabled(False)
            self.spin_sched_7.setEnabled(False)
            self.spin_sched_8.setEnabled(False)
            self.spin_sched_9.setEnabled(False)
            self.spin_sched_10.setEnabled(False)
            self.spin_sched_11.setEnabled(False)
            self.spin_sched_12.setEnabled(False)
        elif valor == 4:
            self.spin_sched_2.setEnabled(True)
            self.spin_sched_3.setEnabled(True)
            self.spin_sched_4.setEnabled(True)
            self.spin_sched_5.setEnabled(False)
            self.spin_sched_6.setEnabled(False)
            self.spin_sched_7.setEnabled(False)
            self.spin_sched_8.setEnabled(False)
            self.spin_sched_9.setEnabled(False)
            self.spin_sched_10.setEnabled(False)
            self.spin_sched_11.setEnabled(False)
            self.spin_sched_12.setEnabled(False)
        elif valor == 5:
            self.spin_sched_2.setEnabled(True)
            self.spin_sched_3.setEnabled(True)
            self.spin_sched_4.setEnabled(True)
            self.spin_sched_5.setEnabled(True)
            self.spin_sched_6.setEnabled(False)
            self.spin_sched_7.setEnabled(False)
            self.spin_sched_8.setEnabled(False)
            self.spin_sched_9.setEnabled(False)
            self.spin_sched_10.setEnabled(False)
            self.spin_sched_11.setEnabled(False)
            self.spin_sched_12.setEnabled(False)
        elif valor == 6:
            self.spin_sched_2.setEnabled(True)
            self.spin_sched_3.setEnabled(True)
            self.spin_sched_4.setEnabled(True)
            self.spin_sched_5.setEnabled(True)
            self.spin_sched_6.setEnabled(True)
            self.spin_sched_7.setEnabled(False)
            self.spin_sched_8.setEnabled(False)
            self.spin_sched_9.setEnabled(False)
            self.spin_sched_10.setEnabled(False)
            self.spin_sched_11.setEnabled(False)
            self.spin_sched_12.setEnabled(False)
        elif valor == 7:
            self.spin_sched_2.setEnabled(True)
            self.spin_sched_3.setEnabled(True)
            self.spin_sched_4.setEnabled(True)
            self.spin_sched_5.setEnabled(True)
            self.spin_sched_6.setEnabled(True)
            self.spin_sched_7.setEnabled(True)
            self.spin_sched_8.setEnabled(False)
            self.spin_sched_9.setEnabled(False)
            self.spin_sched_10.setEnabled(False)
            self.spin_sched_11.setEnabled(False)
            self.spin_sched_12.setEnabled(False)
        elif valor == 8:
            self.spin_sched_2.setEnabled(True)
            self.spin_sched_3.setEnabled(True)
            self.spin_sched_4.setEnabled(True)
            self.spin_sched_5.setEnabled(True)
            self.spin_sched_6.setEnabled(True)
            self.spin_sched_7.setEnabled(True)
            self.spin_sched_8.setEnabled(True)
            self.spin_sched_9.setEnabled(False)
            self.spin_sched_10.setEnabled(False)
            self.spin_sched_11.setEnabled(False)
            self.spin_sched_12.setEnabled(False)
        elif valor == 9:
            self.spin_sched_2.setEnabled(True)
            self.spin_sched_3.setEnabled(True)
            self.spin_sched_4.setEnabled(True)
            self.spin_sched_5.setEnabled(True)
            self.spin_sched_6.setEnabled(True)
            self.spin_sched_7.setEnabled(True)
            self.spin_sched_8.setEnabled(True)
            self.spin_sched_9.setEnabled(True)
            self.spin_sched_10.setEnabled(False)
            self.spin_sched_11.setEnabled(False)
            self.spin_sched_12.setEnabled(False)
        elif valor == 10:
            self.spin_sched_2.setEnabled(True)
            self.spin_sched_3.setEnabled(True)
            self.spin_sched_4.setEnabled(True)
            self.spin_sched_5.setEnabled(True)
            self.spin_sched_6.setEnabled(True)
            self.spin_sched_7.setEnabled(True)
            self.spin_sched_8.setEnabled(True)
            self.spin_sched_9.setEnabled(True)
            self.spin_sched_10.setEnabled(True)
            self.spin_sched_11.setEnabled(False)
            self.spin_sched_12.setEnabled(False)
        elif valor == 11:
            self.spin_sched_2.setEnabled(True)
            self.spin_sched_3.setEnabled(True)
            self.spin_sched_4.setEnabled(True)
            self.spin_sched_5.setEnabled(True)
            self.spin_sched_6.setEnabled(True)
            self.spin_sched_7.setEnabled(True)
            self.spin_sched_8.setEnabled(True)
            self.spin_sched_9.setEnabled(True)
            self.spin_sched_10.setEnabled(True)
            self.spin_sched_11.setEnabled(True)
            self.spin_sched_12.setEnabled(False)
        elif valor == 12:
            self.spin_sched_2.setEnabled(True)
            self.spin_sched_3.setEnabled(True)
            self.spin_sched_4.setEnabled(True)
            self.spin_sched_5.setEnabled(True)
            self.spin_sched_6.setEnabled(True)
            self.spin_sched_7.setEnabled(True)
            self.spin_sched_8.setEnabled(True)
            self.spin_sched_9.setEnabled(True)
            self.spin_sched_10.setEnabled(True)
            self.spin_sched_11.setEnabled(True)
            self.spin_sched_12.setEnabled(True)
        else:
            pass
    
    def clk_rb_startat(self):
        if self.rb_startat.isChecked():
            self.dt_startat.setEnabled(True)
        else:
            self.dt_startat.setEnabled(False)
            
    def clk_btn_tempdir1(self):
        try:
            self.temp_dir1 = QFileDialog.getExistingDirectory(self,"Choose Temporary 1 Directory","C:\\")
            self.line_tempdir1.setText(self.temp_dir1)
        except:
            pass
    
    def clk_btn_tempdir2(self):
        try:
            self.temp_dir2 = QFileDialog.getExistingDirectory(self,"Choose Temporary 2 Directory","C:\\")
            self.line_tempdir2.setText(self.temp_dir2)
        except:
            pass
        
    def clk_btn_addfinaldir(self):
        try:
            self.final_dir = QFileDialog.getExistingDirectory(self,"Choose Final Directory","C:\\")
            self.txt_finaldir.append(self.final_dir)
        except:
            pass
            
    def clk_btn_rmvfinaldir(self):
        try:
            self.txt_finaldir.clear()
        except:
            pass
    
    def clk_addplotdir(self):
        try:
            self.addplot_dir = QFileDialog.getExistingDirectory(self,"Add Plot Directory","C:\\")
            subprocess.run(['chia', 'plots', 'add', '-d', self.addplot_dir], cwd=ruta_chia, shell=True)
        except:
            pass
        
    def clk_rmvplotdir(self):
        try:
            self.rmvplot_dir = QFileDialog.getExistingDirectory(self,"Remove Plot Directory","C:\\")
            if self.rmvplot_dir == "":
                pass
            else:
                subprocess.run(['chia', 'plots', 'remove', '-d', self.rmvplot_dir], cwd=ruta_chia, shell=True)
        except:
            pass
    
    def crear_data(self):
        finaldirs = self.txt_finaldir.toPlainText()
        finaldirs = finaldirs.split('\n')
        data = {}
        data['cfg'] = []
        data['cfg'].append({
            'k': self.cmb_k.currentIndex(),
            'inparallel': self.cmb_plots_paralelo.currentIndex(),
            'queue': self.spin_plots_total.value(),
            'threads': self.cmb_hilos.currentIndex(),
            'ram': self.spin_ram.value(),
            'bitfield': self.chk_bitfield.isChecked(),
            'excludefinaldir': self.chk_excludefinal.isChecked(),
            'tempdir1': self.line_tempdir1.text(),
            'tempdir2': self.line_tempdir2.text(),
            'finaldirs': finaldirs,
            'autosched': self.chk_autosched.isChecked(),
            'relativetimes': self.chk_relative.isChecked(),
            'startat': self.rb_startat.isChecked(),
            'datetime': self.dt_startat.dateTime().toString("yyyy/MM/dd  HH:mm:ss"),
            'delay2': self.spin_sched_2.value(),
            'delay3': self.spin_sched_3.value(),
            'delay4': self.spin_sched_4.value(),
            'delay5': self.spin_sched_5.value(),
            'delay6': self.spin_sched_6.value(),
            'delay7': self.spin_sched_7.value(),
            'delay8': self.spin_sched_8.value(),
            'delay9': self.spin_sched_9.value(),
            'delay10': self.spin_sched_10.value(),
            'delay11': self.spin_sched_11.value(),
            'delay12': self.spin_sched_12.value(),
            'farmerkey': self.line_farmer_pkey.text(),
            'poolkey': self.line_pool_pkey.text(),
        })
        
        return data
    
    def clk_btn_plotting(self):
        try:
            finaldirs = self.txt_finaldir.toPlainText()
            finaldirs = finaldirs.split('\n')
        
            letter_dir = []
            total_free = 0
    
            for ruta in finaldirs:
                letter_dir.append(ruta[0:2])
    
            for letra in letter_dir:
                hdd = psutil.disk_usage(letra)
                total_free = total_free + (((hdd.free // (2**30))) // 102)
        
            self.spin_plots_total.setMaximum(total_free)
        
            data = self.crear_data()
            with open('newplot.newplot', 'w') as iparam:
                json.dump(data, iparam)
            subprocess.run(['start', 'cmd', '/k', python3_path, 'newplot.py'], shell=True)
        except:
            print('Error in final directory')
        
    def clk_btn_savcfg(self):
        self.save_file = QFileDialog.getSaveFileName(self,"Choose Save File", "harryplotter.cfg")
        savedata = self.crear_data()
        try:
            with open(self.save_file[0], 'w') as fparam:
                json.dump(savedata, fparam)
        except:
            pass
        
    def clk_btn_loadcfg(self):
        self.load_file = QFileDialog.getOpenFileName(self, "Choose Load File")
        try:
            with open(self.load_file[0]) as json_file:
                loaddata = json.load(json_file)
                for param in loaddata['cfg']:
                    k = param['k']
                    inparallel = param['inparallel']
                    queue = param['queue']
                    threads = param['threads']
                    ram = param['ram']
                    bitfield = param['bitfield']
                    excludefinaldir = param['excludefinaldir']
                    tempdir1 = param['tempdir1']
                    tempdir2 = param['tempdir2']
                    autosched = param['autosched']
                    relativetimes = param['relativetimes']
                    #startat = param['startat']
                    #datetime = param['datetime']
                    delay2 = param['delay2']
                    delay3 = param['delay3']
                    delay4 = param['delay4']
                    delay5 = param['delay5']
                    delay6 = param['delay6']
                    delay7 = param['delay7']
                    delay8 = param['delay8']
                    delay9 = param['delay9']
                    delay10 = param['delay10']
                    delay11 = param['delay11']
                    delay12 = param['delay12']
                    farmerkey = param['farmerkey']
                    poolkey = param['poolkey']
                
            self.cmb_k.setCurrentIndex(k)
            self.cmb_plots_paralelo.setCurrentIndex(inparallel)
            self.spin_plots_total.setValue(queue)
            self.cmb_hilos.setCurrentIndex(threads)
            self.spin_ram.setValue(ram)
            self.chk_bitfield.setChecked(bitfield)
            self.chk_excludefinal.setChecked(excludefinaldir)
            self.line_tempdir1.setText(tempdir1)
            self.line_tempdir2.setText(tempdir2)
            self.chk_autosched.setChecked(autosched)
            self.chk_relative.setChecked(relativetimes)
            #self.rb_startat.setChecked(startat)
            #self.dt_startat.setDateTime().fromString(dateTime)
            self.spin_sched_2.setValue(delay2)
            self.spin_sched_3.setValue(delay3)
            self.spin_sched_4.setValue(delay4)
            self.spin_sched_5.setValue(delay5)
            self.spin_sched_6.setValue(delay6)
            self.spin_sched_7.setValue(delay7)
            self.spin_sched_8.setValue(delay8)
            self.spin_sched_9.setValue(delay9)
            self.spin_sched_10.setValue(delay10)
            self.spin_sched_11.setValue(delay11)
            self.spin_sched_12.setValue(delay12)
            self.line_farmer_pkey.setText(farmerkey)
            self.line_pool_pkey.setText(poolkey)
        except:
            print('Error to open config file')
                 
def main():
    app = QApplication(sys.argv)
    vent_principal = Principal()
    vent_principal.show()
    sys.exit(app.exec())
    
if __name__ == '__main__':
    main()