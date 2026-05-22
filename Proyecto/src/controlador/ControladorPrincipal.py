from PyQt5.QtWidgets import QMessageBox
<<<<<<< HEAD
=======
from PyQt5 import uic
import os
import datetime

from src.controlador.ControladorAdministrador import ControladorAdministrador

>>>>>>> 53426b5126746eedd29d2824852763c3ebbc5ce2

class ControladorPrincipal:

    def __init__(self, vista, modelo):

        self.vista = vista
        self.modelo = modelo

    def abrirIniciarSesion(self):

        self.vista.botonEntrar.clicked.connect(
            self.iniciarSesion
        )

        self.vista.show()


    def iniciarSesion(self):

        usuario = self.vista.txtUsuario.text()
        password = self.vista.txtPassword.text()

        if usuario == "" or password == "":

            QMessageBox.warning(
                self.vista,
                "Error",
                "Completa todos los campos"
            )

            return

        rol = self.modelo.validarLogin(
            usuario,
            password
        )

        if rol:

            QMessageBox.information(
                self.vista,
                "Correcto",
                f"Bienvenido {usuario}\nRol: {rol}"
            )

        else:

            QMessageBox.warning(
                self.vista,
                "Error",
                "Usuario o contraseña incorrectos"
            )