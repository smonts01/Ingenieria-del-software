"""Elementos de vista reutilizables.

Esta capa es la única que conoce PyQt5. Los controladores usan estos
adaptadores para respetar MVC: controlador coordina, vista dibuja.
"""
from PyQt5 import uic as _uic
from PyQt5.QtCore import Qt as _Qt
from PyQt5.QtGui import QPixmap as _QPixmap
from PyQt5.QtWidgets import (
    QMessageBox as _QMessageBox,
    QTableWidgetItem as _QTableWidgetItem,
    QCheckBox as _QCheckBox,
    QPushButton as _QPushButton,
)
from PyQt5.QtWidgets import QFileDialog


class CargadorVista:
    @staticmethod
    def cargar(ruta):
        return _uic.loadUi(ruta)


class MensajeView:
    SI = _QMessageBox.Yes
    NO = _QMessageBox.No

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


class TablaView:
    @staticmethod
    def crear_item(valor, editable=True):
        item = _QTableWidgetItem(str(valor) if valor is not None else "")
        if not editable:
            item.setFlags(item.flags() & ~_Qt.ItemIsEditable)
        return item

    @staticmethod
    def poner_item(tabla, fila, columna, valor, editable=True):
        tabla.setItem(fila, columna, TablaView.crear_item(valor, editable))

    @staticmethod
    def configurar_columnas(tabla, cabeceras):
        tabla.setColumnCount(len(cabeceras))
        tabla.setHorizontalHeaderLabels(cabeceras)

    @staticmethod
    def activar_edicion_por_click(tabla):
        tabla.setEditTriggers(tabla.DoubleClicked | tabla.SelectedClicked)
        tabla.setSelectionBehavior(tabla.SelectRows)


class CheckBoxView(_QCheckBox):
    pass


class ImagenView:
    @staticmethod
    def desde_bytes(datos):
        pixmap = _QPixmap()
        pixmap.loadFromData(datos)
        return pixmap

class ArchivoView:
    """Componente de vista para seleccionar archivos desde la interfaz."""

    @staticmethod
    def seleccionar_archivo_sql(parent=None, titulo="Seleccionar copia de seguridad"):
        ruta, _ = QFileDialog.getOpenFileName(
            parent,
            titulo,
            "",
            "Archivos SQL (*.sql)"
        )
        return ruta

    @staticmethod
    def seleccionar_carpeta(parent=None, titulo="Seleccionar carpeta"):
        ruta = QFileDialog.getExistingDirectory(
            parent,
            titulo,
            ""
        )
        return ruta
    

class BotonesView:
    @staticmethod
    def crear_boton_ayuda(parent, x, y, slot):
        btn = _QPushButton("?", parent)
        btn.setFixedSize(36, 36)
        btn.move(x, y)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #18B7A5;
                border: 1px solid #18B7A5;
                border-radius: 8px;
                font: bold 14pt 'Segoe UI';
            }
            QPushButton:hover {
                background-color: #E6F7F5;
            }
        """)
        btn.clicked.connect(slot)
        btn.show()
        return btn