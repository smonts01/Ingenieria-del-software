from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from PyQt5 import uic

# Cargar la interfaz generada desde el archivo .ui
Form, Window = uic.loadUiType("./src/vista/Ui/interfaz_grafica.ui")


class MiVentana(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Inicializa los widgets

        # Conectar botones
        self.pushButton.clicked.connect(self.iniciar_sesion)
        self.btnOjo.clicked.connect(self.mostrar_ocultar_contrasena)

        # Estado inicial: contraseña oculta + ojo abierto
        self.txtContrasea.setEchoMode(QLineEdit.Password)
        self.btnOjo.setStyleSheet("""
        QToolButton {
            image: url(./src/vista/imagenes/ojo_abierto.jpg);
            background: transparent;
            border: none;
        }
        """)

    def iniciar_sesion(self):
        usuario = self.txtUsuario.text()
        contrasena = self.txtContrasea.text()

        if usuario == "" or contrasena == "":
            QMessageBox.warning(self, "Error", "Debes completar usuario y contraseña")
        else:
            self.controlador.iniciar_sesion(usuario, contrasena)

    def mostrar_ocultar_contrasena(self):
        if self.txtContrasea.echoMode() == QLineEdit.Password:
            # Mostrar contraseña + ojo cerrado
            self.txtContrasea.setEchoMode(QLineEdit.Normal)
            self.btnOjo.setStyleSheet("""
            QToolButton {
                image: url(./src/vista/imagenes/ojo_cerrado.jpg);
                background: transparent;
                border: none;
            }
            """)
        else:
            # Ocultar contraseña + ojo abierto
            self.txtContrasea.setEchoMode(QLineEdit.Password)
            self.btnOjo.setStyleSheet("""
            QToolButton {
                image: url(./src/vista/imagenes/ojo_abierto.png);
                background: transparent;
                border: none;
            }
            """)


if __name__ == "__main__":
    app = QApplication([])
    ventana = MiVentana()
    ventana.show()
    app.exec_()