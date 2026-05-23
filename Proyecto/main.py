import sys
import os

# Asegurar que el directorio del proyecto esté en el path
base_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_dir)
sys.path.insert(0, base_dir)

from PyQt5.QtWidgets import QApplication
from src.vista.Login import MiVentana
from src.modelo.Logica import Logica
from src.controlador.ControladorPrincipal import ControladorPrincipal

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MiVentana()
    modelo = Logica()
    controlador = ControladorPrincipal(ventana, modelo)
    ventana.controlador = controlador
    controlador.abrirIniciarSesion()
    sys.exit(app.exec_())
