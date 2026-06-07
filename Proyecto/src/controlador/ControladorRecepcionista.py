"""
Controlador del rol Recepcionista — Patrón MVC según ejemplo de la profesora.

Responsabilidad del Controlador:
- Instanciar la Vista y asignarle la referencia al controlador (set_controlador)
- Responder a los eventos que la Vista delega (ir_inicio, registrar_cliente, etc.)
- Llamar al Modelo para obtener/guardar datos
- Llamar a métodos de la Vista para actualizar la UI (set_xxx, cargar_tabla_xxx)
- NO carga .ui directamente
- NO conecta botones
- NO toca widgets directamente
"""
import os
from src.vista.componentes import MensajeView, BotonesView
from src.modelo.VO.NuevoUsuarioFormVO import NuevoUsuarioFormVO
from src.modelo.VO.ModificacionPerfilVO import ModificacionPerfilVO
from src.vista.vistas.vista_recepcionista import (
    VistaRecepcionistaInicio,
    VistaRecepcionistaRegistrarUsuario,
    VistaRecepcionistaControlAcceso,
    VistaRecepcionistaClientes,
    VistaRecepcionistaPerfil,
)

_VISTAS = {
    'interfaz_recepcionista.ui': VistaRecepcionistaInicio,
    'interfaz_recepcionista_registrar_usuario.ui': VistaRecepcionistaRegistrarUsuario,
    'interfaz_recepcionista_control_de_acceso.ui': VistaRecepcionistaControlAcceso,
    'interfaz_recepcionista_clientes.ui': VistaRecepcionistaClientes,
    'interfaz_recepcionista_perfil.ui': VistaRecepcionistaPerfil,
}


class ControladorRecepcionista:

    def __init__(self, modelo, usuario, ruta_ui, vista_login):
        self.modelo = modelo
        self.usuario = usuario
        self.ruta_ui = ruta_ui
        self.vista_login = vista_login
        self.ventana = None
        self.cliente_control_actual = None

    def abrir(self):
        self.ir_inicio()

    def abrir_pantalla(self, archivo):
        if self.ventana:
            self.ventana.close()
        ruta = os.path.join(self.ruta_ui, archivo)
        ClaseVista = _VISTAS[archivo]
        # Instanciamos la vista — ella sola conecta sus botones en __init__
        self.ventana = ClaseVista(ruta)
        # Le damos la referencia al controlador para que pueda llamarnos
        self.ventana.set_controlador(self)
        # Añadimos el botón de ayuda
        self._añadir_boton_ayuda()
        # Cargamos los datos llamando a métodos de la vista
        self.cargar_datos()
        self.ventana.show()

    # ── Navegación ────────────────────────────────────────────────────────
    def ir_inicio(self):
        self.abrir_pantalla('interfaz_recepcionista.ui')

    def ir_registrar_usuario(self):
        self.abrir_pantalla('interfaz_recepcionista_registrar_usuario.ui')

    def ir_control_acceso(self):
        self.abrir_pantalla('interfaz_recepcionista_control_de_acceso.ui')

    def ir_clientes(self):
        self.abrir_pantalla('interfaz_recepcionista_clientes.ui')

    def ir_perfil(self):
        self.abrir_pantalla('interfaz_recepcionista_perfil.ui')

    # ── Carga de datos — llama a métodos de la Vista ──────────────────────
    def cargar_datos(self):
        if isinstance(self.ventana, VistaRecepcionistaInicio):
            self._cargar_inicio()
        elif isinstance(self.ventana, VistaRecepcionistaControlAcceso):
            self._cargar_control_acceso()
        elif isinstance(self.ventana, VistaRecepcionistaClientes):
            self._cargar_clientes()
        elif isinstance(self.ventana, VistaRecepcionistaPerfil):
            self._cargar_perfil()

    def _cargar_inicio(self):
        v = self.ventana
        try:
            v.set_num_clientes(str(self.modelo.recepcion_total_clientes()))
        except Exception:
            v.set_num_clientes('0')
        try:
            v.set_num_entradas(str(self.modelo.recepcion_entradas_hoy()))
        except Exception:
            v.set_num_entradas('0')
        try:
            v.set_num_clases_hoy(str(self.modelo.recepcion_clases_hoy()))
        except Exception:
            v.set_num_clases_hoy('0')
        try:
            v.cargar_tabla_registros(
                ['Cliente', 'DNI', 'Tipo acceso', 'Fecha y hora'],
                self.modelo.recepcion_ultimos_registros_acceso()
            )
        except Exception as e:
            print('Error tabla registros:', e)
        try:
            v.cargar_tabla_clientes_recientes(
                ['Cliente', 'DNI', 'Teléfono', 'Fecha registro'],
                self.modelo.recepcion_clientes_recientes()
            )
        except Exception as e:
            print('Error tabla clientes recientes:', e)

    def _cargar_control_acceso(self):
        v = self.ventana
        v.limpiar_cliente()
        try:
            datos = self.modelo.listar_ultimos_accesos_control()
            v.cargar_tabla_accesos(
                ['Cliente', 'DNI', 'Tipo acceso', 'Fecha y hora'], datos
            )
        except Exception as e:
            print('Error cargando accesos:', e)

    def _cargar_clientes(self):
        v = self.ventana
        try:
            v.set_total_clientes(str(self.modelo.recepcion_total_clientes_lista()))
        except Exception:
            v.set_total_clientes('0')
        try:
            v.set_nuevos_mes(str(self.modelo.recepcion_nuevos_clientes_mes()))
        except Exception:
            v.set_nuevos_mes('0')
        self.filtrar_clientes_recepcionista()

    def _cargar_perfil(self):
        v = self.ventana
        try:
            perfil = self.modelo.perfil_usuario(self.usuario['id_usuario'])
            if not perfil:
                return
            v.set_nombre(str(perfil[2]))
            v.set_email(str(perfil[4]))
            v.set_username(str(perfil[1]))
            v.set_direccion(str(perfil[7]))
        except Exception as e:
            print('Error cargando perfil:', e)

    # ── Acciones — llamadas por la Vista cuando el usuario interactúa ─────
    def registrar_cliente(self):
        v = self.ventana
        try:
            dni          = v.get_dni()
            nombre       = v.get_nombre()
            telefono     = v.get_telefono()
            direccion    = v.get_direccion()
            email        = v.get_email()
            fecha        = v.get_fecha()
            username     = v.get_username()
            password     = v.get_password()
            confirmar    = v.get_confirmar()
            dni_tutor    = v.get_dni_tutor()
            nombre_tutor = v.get_nombre_tutor()
            plan         = v.get_plan()
            es_menor     = v.es_menor()
            es_adulto    = v.es_adulto()

            try:
                self.modelo.validar_datos_registro_cliente(
                    dni, nombre, telefono, direccion, email, fecha,
                    username, password, confirmar, es_adulto, es_menor, plan
                )
                fecha_bd = self.modelo.convertir_fecha_a_bd(fecha)
            except ValueError as e:
                v.mostrar_error(str(e))
                return

            nuevo_vo = NuevoUsuarioFormVO(
                dni, nombre, telefono, email, username, password, 1, direccion, fecha_bd
            )
            id_cliente = self.modelo.crear_cliente_desde_recepcion(
                nuevo_vo.dni, nuevo_vo.nombre, nuevo_vo.telefono,
                nuevo_vo.email, nuevo_vo.username, nuevo_vo.password,
                nuevo_vo.direccion, nuevo_vo.fecha_nacimiento,
                es_menor, dni_tutor, nombre_tutor, plan
            )
            v.mostrar_exito(f'Cliente registrado correctamente con ID {id_cliente}')
            v.limpiar_formulario()

        except Exception as e:
            v.mostrar_error(f'Error al registrar cliente: {str(e)}')

    def buscar_cliente_control_acceso(self):
        v = self.ventana
        texto = v.get_dni_id()
        if not texto:
            v.limpiar_cliente()
            self.cliente_control_actual = None
            return
        try:
            cliente = self.modelo.buscar_cliente_acceso_por_dni_o_id(texto)
        except Exception:
            cliente = None
        if not cliente:
            v.set_cliente_no_encontrado()
            self.cliente_control_actual = None
            return
        id_usuario, dni, nombre, estado_pago = cliente
        self.cliente_control_actual = {'id_usuario': id_usuario, 'dni': dni, 'nombre': nombre}
        v.set_cliente_encontrado(nombre, dni, id_usuario, estado_pago)

    def registrar_acceso_control(self, tipo_acceso):
        v = self.ventana
        if not self.cliente_control_actual:
            v.mostrar_error('Primero busca un cliente por DNI o ID')
            return
        try:
            self.modelo.registrar_acceso_cliente_control(
                self.cliente_control_actual['id_usuario'], tipo_acceso
            )
            v.mostrar_exito(f'{tipo_acceso.capitalize()} registrada correctamente')
            datos = self.modelo.listar_ultimos_accesos_control()
            v.cargar_tabla_accesos(['Cliente', 'DNI', 'Tipo acceso', 'Fecha y hora'], datos)
        except Exception as e:
            v.mostrar_error(str(e))

    def filtrar_clientes_recepcionista(self):
        v = self.ventana
        try:
            dni  = v.get_filtro_dni()
            tipo = v.get_filtro_tipo()
            plan = v.get_filtro_plan()
            datos = self.modelo.recepcion_listar_clientes_filtrados(dni, tipo, plan)
            cabeceras = [
                'ID', 'DNI', 'Nombre', 'Teléfono', 'Email',
                'Dirección', 'Nacimiento', 'Estado pago', 'Tipo', 'Plan'
            ]
            v.cargar_tabla_clientes(cabeceras, datos)
        except Exception as e:
            print('Error filtrando clientes:', e)

    def guardar_cambios_clientes_recepcionista(self):
        v = self.ventana
        try:
            for fila in range(v.num_filas()):
                fila_datos = v.get_fila_tabla(fila, 8)
                id_str = fila_datos[0]
                if not id_str:
                    continue
                id_cliente = int(id_str)
                _, dni, nombre, telefono, email, direccion, nacimiento, estado_pago = fila_datos
                self.modelo.recepcion_guardar_cambios_cliente(
                    id_cliente, dni, nombre, telefono,
                    email, direccion, nacimiento, estado_pago
                )
            v.mostrar_exito('Cambios guardados correctamente')
            self.filtrar_clientes_recepcionista()
        except Exception as e:
            v.mostrar_error(f'Error al guardar cambios: {str(e)}')

    # ── Cerrar sesión ─────────────────────────────────────────────────────
    def cerrar_sesion(self):
        if self.ventana:
            self.ventana.close()
        self.vista_login.show()

    # ── Ayuda ─────────────────────────────────────────────────────────────
    def _añadir_boton_ayuda(self):
        BotonesView.crear_boton_ayuda(self.ventana, 1005, 30, self._mostrar_ayuda)

    def _mostrar_ayuda(self):
        v = self.ventana
        if isinstance(v, VistaRecepcionistaInicio):
            MensajeView.information(v, 'Ayuda — Inicio',
                'Panel de control de la recepción.\n\n'
                '• Resumen del día: clientes totales, entradas y clases de hoy.\n'
                '• La tabla muestra los últimos accesos registrados.\n'
                '• Usa el menú lateral para navegar entre secciones.')
        elif isinstance(v, VistaRecepcionistaRegistrarUsuario):
            MensajeView.information(v, 'Ayuda — Registrar usuario',
                'Formulario para dar de alta un nuevo cliente.\n\n'
                '• Rellena todos los campos: nombre, DNI, email, teléfono y dirección.\n'
                '• Selecciona si es adulto o menor de edad.\n'
                '• Elige el plan de tarifa y pulsa el botón de registrar.')
        elif isinstance(v, VistaRecepcionistaControlAcceso):
            MensajeView.information(v, 'Ayuda — Control de acceso',
                'Gestiona entradas y salidas del gimnasio.\n\n'
                '• Introduce el DNI o ID del cliente en el buscador.\n'
                '• Pulsa Entrada cuando el cliente entre al gimnasio.\n'
                '• Pulsa Salida cuando el cliente abandone el gimnasio.')
        elif isinstance(v, VistaRecepcionistaClientes):
            MensajeView.information(v, 'Ayuda — Clientes',
                'Consulta y edita los datos de los clientes.\n\n'
                '• Filtra por DNI, tipo o plan con los controles superiores.\n'
                '• Haz doble clic en una celda para editar sus datos.\n'
                '• Pulsa Guardar cambios para confirmar la edición.')
        elif isinstance(v, VistaRecepcionistaPerfil):
            MensajeView.information(v, 'Ayuda — Mi perfil',
                'Información de tu cuenta de recepcionista.\n\n'
                '• Aquí puedes consultar tus datos personales registrados.\n'
                '• Contacta con el administrador si necesitas modificar tu información.')