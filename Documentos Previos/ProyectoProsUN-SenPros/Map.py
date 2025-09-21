import numpy as np
import pyvista as pv
import pyvistaqt as pvqt
from Bluethoot import Bluethoot

class MapHeat():
    def __init__(self):
        self.munon = pv.read("MallaSimpl.stl")
        self.num_points = self.munon.n_points
        self.heat_value = np.random.rand(self.num_points)
        self.heat_value2 = []
        self.zone1 = self.munon.point_neighbors(100)
        self.plotter = pv.Plotter()
        self.cmap = 'reds'
        self.title = 'Fuerza Aplicada (N)'
        self.clim =  [0,11]
        self.window_height = 500
        self.window_width = 800
        self.plotter.window_size = (self.window_width,self.window_height)

        self.plotterBackground = pvqt.BackgroundPlotter()
        self.plotterBackground.window_size = (self.window_width,self.window_height)
    
        

    def PrintImage(self):
        print(self.munon)


    def ObtainHeatValue2(self):
        for x in range(self.num_points):
            self.heat_value2.append(0)

    def change_neighbors(self, point, value, i):
        self.heat_value2[point] = value
        queue = [point]
        visited = [point]
        level = {}
        level[point] = 1
        x = 0
        while (len(queue)!=0) and (x<i):
            u = queue.pop(0)
            zone = self.munon.point_neighbors(u)
            for z in zone:
                if not(z in visited):
                    level[z] = level[u] + 1
                    self.heat_value2[z] = value / ( 1 + 0.1 * (level[z]))
                    queue.append(z)
                    visited.append(z)
            x += 1
        return
    
    def SetZone1(self, zone):
        self.zone1 = self.munon.point_neighbors(zone)

    def PrintZone1(self):
        print(self.zone1)

    def AddMesh(self):
        self.plotter.add_mesh(self.munon, scalars = self.heat_value2, cmap = self.cmap, clim =self.clim)

    def AddMeshPlotterBackground(self):
        self.plotterBackground.add_mesh(self.munon, scalars = self.heat_value2, cmap = self.cmap, clim =self.clim)

    def AddScalarBar(self):
        self.plotter.add_scalar_bar(title = self.title)

    def ClosePlotter(self):
        self.plotter.close()

    def ShowPlotter(self):
        self.plotter.show()

    def GetPlotter(self):
        return self.plotter
    
    def  GetPlotterBackground(self):
        return self.plotterBackground
    
    def  SetPlotterBackground(self, *args, **kwargs):
        self.plotterBackground(*args, **kwargs)
    
    def ShowPlotterBackground(self):
        self.plotterBackground.show()

    def ClosePlotterBackground(self):
        self.plotterBackground.close()
    
    def GetPlotterBackground(self):
        return self.plotterBackground
    
    def GetMesh(self):
        return self.munon
    
    def GetLastImagePlotterBackground(self):
        return self.plotterBackground.last_image
    
    def TakeAScreenshot(self):
        # Obtener el renderizado como una imagen
        # Capturar una captura de pantalla
        None
        # Guardar la captura de pantalla en un archivo
       
    

"""munon = MapHeat()
#munon.PrintImage()
munon.ObtainHeatValue2()
munon.SetZone1(100)
#munon.PrintZone1()
munon.change_neighbors(6077, 10, 1500)
munon.change_neighbors(6909, 2.5, 4000)
munon.change_neighbors(5597, 1, 4000)
munon.change_neighbors(6554, 5, 5000)
munon.AddMesh()
munon.AddScalarBar()
munon.ShowPlotter()"""
