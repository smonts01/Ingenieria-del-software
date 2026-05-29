"""Elementos de vista reutilizables.

Los controladores importan estas clases en lugar de crear directamente widgets
concretos de PyQt. Así los detalles visuales quedan centralizados en la capa Vista.
"""
from PyQt5.QtWidgets import QMessageBox as _QMessageBox, QTableWidgetItem as _QTableWidgetItem, QCheckBox as _QCheckBox


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
