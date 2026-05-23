import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from PyQt5 import uic

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Form, Window = uic.loadUiType(os.path.join(_BASE_DIR, "Ui", "interfaz_grafica.ui"))


class MiVentana(QMainWindow, Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.controlador = None

        # Alias para que el controlador siempre encuentre txtPassword y botonEntrar
        if not hasattr(self, "txtPassword"):
            for nombre in ("txtContrasea", "txtContrasena", "lineEdit_password"):
                if hasattr(self, nombre):
                    self.txtPassword = getattr(self, nombre)
                    break

        if not hasattr(self, "botonEntrar"):
            for nombre in ("pushButton", "btnEntrar", "btnLogin"):
                if hasattr(self, nombre):
                    self.botonEntrar = getattr(self, nombre)
                    break

        if hasattr(self, "btnOjo"):
            self.btnOjo.clicked.connect(self._mostrar_ocultar_contrasena)

        self.txtPassword.setEchoMode(QLineEdit.Password)
        self._set_icono_ojo(abierto=True)

    def _mostrar_ocultar_contrasena(self):
        if self.txtPassword.echoMode() == QLineEdit.Password:
            self.txtPassword.setEchoMode(QLineEdit.Normal)
            self._set_icono_ojo(abierto=False)
        else:
            self.txtPassword.setEchoMode(QLineEdit.Password)
            self._set_icono_ojo(abierto=True)

    def _set_icono_ojo(self, abierto):
        if not hasattr(self, "btnOjo"):
            return
        img = "ojo_abierto.jpg" if abierto else "ojo_cerrado.jpg"
        ruta = os.path.join(_BASE_DIR, "imagenes", img).replace("\\", "/")
        self.btnOjo.setStyleSheet(f"""
            QToolButton {{
                image: url({ruta});
                background: transparent;
                border: none;
            }}
        """)
