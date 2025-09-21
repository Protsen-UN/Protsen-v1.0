import sys, time,threading
from Bluethoot import Bluethoot
from Map import MapHeat

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog,  QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.uic import loadUi
from pyvistaqt import QtInteractor, BackgroundPlotter

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('diseno.ui', self)
	
        self.update = True

        self.dialog = Dialog() 
        self.Error = Dialog()

        self.Blue = Bluethoot()
        self.DataSensors = []

        self.Blue.SetConection(False)

        self.munon = MapHeat()
        self.munon.ObtainHeatValue2()
        self.munon.SetZone1(100)
        self.munon.change_neighbors(1211, 0, 200)
        self.munon.change_neighbors(1096, 0, 200)
        self.munon.change_neighbors(1256, 0, 300)
        self.munon.change_neighbors(1148, 0, 400)
        '''self.munon.change_neighbors(6077, 0, 1500)
        self.munon.change_neighbors(6909, 0, 4000)
        self.munon.change_neighbors(5597, 0, 4000)
        self.munon.change_neighbors(6554, 0, 5000)'''
        self.munon.AddMesh()
        self.munon.AddScalarBar()
        self.Plotter_data = self.munon.GetPlotter()

        #Widget de impresion 3D para desarrollo
        """vlayout = QtWidgets.QVBoxLayout()
        self.plotter = QtInteractor(self.frame_contenido)
        vlayout.addWidget(self.plotter.interactor)
        self.frame_contenido.setLayout(vlayout)
        self.plotter.add_mesh(self.Plotter_data, show_edges=True)
        self.plotter.reset_camera()"""

        #Botones de conexion
        self.bt_conectar.clicked.connect(self.control_bt_conectar)
        self.bt_conectar.clicked.connect(self.iniciar_hilo)
        self.bt_desconectar.clicked.connect(self.control_bt_desconectar)
        self.bt_reconectar.clicked.connect(self.control_bt_reconectar)
        self.bt_reconectar.clicked.connect(self.iniciar_hilo)
        
		# mover ventana
        self.frame_Logo.mouseMoveEvent = self.mover_ventana
        self.frame_control.mouseMoveEvent = self.mover_ventana

		#control barra de titulos
        self.bt_minimizar.clicked.connect(self.control_bt_minimizar)		
        self.bt_restaurar.clicked.connect(self.control_bt_normal)
        self.bt_maximizar.clicked.connect(self.control_bt_maximizar)
        self.bt_cerrar.clicked.connect(lambda: self.close())

        self.bt_restaurar.hide()

        #eliminar barra y de titulo - opacidad
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        #self.label_contenido.hide()
        
        #Imagen obejto 3D

    def control_bt_conectar(self):

        try:
            self.Blue.GenerateConection()
            self.Blue.SetConection(True)
           
        except OSError:
            if self.Blue.GetConection() == False:
                self.show_dialog()

    def control_bt_desconectar(self):

        self.Blue.SetConection(False)    

    def control_bt_reconectar(self):
            
        self.Blue.SetConection(True)

    def control_bt_minimizar(self):
        self.showMinimized()		

    def  control_bt_normal(self):
        self.setStyleSheet("background-color:#000000ff")
        self.setAutoFillBackground(True); 
        self.showNormal()		
        self.bt_restaurar.hide()
        self.bt_maximizar.show()

    def  control_bt_maximizar(self):
        self.setStyleSheet("background-color:blck")
        self.setAutoFillBackground(True); 
        self.showMaximized()
        self.bt_maximizar.hide()
        self.bt_restaurar.show()

	## mover ventana
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
                
    def mover_ventana(self, event):
        if self.isMaximized() == False:			
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()

        if event.globalPos().y() <=20:
            self.showMaximized()
        else:
            self.showNormal()

    def show_dialog(self):
        self.dialog.show()

    def show_Error(self):
        self.Error.show()

    def UpdateSensors(self):
        self.DataSensors = self.Blue.GetData()
        self.munon.change_neighbors(1211, self.DataSensors[0], 200)
        self.munon.change_neighbors(1096, self.DataSensors[1], 200)
        self.munon.change_neighbors(1256, self.DataSensors[2], 300)
        self.munon.change_neighbors(1148, self.DataSensors[3], 400)
        self.munon.AddMeshPlotterBackground()

    def ContinueUpdate(self):
        while self.update:
            self.UpdateSensors

    def iniciar_hilo(self):
        hilo = threading.Thread(target=self.mi_hilo)
        hilo.daemon = True
        hilo.start()

    def mi_hilo(self):
        print("Inicio del hilo")
        while(self.Blue.GetConection()):
            if(self.Blue.GetData() == []):
                break
            self.Blue.ObtainData()
            print(self.Blue.GetData())
            self.UpdateSensors()
            time.sleep(1)
        print("Fin del hilo")

class Dialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        loadUi('diseno1.ui', self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        #control barra de titulos
        self.bt_minimizar2.clicked.connect(self.control_bt_minimizar)		
        self.bt_cerrar2.clicked.connect(lambda: self.close())

    def control_bt_minimizar(self):
        self.showMinimized()

    ## mover ventana
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def mover_ventana(self, event):
        if self.isMaximized() == False:			
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()

        if event.globalPos().y() <=20:
            self.showMaximized()
        else:
            self.showNormal()
		
if __name__ == "__main__":
    app = QApplication(sys.argv)
    miApp = MainWindow()
    miApp.show()
    sys.exit(app.exec_())





'''import sys, time,threading
from Bluethoot import Bluethoot
from Map import MapHeat

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog,  QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.uic import loadUi
from pyvistaqt import QtInteractor, BackgroundPlotter

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('diseno.ui', self)
	
        self.update = True

        self.dialog = Dialog() 
        self.Error = Dialog()

        self.Blue = Bluethoot()
        self.DataSensors = []

        self.Blue.SetConection(False)

        self.munon = MapHeat()
        self.munon.ObtainHeatValue2()
        self.munon.SetZone1(100)
        self.munon.change_neighbors(6077, 0, 1500)
        self.munon.change_neighbors(6909, 0, 4000)
        self.munon.change_neighbors(5597, 0, 4000)
        self.munon.change_neighbors(6554, 0, 5000)
        self.munon.AddMesh()
        self.munon.AddScalarBar()
        self.Plotter_data = self.munon.GetPlotter()

        #Widget de impresion 3D
        vlayout = QtWidgets.QVBoxLayout()
        self.plotter = QtInteractor(self.frame_contenido)
        vlayout.addWidget(self.plotter.interactor)
        self.frame_contenido.setLayout(vlayout)
        self.plotter.add_mesh(self.Plotter_data, show_edges=True)
        self.plotter.reset_camera()

        #Botones de conexion
        self.bt_conectar.clicked.connect(self.control_bt_conectar)
        self.bt_conectar.clicked.connect(self.iniciar_hilo)
        self.bt_desconectar.clicked.connect(self.control_bt_desconectar)
        self.bt_reconectar.clicked.connect(self.control_bt_reconectar)
        self.bt_reconectar.clicked.connect(self.iniciar_hilo)
        
		# mover ventana
        self.frame_Logo.mouseMoveEvent = self.mover_ventana
        self.frame_control.mouseMoveEvent = self.mover_ventana

		#control barra de titulos
        self.bt_minimizar.clicked.connect(self.control_bt_minimizar)		
        self.bt_restaurar.clicked.connect(self.control_bt_normal)
        self.bt_maximizar.clicked.connect(self.control_bt_maximizar)
        self.bt_cerrar.clicked.connect(lambda: self.close())

        self.bt_restaurar.hide()

        #eliminar barra y de titulo - opacidad
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        #self.label_contenido.hide()
        
        
        #Imagen obejto 3D


    def control_bt_conectar(self):

        try:
            self.Blue.GenerateConection()
            self.label_contenido.show()
            self.Blue.SetConection(True)
            self.munon.TakeAScreenshot()
            self.pixmap = QPixmap('Toma_2.jpg')
            self.label_contenido.setPixmap(self.pixmap)
            
           
        except OSError:
            if self.Blue.GetConection() == False:
                self.show_dialog()
            

    def control_bt_desconectar(self):

        self.Blue.SetConection(False)    

    def control_bt_reconectar(self):
            
        self.Blue.SetConection(True)


    def control_bt_minimizar(self):
        self.showMinimized()		

    def  control_bt_normal(self):
        self.setStyleSheet("background-color:#000000ff")
        self.setAutoFillBackground(True); 
        self.showNormal()		
        self.bt_restaurar.hide()
        self.bt_maximizar.show()

    def  control_bt_maximizar(self):
        self.setStyleSheet("background-color:blck")
        self.setAutoFillBackground(True); 
        self.showMaximized()
        self.bt_maximizar.hide()
        self.bt_restaurar.show()

	## mover ventana
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
                
    def mover_ventana(self, event):
        if self.isMaximized() == False:			
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()

        if event.globalPos().y() <=20:
            self.showMaximized()
        else:
            self.showNormal()

    def show_dialog(self):
        
        self.dialog.show()

    def show_Error(self):
        
        self.Error.show()

    def UpdateSensors(self):
        self.DataSensors = Bluethoot.GetData()
        self.munon.change_neighbors(6077, self.DataSensors[0], 1500)
        self.munon.change_neighbors(6909, self.DataSensors[1], 4000)
        self.munon.change_neighbors(5597, self.DataSensors[2], 4000)
        self.munon.change_neighbors(6554, self.DataSensors[3], 5000)
        self.munon.change_neighbors(1211, self.DataSensors[0], 200)
        self.munon.change_neighbors(1096, self.DataSensors[1], 200)
        self.munon.change_neighbors(1256, self.DataSensors[2], 300)
        self.munon.change_neighbors(1148, self.DataSensors[3], 400)
        self.munon.AddMesh()
        self.munon.GetPlotterBackground()

    def ContinueUpdate(self):
        while self.update:
            self.UpdateSensors

    def iniciar_hilo(self):
        hilo = threading.Thread(target=self.mi_hilo)
        hilo.daemon = True
        hilo.start()
        print("llegamos")
        

    def mi_hilo(self):
        print("Inicio del hilo")
        while(self.Blue.GetConection()):
            if(self.Blue.GetData() == []):
                break
            self.Blue.ObtainData()
            print(self.Blue.GetData())
            time.sleep(1)
        print("Fin del hilo")
       

class Dialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        loadUi('diseno1.ui', self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        #control barra de titulos
        self.bt_minimizar2.clicked.connect(self.control_bt_minimizar)		
        self.bt_cerrar2.clicked.connect(lambda: self.close())

    def control_bt_minimizar(self):
        self.showMinimized()

    ## mover ventana
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def mover_ventana(self, event):
        if self.isMaximized() == False:			
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()

        if event.globalPos().y() <=20:
            self.showMaximized()
        else:
            self.showNormal()


		
if __name__ == "__main__":
    app = QApplication(sys.argv)
    miApp = MainWindow()
    miApp.show()
    sys.exit(app.exec_())'''