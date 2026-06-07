"""
Controlador del rol Administrador — Patrón MVC según ejemplo de la profesora.

Responsabilidad:
- Instanciar la Vista y asignarle set_controlador(self)
- Responder a los eventos que la Vista delega
- Llamar al Modelo para obtener/guardar datos
- Llamar a métodos de la Vista para actualizar la UI
- NO conecta botones, NO toca widgets directamente
"""
import os
import io

from src.vista.componentes import MensajeView, TablaView, ImagenView, ArchivoView, BotonesView
from src.modelo.VO.NuevoUsuarioFormVO import NuevoUsuarioFormVO
from src.vista.vistas.vista_admin import (
    VistaAdminInicio,
    VistaAdminUsuariosClientes,
    VistaAdminUsuariosTrabajadores,
    VistaAdminNuevoUsuario,
    VistaAdminClases,
    VistaAdminInscripciones,
    VistaAdminPagos,
    VistaAdminEstadisticas,
)

_VISTAS = {
    'interfaz_admin_inicio.ui':                    VistaAdminInicio,
    'interfaz_admin_usuarios_clientes.ui':          VistaAdminUsuariosClientes,
    'interfaz_admin_usuarios_trabajadores.ui':      VistaAdminUsuariosTrabajadores,
    'interfaz_admin_usuarios_nuevo_usuario.ui':     VistaAdminNuevoUsuario,
    'interfaz_admin_clases.ui':                     VistaAdminClases,
    'interfaz_admin_inscripciones.ui':              VistaAdminInscripciones,
    'interfaz_admin_pagos.ui':                      VistaAdminPagos,
    'interfaz_admin_estadisticas.ui':               VistaAdminEstadisticas,
}


class ControladorAdministrador:

    def __init__(self, modelo, usuario, ruta_ui, vista_login):
        self.modelo = modelo
        self.usuario = usuario
        self.ruta_ui = ruta_ui
        self.vista_login = vista_login
        self.ventana = None

    def abrir(self):
        self.ir_inicio()

    def abrir_pantalla(self, archivo):
        if self.ventana:
            self.ventana.close()
        ruta = os.path.join(self.ruta_ui, archivo)
        ClaseVista = _VISTAS[archivo]
        self.ventana = ClaseVista(ruta)
        self.ventana.set_controlador(self)
        self._añadir_boton_ayuda()
        self.cargar_datos()
        self.ventana.show()

    # ── Navegación ────────────────────────────────────────────────────────
    def ir_inicio(self):                self.abrir_pantalla('interfaz_admin_inicio.ui')
    def ir_usuarios_clientes(self):     self.abrir_pantalla('interfaz_admin_usuarios_clientes.ui')
    def ir_usuarios_trabajadores(self): self.abrir_pantalla('interfaz_admin_usuarios_trabajadores.ui')
    def ir_nuevo_usuario(self):         self.abrir_pantalla('interfaz_admin_usuarios_nuevo_usuario.ui')
    def ir_clases(self):                self.abrir_pantalla('interfaz_admin_clases.ui')
    def ir_inscripciones(self):         self.abrir_pantalla('interfaz_admin_inscripciones.ui')
    def ir_pagos(self):                 self.abrir_pantalla('interfaz_admin_pagos.ui')
    def ir_estadisticas(self):          self.abrir_pantalla('interfaz_admin_estadisticas.ui')

    # ── Carga de datos por pantalla ───────────────────────────────────────
    def cargar_datos(self):
        v = self.ventana
        if isinstance(v, VistaAdminInicio):             self._cargar_inicio()
        elif isinstance(v, VistaAdminUsuariosClientes): self._cargar_clientes()
        elif isinstance(v, VistaAdminUsuariosTrabajadores): self._cargar_trabajadores()
        elif isinstance(v, VistaAdminClases):           self._cargar_clases()
        elif isinstance(v, VistaAdminInscripciones):    self._cargar_inscripciones()
        elif isinstance(v, VistaAdminPagos):            self._cargar_pagos()
        elif isinstance(v, VistaAdminEstadisticas):     self._cargar_estadisticas()

    def _cargar_inicio(self):
        v = self.ventana
        try: v.set_num_usuarios(str(self.modelo.contar_usuarios()))
        except: v.set_num_usuarios('0')
        try: v.set_num_clases(str(self.modelo.contar_clases()))
        except: pass
        for tipo in ['spinning','zumba','yoga','pilates','crossfit']:
            try: v.set_clases_por_tipo(tipo, str(self.modelo.contar_inscripciones_clase(tipo)))
            except: v.set_clases_por_tipo(tipo, '0')
        try: v.set_clientes_basico(str(self.modelo.contar_clientes_tarifa('basico')))
        except: pass
        try: v.set_clientes_premium(str(self.modelo.contar_clientes_tarifa('premium')))
        except: pass
        try: v.cargar_tabla_inscripciones(self.modelo.listar_inscripciones_resumen())
        except Exception as e: print('Error tabla inscripciones inicio:', e)
        try:
            datos_pend = self.modelo.clientes_pendientes_admin()
            v.cargar_tabla_pagos_pendientes(
                ['ID cliente','Nombre','Tarifa','Precio'], datos_pend
            )
        except Exception as e: print('Error tabla pagos pendientes inicio:', e)
        try: self._dibujar_grafico()
        except Exception as e: print('Error grafico:', e)

    def _cargar_clientes(self):
        v = self.ventana
        try:
            datos = self.modelo.listar_clientes_completo()
            v.cargar_tabla(datos)
            v.set_num_usuarios(str(len(datos)))
            v.set_texto_mostrando(f'Mostrando {len(datos)} clientes')
        except Exception as e: print('Error cargar clientes:', e)

    def _cargar_trabajadores(self):
        v = self.ventana
        try:
            datos = self.modelo.listar_trabajadores_completo()
            v.cargar_tabla(datos)
            resumen = self.modelo.resumen_trabajadores_por_rol(datos)
            v.set_resumen(
                resumen['total'], resumen['entrenadores'],
                resumen['recepcionistas'], resumen['contables'],
                resumen['administradores']
            )
            v.set_texto_mostrando(f'Mostrando {len(datos)} trabajadores')
        except Exception as e: print('Error cargar trabajadores:', e)

    def _cargar_clases(self):
        v = self.ventana
        try:
            datos = self.modelo.listar_clases()
            v.cargar_tabla(datos)
            v.set_total_clases(str(len(datos)))
        except Exception as e: print('Error cargar clases:', e)

    def _cargar_inscripciones(self):
        v = self.ventana
        try:
            datos = self.modelo.listar_inscripciones_resumen()
            v.cargar_tabla(datos)
            try:
                stats = self.modelo.estadisticas_inscripciones()
                v.set_stats(stats)
            except: pass
            v.set_texto_mostrando(f'Mostrando {len(datos)} inscripciones')
        except Exception as e: print('Error cargar inscripciones:', e)

    def _cargar_pagos(self):
        v = self.ventana
        try:
            datos = self.modelo.clientes_pendientes_admin()
            v.cargar_tabla_pagos(datos)
        except Exception as e: print('Error cargar pagos:', e)
        try:
            v.set_resumen_pagos(
                float(self.modelo.ingresos_mes_actual()),
                float(self.modelo.ingresos_anio_actual()),
                int(self.modelo.numero_clientes_pendientes_pago()),
                float(self.modelo.importe_pendiente_cobrar())
            )
        except Exception as e: print('Error resumen pagos:', e)

    def _cargar_estadisticas(self):
        v = self.ventana
        try:
            stats = self.modelo.estadisticas_admin()
            v.set_stats(stats)
        except Exception as e: print('Error stats admin:', e)
        try:
            ranking = self.modelo.ranking_usuarios_activos_estadisticas()
            v.cargar_tabla_ranking(ranking)
        except Exception as e: print('Error ranking:', e)
        try:
            ocupacion = self.modelo.ocupacion_por_clase_estadisticas()
            for i in range(4):
                if i < len(ocupacion):
                    nombre = str(ocupacion[i].nombre_actividad)
                    pct = int(ocupacion[i].ocupacion) if ocupacion[i].ocupacion is not None else 0
                else:
                    nombre, pct = '-', 0
                v.set_ocupacion_clase(i, nombre, pct)
        except Exception as e: print('Error ocupacion:', e)

    # ── Acciones ──────────────────────────────────────────────────────────
    def filtrar_clientes(self):
        v = self.ventana
        try:
            texto = v.get_texto_buscar()
            datos = self.modelo.buscar_clientes(texto) if texto else self.modelo.listar_clientes_completo()
            v.cargar_tabla(datos)
            v.set_texto_mostrando(f'Mostrando {len(datos)} clientes')
        except Exception as e: print('Error filtrar clientes:', e)

    def filtrar_trabajadores(self):
        v = self.ventana
        try:
            texto = v.get_texto_buscar()
            datos = self.modelo.buscar_trabajadores(texto) if texto else self.modelo.listar_trabajadores_completo()
            v.cargar_tabla(datos)
            v.set_texto_mostrando(f'Mostrando {len(datos)} trabajadores')
        except Exception as e: print('Error filtrar trabajadores:', e)

    def filtrar_por_rol(self):
        v = self.ventana
        try:
            rol = v.get_rol_filtro()
            datos = (self.modelo.listar_trabajadores_completo()
                     if rol == 'Todos los roles'
                     else self.modelo.buscar_trabajadores_rol(rol))
            v.cargar_tabla(datos)
            v.set_texto_mostrando(f'Mostrando {len(datos)} trabajadores')
        except Exception as e: print('Error filtrar rol:', e)

    def guardar_cambios_trabajador(self):
        v = self.ventana
        try:
            filas = v.get_datos_tabla()
            for fila in filas:
                id_str = fila[0]
                if not id_str:
                    continue
                id_usuario = int(id_str)
                nombre, telefono, email, direccion = fila[2], fila[3], fila[4], fila[7]
                self.modelo.guardar_cambios_trabajador(
                    id_usuario, nombre, telefono, email, direccion
                )
            v.mostrar_exito('Cambios guardados correctamente')
        except Exception as e:
            v.mostrar_error(str(e))

    def registrar_usuario(self):
        v = self.ventana
        try:
            dni       = v.get_dni()
            nombre    = v.get_nombre()
            telefono  = v.get_telefono()
            email     = v.get_email()
            direccion = v.get_direccion()
            fecha     = v.get_fecha()
            username  = v.get_username()
            password  = v.get_password()
            confirmar = v.get_confirmar()
            rol_texto = v.get_rol()

            try:
                fecha_bd = self.modelo.validar_nuevo_usuario(
                    dni, nombre, telefono, email, username, password, confirmar, fecha
                )
            except ValueError as e:
                v.mostrar_error(str(e))
                return

            id_rol = self.modelo.rol_texto_a_id(rol_texto)

            nuevo_usuario_vo = NuevoUsuarioFormVO(
                dni, nombre, telefono, email, username, password,
                id_rol, direccion, fecha_bd
            )
            self.modelo.crear_usuario_completo(
                nuevo_usuario_vo.dni, nuevo_usuario_vo.nombre,
                nuevo_usuario_vo.telefono, nuevo_usuario_vo.email,
                nuevo_usuario_vo.username, nuevo_usuario_vo.password,
                nuevo_usuario_vo.id_rol, nuevo_usuario_vo.direccion,
                nuevo_usuario_vo.fecha_nacimiento, self.usuario['id_usuario']
            )
            v.mostrar_exito(f"Usuario '{username}' registrado como {rol_texto}")
            v.limpiar()
        except Exception as e:
            v.mostrar_error(f'Error al registrar: {str(e)}')

    def filtrar_clases(self):
        v = self.ventana
        try:
            texto = v.get_texto_buscar()
            datos = self.modelo.buscar_clases(texto) if texto else self.modelo.listar_clases()
            v.cargar_tabla(datos)
            v.set_total_clases(str(len(datos)))
        except Exception as e: print('Error filtrar clases:', e)

    def anadir_fila_clase(self):
        v = self.ventana
        fi = v.insertar_fila_vacia()
        v.set_total_clases(str(self.ventana.tablaClases.rowCount()))

    def guardar_cambios_clase(self):
        v = self.ventana
        try:
            filas = v.get_datos_tabla()
            for fila in filas:
                id_texto, nombre, dia, hora_ini, hora_fin, aforo, nivel = fila
                if not nombre:
                    continue
                dia      = dia or 'lunes'
                hora_ini = hora_ini or '09:00'
                hora_fin = hora_fin or '10:00'
                nivel    = nivel or 'media'
                try: aforo = int(aforo) if aforo else 20
                except ValueError:
                    v.mostrar_error('El aforo debe ser un número')
                    return
                if id_texto:
                    self.modelo.guardar_cambios_clase_tabla(
                        int(id_texto), nombre, dia, hora_ini, hora_fin, aforo, nivel
                    )
                else:
                    self.modelo.registrar_clase(
                        2, 1, nombre, 300, dia, hora_ini, hora_fin, 60, aforo, nivel
                    )
            v.mostrar_exito('Clases guardadas correctamente')
            self._cargar_clases()
        except Exception as e:
            v.mostrar_error(str(e))

    def filtrar_inscripciones(self):
        v = self.ventana
        try:
            texto = v.get_texto_buscar()
            datos = (self.modelo.buscar_inscripciones(texto)
                     if texto else self.modelo.listar_inscripciones_resumen())
            v.cargar_tabla(datos)
            v.set_texto_mostrando(f'Mostrando {len(datos)} inscripciones')
        except Exception as e: print('Error filtrar inscripciones:', e)

    def filtrar_pagos_pendientes(self):
        v = self.ventana
        try:
            texto = v.get_texto_buscar()
            datos = (self.modelo.buscar_cliente_pendiente_por_dni_admin(texto)
                     if texto else self.modelo.clientes_pendientes_admin())
            v.cargar_tabla_pagos(datos)
            try:
                v.set_resumen_pagos(
                    float(self.modelo.ingresos_mes_actual()),
                    float(self.modelo.ingresos_anio_actual()),
                    int(self.modelo.numero_clientes_pendientes_pago()),
                    float(self.modelo.importe_pendiente_cobrar())
                )
            except: pass
        except Exception as e: print('Error filtrar pagos:', e)

    def crear_copia_seguridad(self):
        v = self.ventana
        try:
            ruta = self.modelo.crear_copia_seguridad()
            v.mostrar_exito(f'Copia creada correctamente:\n\n{ruta}')
        except Exception as e:
            v.mostrar_error(f'No se pudo crear la copia:\n\n{e}')

    def restaurar_copia_seguridad(self):
        v = self.ventana
        ruta_sql = ArchivoView.seleccionar_archivo_sql(v, 'Seleccionar copia de seguridad')
        if not ruta_sql:
            return
        try:
            self.modelo.restaurar_copia_seguridad(ruta_sql)
            v.mostrar_exito('Copia restaurada correctamente.')
            self.cargar_datos()
        except Exception as e:
            v.mostrar_error(f'No se pudo restaurar:\n\n{e}')

    # Informe

    def _dibujar_grafico(self):
        try:
            datos = self.modelo.ingresos_por_mes()
            if not datos:
                return
            meses = ['','Ene','Feb','Mar','Abr','May','Jun',
                    'Jul','Ago','Sep','Oct','Nov','Dic']
            etiquetas = [f"{meses[int(r.mes)]}\n{str(r.anio)[-2:]}" for r in datos][::-1]
            valores   = [float(r.total) for r in datos][::-1]
            # Pasa los datos a la vista, que se encarga de dibujar
            self.ventana.dibujar_grafico_ingresos(etiquetas, valores)
        except Exception as e:
            print('Error grafico:', e)

    # ── Cerrar sesión ─────────────────────────────────────────────────────
    def cerrar_sesion(self):
        if self.ventana:
            self.ventana.close()
        self.vista_login.show()

    # ── Ayuda ─────────────────────────────────────────────────────────────
    def _añadir_boton_ayuda(self):
        BotonesView.crear_boton_ayuda(self.ventana, 1015, 20, self._mostrar_ayuda)

    def _mostrar_ayuda(self):
        v = self.ventana
        if isinstance(v, VistaAdminInicio):
            MensajeView.information(v, 'Ayuda — Inicio',
                'Panel de control del administrador.\n\n'
                '• Resumen global: usuarios, clases e inscripciones.\n'
                '• Usa Backup para crear o restaurar copias de seguridad.')
        elif isinstance(v, VistaAdminUsuariosClientes):
            MensajeView.information(v, 'Ayuda — Clientes',
                'Consulta y gestiona los clientes del gimnasio.\n\n'
                '• Usa el buscador para filtrar por nombre.\n'
                '• Haz doble clic en una celda para editar.')
        elif isinstance(v, VistaAdminUsuariosTrabajadores):
            MensajeView.information(v, 'Ayuda — Trabajadores',
                'Lista del personal del gimnasio.\n\n'
                '• Filtra por rol con el desplegable.\n'
                '• Edita celdas y pulsa Guardar cambios.')
        elif isinstance(v, VistaAdminNuevoUsuario):
            MensajeView.information(v, 'Ayuda — Nuevo usuario',
                'Registra un nuevo usuario en el sistema.\n\n'
                '• Selecciona el rol antes de rellenar el formulario.\n'
                '• Todos los campos son obligatorios.')
        elif isinstance(v, VistaAdminClases):
            MensajeView.information(v, 'Ayuda — Clases',
                'Administra las clases del gimnasio.\n\n'
                '• Pulsa Nueva clase para añadir una fila.\n'
                '• Edita y pulsa Guardar cambios.')
        elif isinstance(v, VistaAdminInscripciones):
            MensajeView.information(v, 'Ayuda — Inscripciones',
                'Consulta todas las inscripciones activas.\n\n'
                '• Filtra por nombre de cliente o clase.')
        elif isinstance(v, VistaAdminPagos):
            MensajeView.information(v, 'Ayuda — Pagos',
                'Gestión de pagos y cobros pendientes.\n\n'
                '• Filtra por DNI para localizar un cliente.')
        elif isinstance(v, VistaAdminEstadisticas):
            MensajeView.information(v, 'Ayuda — Estadísticas',
                'Vista global de la actividad del gimnasio.\n\n'
                '• Ranking de clientes más activos.\n'
                '• Ocupación por clase.')