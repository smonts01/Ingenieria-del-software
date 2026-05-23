from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from PyQt5 import uic
import os

# Carga la interfaz desde el archivo .ui
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Form, Window = uic.loadUiType(os.path.join(_BASE_DIR, "Ui", "interfaz_grafica.ui"))


class MiVentana(QMainWindow, Form):
    """
    Vista de Login (MVC - View).
    Solo gestiona la presentación y delega la lógica al controlador.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.controlador = None

        # Normalizar nombres de widgets para que el controlador encuentre siempre
        # botonEntrar, txtUsuario y txtPassword, independientemente del .ui
        self._normalizar_widgets()

        # Botón de mostrar/ocultar contraseña (si existe)
        if hasattr(self, "btnOjo"):
            self.btnOjo.clicked.connect(self._mostrar_ocultar_contrasena)

        # Contraseña oculta por defecto
        self.txtPassword.setEchoMode(QLineEdit.Password)
        self._set_icono_ojo(abierto=True)

    def _normalizar_widgets(self):
        """
        Crea alias de widgets para garantizar la interfaz MVC independientemente
        de los nombres usados en el .ui de Qt Designer.
        """
        # txtUsuario - buscar por varios nombres posibles
        if not hasattr(self, "txtUsuario") and hasattr(self, "lineEdit_usuario"):
            self.txtUsuario = self.lineEdit_usuario

        # txtPassword - el .ui puede llamarlo txtContrasea o lineEdit_password
        if not hasattr(self, "txtPassword"):
            for nombre in ("txtContrasea", "lineEdit_password", "txtContrasena"):
                if hasattr(self, nombre):
                    self.txtPassword = getattr(self, nombre)
                    break
            else:
                # Último recurso: primer QLineEdit que no sea usuario
                self.txtPassword = self.txtContrasea if hasattr(self, "txtContrasea") else None

        # botonEntrar - buscar por varios nombres posibles
        if not hasattr(self, "botonEntrar"):
            for nombre in ("pushButton", "btnEntrar", "btnLogin", "pushButton_login"):
                if hasattr(self, nombre):
                    self.botonEntrar = getattr(self, nombre)
                    break

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


if __name__ == "__main__":
    app = QApplication([])
    ventana = MiVentana()
    ventana.show()
    app.exec_()