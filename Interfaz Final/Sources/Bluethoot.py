import serial, time
import serial.tools.list_ports

class Bluethoot():
    def __init__(self):
        # Obtener la lista de todos los puertos seriales disponibles en el sistema
        self.available_ports = list(serial.tools.list_ports.comports())
        # Lista para almacenar los nombres de los dispositivos Bluetooth
        self.device_names = []
        # Lista para almacenar los puertos seriales utilizados por los dispositivos Bluetooth
        self.serial_ports = []
        #Puerto serial a usar 
        self.Port = ''
        #Lista con los datos
        self.Data = []
        #Conexion establecida
        self.Conection = True
        #Conexion serial
        self.ser = ''            

    def ObtainBluethootPorts(self):     
        # Iterar sobre los puertos seriales disponibles en el sistema
        for port in self.available_ports:
            # Si el puerto serial está asociado a un dispositivo Bluetooth, agregarlo a las listas
            if "Bluetooth" in port.description:
                self.device_names.append(port.description)
                self.serial_ports.append(port.device)
                #print("Dispositivo Bluetooth: {}".format(port.description))
                #print("Puerto Serial: {}".format(port.device))

        print("Nombres de dispositivos Bluetooth: {}".format(self.device_names))
        print("Puertos seriales utilizados por dispositivos Bluetooth: {}".format(self.serial_ports))

    def ObtainValidPort(self):
        #Iteración sobre los puertos seriales bluethoot hasta encontrar el que esta mandando los datos correctos
        for port in self.serial_ports:
            self.Port = port
            self.ser = serial.Serial(self.Port, 9600, timeout = 1)
            time.sleep(2)
            self.Datos = self.ser.readline().decode('utf-8')
            self.Data = self.Datos.split(" ")
            if self.Data[0] == "Sensor1:":
                break

    def ContinueConetion(self):
        #Ciclo infinito el cual mantiene la recepción de datos 
        while self.Conection:
            self.Datos = self.ser.readline().decode('utf-8')
            self.Data = self.Datos.split(" ")
            #print(self.Datos)
            #print(self.Data)
            time.sleep(2)

    def ObtainData(self):
        if self.Conection == True:
            #Obtención y separacion de datos
            self.Datos = self.ser.readline().decode('utf-8')
            self.Data = self.Datos.split(" ")
            #print(self.Datos)
            #print(self.Data)
            time.sleep(2)

    def SetConection(self, Conection = True):
        self.Conection = Conection

    def GetConection(self):
        return self.Conection

    def GenerateConection(self):
        self.ObtainBluethootPorts()
        self.ObtainValidPort()
        self.SetConection()
    
    def GetData(self):
        Dataout = []
        for i in self.Data:
            try:
                Datain = float(i)
                Dataout.append(Datain)
            except ValueError:
                continue
        return Dataout
    
    def GetDatos(self):
        return self.Datos



Blue = Bluethoot()
Blue.GenerateConection()
Blue.ObtainData()
print(Blue.GetData())
Blue.ContinueConetion()





'''import serial, time
import serial.tools.list_ports

class Bluethoot():
    def __init__(self):
        # Obtener la lista de todos los puertos seriales disponibles en el sistema
        self.available_ports = list(serial.tools.list_ports.comports())
        # Lista para almacenar los nombres de los dispositivos Bluetooth
        self.device_names = []
        # Lista para almacenar los puertos seriales utilizados por los dispositivos Bluetooth
        self.serial_ports = []
        #Puerto serial a usar 
        self.Port = ''
        #Lista con los datos
        self.Data = []
        #Conexion establecida
        self.Conection = True
        #Conexion serial
        self.ser = ''            

    def ObtainBluethootPorts(self):     
        # Iterar sobre los puertos seriales disponibles en el sistema
        for port in self.available_ports:
            # Si el puerto serial está asociado a un dispositivo Bluetooth, agregarlo a las listas
            if "Bluetooth" in port.description:
                self.device_names.append(port.description)
                self.serial_ports.append(port.device)
                #print("Dispositivo Bluetooth: {}".format(port.description))
                #print("Puerto Serial: {}".format(port.device))

        #print("Nombres de dispositivos Bluetooth: {}".format(self.device_names))
        #print("Puertos seriales utilizados por dispositivos Bluetooth: {}".format(self.serial_ports))

    def ObtainValidPort(self):
        #Iteración sobre los puertos seriales bluethoot hasta encontrar el que esta mandando los datos correctos
        for port in self.serial_ports:
            self.Port = port
            self.ser = serial.Serial(self.Port, 9600, timeout = 1)
            time.sleep(2)
            self.Datos = self.ser.readline().decode('utf-8')
            self.Data = self.Datos.split(" ")
            if self.Data[0] == "Sensor1: ":
                break

    def ContinueConetion(self):
        #Ciclo infinito el cual mantiene la recepción de datos 
        while self.Conection:
            self.Datos = self.ser.readline().decode('utf-8')
            self.Data = self.Datos.split(" ")
            #print(self.Datos)
            #print(self.Data)
            time.sleep(2)

    def ObtainData(self):
        if self.Conection == True:
            #Obtención y separacion de datos
            self.Datos = self.ser.readline().decode('utf-8')
            self.Data = self.Datos.split(" ")
            #print(self.Datos)
            #print(self.Data)
            time.sleep(2)

    def SetConection(self, Conection = True):
        self.Conection = Conection

    def GetConection(self):
        return self.Conection

    def GenerateConection(self):
        self.ObtainBluethootPorts()
        self.ObtainValidPort()
        self.SetConection()
    
    def GetData(self):
        Dataout = []
        for i in self.Data:
            try:
                Data = float(i)
                Dataout.append(Data)
            except ValueError:
                continue
        return Dataout
    
    def GetDatos(self):
        return self.Datos'''



'''Blue = Bluethoot()
Blue.GenerateConection()
Blue.ObtainData()
print(Blue.GetData())
Blue.ContinueConetion()'''