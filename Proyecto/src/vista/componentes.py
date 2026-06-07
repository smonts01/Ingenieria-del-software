"""Componentes de vista reutilizables. 
Esta capa es la única que conoce PyQt5 directamente. Envuelve los
widgets y diálogos de Qt en clases simples que los controladores y
vistas usan sin importar PyQt5 ellos mismos, respetando así el
principio MVC: el controlador coordina, la vista dibuja.
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
    """Adaptador para cargar archivos .ui de Qt Designer.
    Centraliza la llamada a loadUi para que ninguna vista importe
    uic directamente.
    """

    @staticmethod
    def cargar(ruta: str):
        """Carga y devuelve el widget definido en el archivo .ui indicado."""
        return _uic.loadUi(ruta)


class MensajeView:
    """Adaptador para los diálogos de mensajes de Qt (QMessageBox).
    Agrupa los tipos de diálogo más usados: información, aviso,
    error y pregunta. Los controladores usan esta clase en lugar de
    importar QMessageBox directamente.
    """

    # Constantes para los botones de la pregunta (Sí / No)
    SI = _QMessageBox.Yes
    NO = _QMessageBox.No

    @staticmethod
    def information(parent, title, text):
        """Muestra un diálogo informativo (icono azul de información)."""
        return _QMessageBox.information(parent, title, text)

    @staticmethod
    def warning(parent, title, text):
        """Muestra un diálogo de aviso (icono amarillo de advertencia)."""
        return _QMessageBox.warning(parent, title, text)

    @staticmethod
    def critical(parent, title, text):
        """Muestra un diálogo de error (icono rojo de error crítico)."""
        return _QMessageBox.critical(parent, title, text)

    @staticmethod
    def question(parent, title, text, buttons):
        """Muestra un diálogo de pregunta con los botones indicados.
        Devuelve el botón pulsado (MensajeView.SI o MensajeView.NO)."""
        return _QMessageBox.question(parent, title, text, buttons)


class TablaView:
    """Utilidades para manipular tablas QTableWidget desde las vistas.
    Evita que las vistas importen QTableWidgetItem o Qt directamente.
    """

    @staticmethod
    def crear_item(valor, editable: bool = True):
        """Crea un QTableWidgetItem con el valor indicado.
        Si editable=False, el usuario no podrá modificar la celda."""
        item = _QTableWidgetItem(str(valor) if valor is not None else "")
        if not editable:
            item.setFlags(item.flags() & ~_Qt.ItemIsEditable)
        return item

    @staticmethod
    def poner_item(tabla, fila: int, columna: int, valor, editable: bool = True):
        """Inserta un ítem en la celda indicada de la tabla."""
        tabla.setItem(fila, columna, TablaView.crear_item(valor, editable))

    @staticmethod
    def configurar_columnas(tabla, cabeceras: list):
        """Establece el número de columnas y sus cabeceras en la tabla."""
        tabla.setColumnCount(len(cabeceras))
        tabla.setHorizontalHeaderLabels(cabeceras)

    @staticmethod
    def activar_edicion_por_click(tabla):
        """Configura la tabla para que se edite con doble clic o clic sobre
        la celda seleccionada, y selecciona filas completas."""
        tabla.setEditTriggers(tabla.DoubleClicked | tabla.SelectedClicked)
        tabla.setSelectionBehavior(tabla.SelectRows)




class ImagenView:
    """Utilidades para cargar imágenes en los widgets de Qt."""

    @staticmethod
    def desde_bytes(datos: bytes):
        """Crea y devuelve un QPixmap a partir de bytes de imagen
        (por ejemplo, el contenido de un PNG generado con matplotlib)."""
        pixmap = _QPixmap()
        pixmap.loadFromData(datos)
        return pixmap


class ArchivoView:
    """Adaptador para los diálogos de selección de archivos (QFileDialog).

    Permite seleccionar un archivo SQL de backup o una carpeta de destino
    sin que las vistas importen QFileDialog directamente.
    """

    @staticmethod
    def seleccionar_archivo_sql(parent=None,
                                titulo="Seleccionar copia de seguridad") -> str:
        """Abre un diálogo para seleccionar un archivo .sql.
        Devuelve la ruta del archivo seleccionado, o cadena vacía si se cancela."""
        ruta, _ = QFileDialog.getOpenFileName(
            parent,
            titulo,
            "",
            "Archivos SQL (*.sql)"
        )
        return ruta

    @staticmethod
    def seleccionar_carpeta(parent=None, titulo="Seleccionar carpeta") -> str:
        """Abre un diálogo para seleccionar una carpeta.
        Devuelve la ruta de la carpeta seleccionada, o cadena vacía si se cancela."""
        ruta = QFileDialog.getExistingDirectory(parent, titulo, "")
        return ruta


class BotonesView:
    """Fábrica de botones reutilizables con el estilo visual de StayFit."""

    @staticmethod
    def crear_boton_ayuda(parent, x: int, y: int, slot) -> _QPushButton:
        """Crea y posiciona un botón de ayuda '?' con el estilo corporativo.

        El botón es circular, verde (#18B7A5) y llama a slot cuando se pulsa.
        Se usa en todas las pantallas para mostrar la ayuda contextual.

        Args:
            parent: widget padre sobre el que se posiciona el botón.
            x, y:   coordenadas de posición dentro del padre.
            slot:   función a llamar cuando el usuario pulse el botón.

        Devuelve el QPushButton creado y ya visible.
        """
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