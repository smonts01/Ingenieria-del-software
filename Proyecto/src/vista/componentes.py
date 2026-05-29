"""Elementos de vista reutilizables.

Esta capa es la única que conoce PyQt5. Los controladores deben usar estos
adaptadores para respetar MVC: controlador coordina, vista dibuja.
"""
from PyQt5 import uic as _uic
from PyQt5.QtCore import Qt as _Qt
from PyQt5.QtGui import QPixmap as _QPixmap
from PyQt5.QtWidgets import QMessageBox as _QMessageBox, QTableWidgetItem as _QTableWidgetItem, QCheckBox as _QCheckBox


class CargadorVista:
    @staticmethod
    def cargar(ruta):
        return _uic.loadUi(ruta)


class MensajeView:
    Yes = _QMessageBox.Yes
    No = _QMessageBox.No

    @staticmethod
    def information(parent, title, text):
        return _QMessageBox.information(parent, title, text)

    @staticmethod
    def warning(parent, title, text):
        return _QMessageBox.warning(parent, title, text)

    @staticmethod
    def critical(parent, title, text):
        return _QMessageBox.critical(parent, title, text)

    @staticmethod
    def question(parent, title, text, buttons):
        return _QMessageBox.question(parent, title, text, buttons)


class TablaItem(_QTableWidgetItem):
    pass


class CheckBoxView(_QCheckBox):
    pass


class ImagenView:
    @staticmethod
    def desde_bytes(datos):
        pixmap = _QPixmap()
        pixmap.loadFromData(datos)
        return pixmap


class ConstantesVista:
    ItemIsEditable = _Qt.ItemIsEditable
