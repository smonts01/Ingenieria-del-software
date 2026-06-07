"""
Vistas del rol Recepcionista
Responsabilidad de la Vista:
- Cargar el archivo .ui que le pasa el controlador.
- Conocer sus botones y conectar sus eventos.
- Delegar las acciones al controlador.
- Exponer métodos get_xxx() para que el controlador lea datos.
- Exponer métodos set_xxx() / cargar_tabla_xxx() para que el controlador actualice la interfaz.
- Mostrar mensajes visuales.
"""

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QLineEdit, QMessageBox
from PyQt5.uic import loadUi


# Compartidos

def _rellenar_tabla_accesos(tabla, cabeceras, datos):
    """
    Rellena una tabla de accesos.
    Esta función pertenece a la Vista porque solo pinta datos en una tabla.
    No calcula datos ni consulta la base de datos.
    """
    tabla.clear()
    tabla.setColumnCount(len(cabeceras))
    tabla.setHorizontalHeaderLabels(cabeceras)
    tabla.setRowCount(len(datos))

    for fi, vo in enumerate(datos):
        valores = [
            str(getattr(vo, "nombre", "")),
            str(getattr(vo, "dni", "")),
            str(getattr(vo, "tipo_acceso", "")),
            str(getattr(vo, "fecha_hora_registro", "")),
        ]

        for ci, val in enumerate(valores[:len(cabeceras)]):
            tabla.setItem(fi, ci, QTableWidgetItem(val))

    tabla.resizeColumnsToContents()


def _rellenar_tabla_tuplas(tabla, cabeceras, datos):
    """
    Rellena una tabla con tuplas o con objetos VO.
    Se usa en las pantallas de recepción para mostrar clientes recientes,
    clientes filtrados y otros datos de resumen.
    """
    tabla.clear()
    tabla.setColumnCount(len(cabeceras))
    tabla.setHorizontalHeaderLabels(cabeceras)
    tabla.setRowCount(len(datos))

    for fi, fila in enumerate(datos):

        if isinstance(fila, (list, tuple)):
            valores = list(fila)
        else:
            valores = [
                getattr(fila, "id_cliente", getattr(fila, "id_usuario", "")),
                getattr(fila, "dni", ""),
                getattr(fila, "nombre", ""),
                getattr(fila, "telefono", ""),
                getattr(fila, "email", ""),
                getattr(fila, "direccion", ""),
                getattr(fila, "fecha_nacimiento", ""),
                getattr(fila, "estado_pagado", ""),
            ]

        for ci, val in enumerate(valores[:len(cabeceras)]):
            tabla.setItem(
                fi,
                ci,
                QTableWidgetItem(str(val) if val is not None else "")
            )

    tabla.resizeColumnsToContents()


# Inicio

class VistaRecepcionistaInicio(QMainWindow):
    """
    Vista principal de recepción.
    Recibe la ruta completa del .ui desde el controlador.
    La vista carga el .ui y conecta sus botones.
    """

    def __init__(self, ruta_ui):
        super().__init__()

        # El controlador ya nos pasa la ruta completa:
        # src/vista/Ui/interfaz_recepcionista.ui
        loadUi(ruta_ui, self)

        self.controlador = None

        # La vista conoce sus botones y captura los clicks.
        # Luego delega la acción al controlador.
        self.btnCerrarSesion.clicked.connect(self._on_cerrar_sesion)
        self.btnInicio.clicked.connect(self._on_inicio)
        self.btnRegistroUsuario.clicked.connect(self._on_registrar_usuario)
        self.btnControlAcceso.clicked.connect(self._on_control_acceso)
        self.btnClientes.clicked.connect(self._on_clientes)
        self.btnPerfil.clicked.connect(self._on_perfil)

    # Delegar al controlador

    def _on_cerrar_sesion(self):
        self.controlador.cerrar_sesion()

    def _on_inicio(self):
        self.controlador.ir_inicio()

    def _on_registrar_usuario(self):
        self.controlador.ir_registrar_usuario()

    def _on_control_acceso(self):
        self.controlador.ir_control_acceso()

    def _on_clientes(self):
        self.controlador.ir_clientes()

    def _on_perfil(self):
        self.controlador.ir_perfil()

    def set_controlador(self, ctrl):
        """
        El controlador se asigna después de crear la vista.
        Así la vista puede delegarle las acciones.
        """
        self.controlador = ctrl

    # Metodos que usa el controlador

    def set_num_clientes(self, valor: str):
        self.lblNumClientes.setText(valor)

    def set_num_entradas(self, valor: str):
        self.lblNumEntradas.setText(valor)

    def set_num_clases_hoy(self, valor: str):
        self.lblNumClasesHoy.setText(valor)

    def cargar_tabla_registros(self, cabeceras: list, datos: list):
        _rellenar_tabla_accesos(self.tablaUltimosRegistros, cabeceras, datos)

    def cargar_tabla_clientes_recientes(self, cabeceras: list, datos: list):
        _rellenar_tabla_tuplas(self.tablaClientesRecientes, cabeceras, datos)


# Registrar usuario

class VistaRecepcionistaRegistrarUsuario(QMainWindow):
    """
    Vista para registrar un nuevo cliente desde recepción.
    """

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)

        self.controlador = None

        # Menú lateral.
        self.btnCerrarSesion.clicked.connect(self._on_cerrar_sesion)
        self.btnInicio.clicked.connect(self._on_inicio)
        self.btnRegistroUsuario.clicked.connect(self._on_registrar_usuario)
        self.btnControlAcceso.clicked.connect(self._on_control_acceso)
        self.btnClientes.clicked.connect(self._on_clientes)
        self.btnPerfil.clicked.connect(self._on_perfil)

        # Botón de registrar cliente.
        self.btnInicio_20.clicked.connect(self._on_confirmar_registro)

    # Delegar a controlador

    def _on_cerrar_sesion(self):
        self.controlador.cerrar_sesion()

    def _on_inicio(self):
        self.controlador.ir_inicio()

    def _on_registrar_usuario(self):
        self.controlador.ir_registrar_usuario()

    def _on_control_acceso(self):
        self.controlador.ir_control_acceso()

    def _on_clientes(self):
        self.controlador.ir_clientes()

    def _on_perfil(self):
        self.controlador.ir_perfil()

    def _on_confirmar_registro(self):
        self.controlador.registrar_cliente()

    def set_controlador(self, ctrl):
        self.controlador = ctrl

    # getters formularios
    # El controlador no toca directamente los widgets.
    # Lee los datos usando estos métodos.

    def get_dni(self):
        return self.DNI.text().strip()

    def get_nombre(self):
        return self.NombreCompleto.text().strip()

    def get_telefono(self):
        return self.Telefono.text().strip()

    def get_direccion(self):
        return self.Direccion.text().strip()

    def get_email(self):
        return self.Email.text().strip()

    def get_fecha(self):
        return self.Nacimiento.text().strip()

    def get_username(self):
        return self.Usuario.text().strip()

    def get_password(self):
        return self.Contrasea.text().strip()

    def get_confirmar(self):
        return self.ConfirmarContrasea.text().strip()

    def get_dni_tutor(self):
        if hasattr(self, "DNITutor"):
            return self.DNITutor.text().strip()
        return ""

    def get_nombre_tutor(self):
        if hasattr(self, "NombreTutor"):
            return self.NombreTutor.text().strip()
        return ""

    def get_plan(self):
        if hasattr(self, "PlanComboBox"):
            return self.PlanComboBox.currentText().strip()
        return "Basico"

    def es_menor(self):
        if hasattr(self, "ButtomMenor"):
            return self.ButtomMenor.isChecked()
        return False

    def es_adulto(self):
        if hasattr(self, "ButtomAdulto"):
            return self.ButtomAdulto.isChecked()
        return True

    # Metodos visuales

    def limpiar_formulario(self):
        for widget in self.findChildren(QLineEdit):
            widget.clear()

    def mostrar_error(self, msg: str):
        QMessageBox.warning(self, "Error", msg)

    def mostrar_exito(self, msg: str):
        QMessageBox.information(self, "Correcto", msg)


# Control de acceso

class VistaRecepcionistaControlAcceso(QMainWindow):
    """
    Vista para registrar entradas y salidas de clientes.
    """

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)

        self.controlador = None

        # Menú lateral.
        self.btnCerrarSesion.clicked.connect(self._on_cerrar_sesion)
        self.btnInicio.clicked.connect(self._on_inicio)
        self.btnRegistroUsuario.clicked.connect(self._on_registrar_usuario)
        self.btnControlAcceso.clicked.connect(self._on_control_acceso)
        self.btnClientes.clicked.connect(self._on_clientes)
        self.btnPerfil.clicked.connect(self._on_perfil)

        # Buscador y botones de acción.
        self.txtDNIoID.textChanged.connect(self._on_buscar)
        self.btnEntrada.clicked.connect(self._on_entrada)
        self.btnSalida.clicked.connect(self._on_salida)

    # Delegar al controlador

    def _on_cerrar_sesion(self):
        self.controlador.cerrar_sesion()

    def _on_inicio(self):
        self.controlador.ir_inicio()

    def _on_registrar_usuario(self):
        self.controlador.ir_registrar_usuario()

    def _on_control_acceso(self):
        self.controlador.ir_control_acceso()

    def _on_clientes(self):
        self.controlador.ir_clientes()

    def _on_perfil(self):
        self.controlador.ir_perfil()

    def _on_buscar(self):
        self.controlador.buscar_cliente_control_acceso()

    def _on_entrada(self):
        self.controlador.registrar_acceso_control("entrada")

    def _on_salida(self):
        self.controlador.registrar_acceso_control("salida")

    def set_controlador(self, ctrl):
        self.controlador = ctrl


    def get_dni_id(self):
        return self.txtDNIoID.text().strip()

    # Actualizar ui

    def set_cliente_encontrado(self, nombre, dni, id_usuario, estado_pago):
        self.lblNombre.setText(str(nombre))
        self.lblDNI.setText(f"DNI: {dni}")
        self.lblID.setText(f"ID: {id_usuario}")
        self.lblEstado.setText(str(estado_pago))

    def set_cliente_no_encontrado(self):
        self.lblNombre.setText("Cliente no encontrado")
        self.lblDNI.setText("DNI: -")
        self.lblID.setText("ID: -")
        self.lblEstado.setText("-")

    def limpiar_cliente(self):
        self.lblNombre.setText("Cliente no seleccionado")
        self.lblDNI.setText("DNI: -")
        self.lblID.setText("ID: -")
        self.lblEstado.setText("-")

    def cargar_tabla_accesos(self, cabeceras: list, datos: list):
        _rellenar_tabla_accesos(self.tableAccesos, cabeceras, datos)

    def mostrar_error(self, msg: str):
        QMessageBox.warning(self, "Error", msg)

    def mostrar_exito(self, msg: str):
        QMessageBox.information(self, "Correcto", msg)


# Clientes

class VistaRecepcionistaClientes(QMainWindow):
    """
    Vista del listado de clientes de recepción.
    Permite filtrar clientes y editar datos de la tabla.
    """

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)

        self.controlador = None

        # Menú lateral.
        self.btnCerrarSesion.clicked.connect(self._on_cerrar_sesion)
        self.btnInicio.clicked.connect(self._on_inicio)
        self.btnRegistroUsuario.clicked.connect(self._on_registrar_usuario)
        self.btnControlAcceso.clicked.connect(self._on_control_acceso)
        self.btnClientes.clicked.connect(self._on_clientes)
        self.btnPerfil.clicked.connect(self._on_perfil)

        # Filtros y guardar cambios.
        self.lblBuscarDNI.textChanged.connect(self._on_filtrar)
        self.comboBox_adultomenor.currentIndexChanged.connect(self._on_filtrar)
        self.comboBox_plan.currentIndexChanged.connect(self._on_filtrar)
        self.btnCambios.clicked.connect(self._on_guardar)

    # Delegar al controlador

    def _on_cerrar_sesion(self):
        self.controlador.cerrar_sesion()

    def _on_inicio(self):
        self.controlador.ir_inicio()

    def _on_registrar_usuario(self):
        self.controlador.ir_registrar_usuario()

    def _on_control_acceso(self):
        self.controlador.ir_control_acceso()

    def _on_clientes(self):
        self.controlador.ir_clientes()

    def _on_perfil(self):
        self.controlador.ir_perfil()

    def _on_filtrar(self):
        self.controlador.filtrar_clientes_recepcionista()

    def _on_guardar(self):
        self.controlador.guardar_cambios_clientes_recepcionista()

    def set_controlador(self, ctrl):
        self.controlador = ctrl

    # getter

    def get_filtro_dni(self):
        return self.lblBuscarDNI.text().strip()

    def get_filtro_tipo(self):
        return self.comboBox_adultomenor.currentText()

    def get_filtro_plan(self):
        return self.comboBox_plan.currentText()

    # actualizar ui

    def set_total_clientes(self, valor: str):
        self.lblTotalClientes.setText(valor)

    def set_nuevos_mes(self, valor: str):
        self.lblNuevosMes.setText(valor)

    def cargar_tabla_clientes(self, cabeceras: list, datos: list):
        _rellenar_tabla_tuplas(self.tablaClientes, cabeceras, datos)

        # Permitimos editar celdas con doble click o click sobre selección.
        self.tablaClientes.setEditTriggers(
            self.tablaClientes.DoubleClicked | self.tablaClientes.SelectedClicked
        )

        self.tablaClientes.setSelectionBehavior(self.tablaClientes.SelectRows)

    def num_filas(self) -> int:
        return self.tablaClientes.rowCount()

    def get_fila_tabla(self, fila: int, num_cols: int) -> list:
        """
        Devuelve los textos de una fila editada.
        El controlador usa esto para enviar los datos al modelo.
        """
        return [
            self.tablaClientes.item(fila, col).text().strip()
            if self.tablaClientes.item(fila, col) else ""
            for col in range(num_cols)
        ]

    def mostrar_error(self, msg: str):
        QMessageBox.warning(self, "Error", msg)

    def mostrar_exito(self, msg: str):
        QMessageBox.information(self, "Correcto", msg)


# Perfil

class VistaRecepcionistaPerfil(QMainWindow):
    """
    Vista del perfil del recepcionista.
    """

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)

        self.controlador = None

        # Menú lateral.
        self.btnCerrarSesion.clicked.connect(self._on_cerrar_sesion)
        self.btnInicio.clicked.connect(self._on_inicio)
        self.btnRegistroUsuario.clicked.connect(self._on_registrar_usuario)
        self.btnControlAcceso.clicked.connect(self._on_control_acceso)
        self.btnClientes.clicked.connect(self._on_clientes)
        self.btnPerfil.clicked.connect(self._on_perfil)

    # Delegar al controlador

    def _on_cerrar_sesion(self):
        self.controlador.cerrar_sesion()

    def _on_inicio(self):
        self.controlador.ir_inicio()

    def _on_registrar_usuario(self):
        self.controlador.ir_registrar_usuario()

    def _on_control_acceso(self):
        self.controlador.ir_control_acceso()

    def _on_clientes(self):
        self.controlador.ir_clientes()

    def _on_perfil(self):
        self.controlador.ir_perfil()

    def set_controlador(self, ctrl):
        self.controlador = ctrl

    # actualizar ui

    def set_nombre(self, valor: str):
        self.label_Nombre.setText(valor)

    def set_email(self, valor: str):
        self.label_7.setText(valor)

    def set_username(self, valor: str):
        self.label_9.setText(valor)

    def set_direccion(self, valor: str):
        self.label_16.setText(valor)