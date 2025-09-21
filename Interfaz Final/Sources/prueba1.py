import pyvistaqt as pvqt

# Crea un plot 3D
plotter = pvqt.BackgroundPlotter()

# Agrega una malla de ejemplo al plot
mesh = plotter.create_sphere()
plotter.add_mesh(mesh)

# Muestra la ventana de visualización
plotter.show()
