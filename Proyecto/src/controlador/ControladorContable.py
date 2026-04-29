from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5 import uic


class ControladorContable:
    """
    UC6  · Registrar pago
    UC11 · Gestión de recursos económicos (tarifas, salarios)
    UC12 · Generar informes
    UC14 · Detectar clientes con pagos pendientes
    """

    def __init__(self, modelo, usuario, controlador_principal):
        self.modelo = modelo
        self.usuario = usuario
        self.id_contable = usuario["id_usuario"]
        self.ctrl_principal = controlador_principal
        self.ventana = None

    # ------------------------------------------------------------------
    # Panel principal
    # ------------------------------------------------------------------
    def abrir(self):
        Form, Window = uic.loadUiType("./src/vista/Ui/interfaz_comun.ui")

        class VentanaContable(Window, Form):
            pass

        self.ventana = VentanaContable()
        self._conectar_botones()
        self._cargar_resumen_economico()
        self.ventana.show()

    def _conectar_botones(self):
        v = self.ventana
        if hasattr(v, "btnRegistrarPago"):
            v.btnRegistrarPago.clicked.connect(self.buscarClienteParaPago)
        if hasattr(v, "btnPagosPendientes"):
            v.btnPagosPendientes.clicked.connect(self.detectarClientesPagosPendientes)
        if hasattr(v, "btnGestionEconomica"):
            v.btnGestionEconomica.clicked.connect(self.abrirGestionEconomica)
        if hasattr(v, "btnGenerarInforme"):
            v.btnGenerarInforme.clicked.connect(self.abrirSeleccionInforme)
        if hasattr(v, "btnCerrarSesion"):
            v.btnCerrarSesion.clicked.connect(self._cerrar_sesion)
        # Búsqueda de cliente para registro de pago
        if hasattr(v, "btnBuscarCliente"):
            v.btnBuscarCliente.clicked.connect(self.buscarClienteParaPago)

    def _cargar_resumen_economico(self):
        """Muestra métricas de resumen en el panel de inicio si los labels existen."""
        v = self.ventana
        resumen = self.modelo.obtener_resumen_economico()
        if hasattr(v, "lblTotalRecaudado"):
            v.lblTotalRecaudado.setText(
                f"Recaudado: {resumen.get('total_recaudado', 0):.2f} €"
            )
        if hasattr(v, "lblPendientes"):
            v.lblPendientes.setText(
                f"Pendientes: {resumen.get('total_pendiente', 0):.2f} €"
            )

    # ------------------------------------------------------------------
    # UC6 · Registrar pago
    # ------------------------------------------------------------------
    def buscarClienteParaPago(self):
        v = self.ventana
        texto = _get_text(v, "txtBuscarCliente")
        if not texto:
            QMessageBox.warning(v, "Búsqueda", "Introduce un nombre, DNI o email.")
            return
        clientes = self.modelo.buscar_clientes(texto)
        if not clientes:
            QMessageBox.information(v, "Sin resultados",
                                    "No se encontró ningún cliente.")
            return
        if hasattr(v, "tablaClientesPago"):
            _rellenar_tabla(
                v.tablaClientesPago, clientes,
                ["ID", "Nombre", "DNI", "Email", "Estado pago"],
                ["id_usuario", "nombre", "dni", "email", "estado_pagado"],
            )
        # Conectar selección de la tabla con el botón de registrar pago
        if hasattr(v, "tablaClientesPago") and hasattr(v, "btnConfirmarPago"):
            v.btnConfirmarPago.clicked.connect(self._abrirFormularioPago)

    def _abrirFormularioPago(self):
        v = self.ventana
        tabla = getattr(v, "tablaClientesPago", None)
        if tabla is None:
            return
        fila = tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(v, "Selección", "Selecciona un cliente.")
            return
        id_item = tabla.item(fila, 0)
        if id_item is None:
            return
        id_cliente = int(id_item.text())
        nombre_cliente = tabla.item(fila, 1).text() if tabla.item(fila, 1) else ""

        pagos_pendientes = self.modelo.obtener_pagos_pendientes_cliente(id_cliente)
        if not pagos_pendientes:
            QMessageBox.information(
                v, "Sin pendientes",
                f"{nombre_cliente} no tiene pagos pendientes."
            )
            return

        self._mostrar_dialogo_pago(id_cliente, nombre_cliente, pagos_pendientes)

    def _mostrar_dialogo_pago(self, id_cliente, nombre_cliente, pagos_pendientes):
        Form, Window = uic.loadUiType("./src/vista/Ui/interfaz_comun.ui")

        class VentanaPago(Window, Form):
            pass

        self.ventana_pago = VentanaPago()
        v = self.ventana_pago

        if hasattr(v, "lblCliente"):
            v.lblCliente.setText(f"Cliente: {nombre_cliente}")

        _rellenar_tabla(
            getattr(v, "tablaPagosPendientes", None) or _TablaFake(),
            pagos_pendientes,
            ["ID Pago", "Tarifa", "Importe (€)", "Tipo cuota"],
            ["id_pago", "nombre", "importe", "tipo_cuota"],
        )

        if hasattr(v, "btnPagar"):
            v.btnPagar.clicked.connect(
                lambda: self.registrarPago(id_cliente)
            )
        if hasattr(v, "btnCancelar"):
            v.btnCancelar.clicked.connect(v.close)
        v.show()

    def registrarPago(self, id_cliente):
        v = self.ventana_pago
        tabla = getattr(v, "tablaPagosPendientes", None)
        if tabla is None:
            return
        fila = tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(v, "Selección", "Selecciona el pago a registrar.")
            return
        id_item = tabla.item(fila, 0)
        if id_item is None:
            return
        id_pago = int(id_item.text())

        metodo = _get_combo(v, "cmbMetodoPago") or "efectivo"

        ok, mensaje = self.modelo.registrar_pago(
            id_pago, self.id_contable, metodo
        )
        if ok:
            QMessageBox.information(v, "Pago registrado", mensaje)
            v.close()
            self._cargar_resumen_economico()
        else:
            QMessageBox.critical(v, "Error", mensaje)

    # ------------------------------------------------------------------
    # UC14 · Detectar clientes con pagos pendientes
    # ------------------------------------------------------------------
    def detectarClientesPagosPendientes(self):
        clientes = self.modelo.obtener_clientes_con_pagos_pendientes()
        v = self.ventana
        if not clientes:
            QMessageBox.information(
                v, "Pagos pendientes",
                "No hay clientes con pagos pendientes."
            )
            return

        if hasattr(v, "tablaDeudores"):
            _rellenar_tabla(
                v.tablaDeudores, clientes,
                ["Nombre", "DNI", "Email", "Importe pendiente (€)",
                 "Tarifa", "Fecha pago"],
                ["nombre", "dni", "email", "importe",
                 "nombre_tarifa", "fecha_pago"],
            )
        else:
            lineas = [
                f"{c.get('nombre')} ({c.get('dni')}) — "
                f"{c.get('importe')} € — {c.get('nombre_tarifa')}"
                for c in clientes
            ]
            QMessageBox.warning(v, "Clientes con pagos pendientes",
                                "\n".join(lineas))

    # ------------------------------------------------------------------
    # UC11 · Gestión de recursos económicos
    # ------------------------------------------------------------------
    def abrirGestionEconomica(self):
        Form, Window = uic.loadUiType("./src/vista/Ui/interfaz_comun.ui")

        class VentanaGE(Window, Form):
            pass

        self.ventana_ge = VentanaGE()
        v = self.ventana_ge

        if hasattr(v, "btnVerTarifas"):
            v.btnVerTarifas.clicked.connect(self._cargar_tarifas)
        if hasattr(v, "btnVerSalarios"):
            v.btnVerSalarios.clicked.connect(self._cargar_salarios)
        if hasattr(v, "btnActualizarTarifa"):
            v.btnActualizarTarifa.clicked.connect(self._actualizar_tarifa)
        if hasattr(v, "btnActualizarSalario"):
            v.btnActualizarSalario.clicked.connect(self._actualizar_salario)
        if hasattr(v, "btnVolver"):
            v.btnVolver.clicked.connect(v.close)

        self._cargar_tarifas()
        v.show()

    def _cargar_tarifas(self):
        tarifas = self.modelo.obtener_tarifas()
        v = self.ventana_ge
        if not hasattr(v, "tablaTarifas"):
            return
        _rellenar_tabla(
            v.tablaTarifas, tarifas,
            ["ID", "Nombre", "Precio mensual (€)", "Servicios", "Desde", "Hasta"],
            ["id_tarifa", "nombre", "precio_mensual",
             "servicios_incluidos", "fecha_inicio", "fecha_fin"],
        )

    def _cargar_salarios(self):
        salarios = self.modelo.obtener_salarios_empleados()
        v = self.ventana_ge
        if not hasattr(v, "tablaSalarios"):
            return
        _rellenar_tabla(
            v.tablaSalarios, salarios,
            ["ID Empleado", "Nombre", "Rol", "Salario (€)"],
            ["id_empleado", "nombre", "nombre_rol", "salario"],
        )

    def _actualizar_tarifa(self):
        v = self.ventana_ge
        tabla = getattr(v, "tablaTarifas", None)
        if tabla is None:
            return
        fila = tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(v, "Selección", "Selecciona una tarifa.")
            return
        id_tarifa = int(tabla.item(fila, 0).text())
        nuevo_precio = _get_text(v, "txtNuevoPrecio")
        if not nuevo_precio:
            QMessageBox.warning(v, "Dato requerido", "Introduce el nuevo precio.")
            return
        try:
            precio = float(nuevo_precio.replace(",", "."))
        except ValueError:
            QMessageBox.warning(v, "Formato incorrecto", "El precio debe ser un número.")
            return
        ok, mensaje = self.modelo.actualizar_precio_tarifa(id_tarifa, precio)
        if ok:
            QMessageBox.information(v, "Actualizado", mensaje)
            self._cargar_tarifas()
        else:
            QMessageBox.critical(v, "Error", mensaje)

    def _actualizar_salario(self):
        v = self.ventana_ge
        tabla = getattr(v, "tablaSalarios", None)
        if tabla is None:
            return
        fila = tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(v, "Selección", "Selecciona un empleado.")
            return
        id_empleado = int(tabla.item(fila, 0).text())
        nuevo_salario = _get_text(v, "txtNuevoSalario")
        if not nuevo_salario:
            QMessageBox.warning(v, "Dato requerido", "Introduce el nuevo salario.")
            return
        try:
            salario = float(nuevo_salario.replace(",", "."))
        except ValueError:
            QMessageBox.warning(v, "Formato incorrecto", "El salario debe ser un número.")
            return
        ok, mensaje = self.modelo.actualizar_salario(id_empleado, salario)
        if ok:
            QMessageBox.information(v, "Actualizado", mensaje)
            self._cargar_salarios()
        else:
            QMessageBox.critical(v, "Error", mensaje)

    # ------------------------------------------------------------------
    # UC12 · Generar informes
    # ------------------------------------------------------------------
    def abrirSeleccionInforme(self):
        Form, Window = uic.loadUiType("./src/vista/Ui/interfaz_comun.ui")

        class VentanaInforme(Window, Form):
            pass

        self.ventana_informe = VentanaInforme()
        v = self.ventana_informe

        # Botones por tipo de informe
        tipos = {
            "btnInformePagosRealizados": "pagos_realizados",
            "btnInformePagosPendientes": "pagos_pendientes",
            "btnInformeTarifas":         "tarifas",
            "btnInformeSalarios":        "salarios",
        }
        for btn_name, tipo in tipos.items():
            if hasattr(v, btn_name):
                getattr(v, btn_name).clicked.connect(
                    lambda checked, t=tipo: self.generarInforme(t)
                )
        if hasattr(v, "btnVolver"):
            v.btnVolver.clicked.connect(v.close)
        v.show()

    def generarInforme(self, tipo_informe: str):
        v = self.ventana_informe
        datos, cabeceras, campos = self.modelo.generar_informe(
            tipo_informe, self.id_contable
        )

        if datos is None:
            QMessageBox.critical(v, "Error",
                                 "No se pudo generar el informe. Intenta de nuevo.")
            return
        if not datos:
            QMessageBox.information(v, "Informe vacío",
                                    "No hay datos disponibles para este informe.")
            return

        tabla = getattr(v, "tablaInforme", None)
        if tabla:
            _rellenar_tabla(tabla, datos, cabeceras, campos)
        else:
            # Mostrar como texto si no hay tabla en la UI
            lineas = [" | ".join(str(r.get(c, "")) for c in campos) for r in datos]
            QMessageBox.information(v, f"Informe: {tipo_informe}",
                                    "\n".join(lineas[:50]))  # máx 50 líneas en popup

    # ------------------------------------------------------------------
    def _cerrar_sesion(self):
        self.ventana.close()
        self.ctrl_principal.cerrar_sesion()


# ── Helpers ────────────────────────────────────────────────────────────

class _TablaFake:
    """Sustituto nulo cuando un widget de tabla no existe en la UI."""
    def setColumnCount(self, *a): pass
    def setHorizontalHeaderLabels(self, *a): pass
    def setRowCount(self, *a): pass
    def setItem(self, *a): pass
    def resizeColumnsToContents(self): pass
    def currentRow(self): return -1
    def item(self, *a): return None


def _get_text(v, nombre):
    w = getattr(v, nombre, None)
    return w.text().strip() if w else ""

def _get_combo(v, nombre):
    w = getattr(v, nombre, None)
    return w.currentText().strip() if w else ""

def _rellenar_tabla(tabla, datos, cabeceras, campos):
    if tabla is None:
        return
    tabla.setColumnCount(len(cabeceras))
    tabla.setHorizontalHeaderLabels(cabeceras)
    tabla.setRowCount(len(datos))
    for fi, fila in enumerate(datos):
        for ci, campo in enumerate(campos):
            tabla.setItem(fi, ci, QTableWidgetItem(str(fila.get(campo, ""))))
    tabla.resizeColumnsToContents()
