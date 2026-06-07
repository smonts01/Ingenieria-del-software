"""
Controlador del rol Recepcionista.
Responsabilidad:
- Recibir las acciones que la Vista delega.
- Decidir qué operación debe ejecutarse.
- Pedir datos al Modelo/Logica.
- Enviar datos a la Vista para que los muestre.
"""

import os
from src.vista.componentes import MensajeView, BotonesView

# VO usado para transportar los datos del formulario de registro.
from src.modelo.VO.NuevoUsuarioFormVO import NuevoUsuarioFormVO

# VO relacionado con modificación de perfil.
from src.modelo.VO.ModificacionPerfilVO import ModificacionPerfilVO

# Importamos las clases Vista del rol recepcionista.
# Cada clase Vista carga su .ui y conoce sus botones.
from src.vista.vistas.vista_recepcionista import (
    VistaRecepcionistaInicio,
    VistaRecepcionistaRegistrarUsuario,
    VistaRecepcionistaControlAcceso,
    VistaRecepcionistaClientes,
    VistaRecepcionistaPerfil,
)

# Diccionario que relaciona cada archivo .ui con su clase Vista.
# El controlador decide qué pantalla abrir, pero no dibuja la interfaz.
_VISTAS = {
    'interfaz_recepcionista.ui': VistaRecepcionistaInicio,
    'interfaz_recepcionista_registrar_usuario.ui': VistaRecepcionistaRegistrarUsuario,
    'interfaz_recepcionista_control_de_acceso.ui': VistaRecepcionistaControlAcceso,
    'interfaz_recepcionista_clientes.ui': VistaRecepcionistaClientes,
    'interfaz_recepcionista_perfil.ui': VistaRecepcionistaPerfil,
}


class ControladorRecepcionista:

    def __init__(self, modelo, usuario, ruta_ui, vista_login):
        # Desde aquí se accede a las operaciones de clientes, accesos, perfil, etc.
        self.modelo = modelo

        # Usuario recepcionista que ha iniciado sesión.
        self.usuario = usuario

        # Ruta donde están los archivos .ui.
        self.ruta_ui = ruta_ui

        # Vista de login, se guarda para volver a ella al cerrar sesión.
        self.vista_login = vista_login

        # Ventana actual del rol recepcionista.
        self.ventana = None

        # Cliente seleccionado en la pantalla de control de acceso.
        self.cliente_control_actual = None

    def abrir(self):
        # Al entrar como recepcionista, se abre la pantalla de inicio.
        self.ir_inicio()

    def abrir_pantalla(self, archivo):
        """
        Abre una pantalla del rol recepcionista.
        Flujo:
        Controlador -> elige pantalla -> crea Vista -> set_controlador -> cargar datos -> mostrar.
        La vista recibe el controlador y conecta sus propios eventos.
        """

        # Si ya hay una ventana abierta, se cierra antes de abrir otra.
        if self.ventana:
            self.ventana.close()

        # Construimos la ruta completa del archivo .ui.
        ruta = os.path.join(self.ruta_ui, archivo)

        # Buscamos qué clase Vista corresponde a ese archivo.
        ClaseVista = _VISTAS[archivo]

        # Creamos la vista correspondiente.
        self.ventana = ClaseVista(ruta)

        # Pasamos el controlador a la vista.
        # Así la vista puede llamar a métodos.
        self.ventana.set_controlador(self)

        # Añadimos botón de ayuda.
        self._añadir_boton_ayuda()

        # Cargamos los datos iniciales de la pantalla.
        self.cargar_datos()

        # Mostramos la ventana.
        self.ventana.show()

    # Abrir pantallas

    def ir_inicio(self):
        # Abre el panel principal de recepción.
        self.abrir_pantalla('interfaz_recepcionista.ui')

    def ir_registrar_usuario(self):
        # Abre el formulario para registrar clientes.
        self.abrir_pantalla('interfaz_recepcionista_registrar_usuario.ui')

    def ir_control_acceso(self):
        # Abre la pantalla de entradas y salidas.
        self.abrir_pantalla('interfaz_recepcionista_control_de_acceso.ui')

    def ir_clientes(self):
        # Abre la pantalla de listado y edición de clientes.
        self.abrir_pantalla('interfaz_recepcionista_clientes.ui')

    def ir_perfil(self):
        # Abre la pantalla del perfil del recepcionista.
        self.abrir_pantalla('interfaz_recepcionista_perfil.ui')

    # Cargar datos

    def cargar_datos(self):
        """
        Decide qué datos cargar dependiendo de la pantalla abierta.
        El controlador no calcula los datos.
        Solo llama al método que corresponda a la carga de datos que querramos hacer.
        """

        if isinstance(self.ventana, VistaRecepcionistaInicio):
            self._cargar_inicio()

        elif isinstance(self.ventana, VistaRecepcionistaControlAcceso):
            self._cargar_control_acceso()

        elif isinstance(self.ventana, VistaRecepcionistaClientes):
            self._cargar_clientes()

        elif isinstance(self.ventana, VistaRecepcionistaPerfil):
            self._cargar_perfil()

    def _cargar_inicio(self):
        # Carga los datos resumen del panel inicial de recepción.
        v = self.ventana

        try:
            # Pide al modelo el número total de clientes.
            v.set_num_clientes(str(self.modelo.recepcion_total_clientes()))
        except Exception:
            v.set_num_clientes('0')

        try:
            # Pide al modelo las entradas registradas hoy.
            v.set_num_entradas(str(self.modelo.recepcion_entradas_hoy()))
        except Exception:
            v.set_num_entradas('0')

        try:
            # Pide al modelo el número de clases programadas hoy.
            v.set_num_clases_hoy(str(self.modelo.recepcion_clases_hoy()))
        except Exception:
            v.set_num_clases_hoy('0')

        try:
            # Carga en la vista la tabla de últimos accesos.
            v.cargar_tabla_registros(
                ['Cliente', 'DNI', 'Tipo acceso', 'Fecha y hora'],
                self.modelo.recepcion_ultimos_registros_acceso()
            )
        except Exception as e:
            print('Error tabla registros:', e)

        try:
            # Carga clientes registrados recientemente.
            v.cargar_tabla_clientes_recientes(
                ['Cliente', 'DNI', 'Teléfono', 'Fecha registro'],
                self.modelo.recepcion_clientes_recientes()
            )
        except Exception as e:
            print('Error tabla clientes recientes:', e)

    def _cargar_control_acceso(self):
        # Carga la pantalla de control de entradas y salidas.
        v = self.ventana

        # Limpia el panel del cliente seleccionado.
        v.limpiar_cliente()

        try:
            # Pide al modelo los últimos accesos registrados.
            datos = self.modelo.listar_ultimos_accesos_control()

            # La vista se encarga de pintar la tabla.
            v.cargar_tabla_accesos(
                ['Cliente', 'DNI', 'Tipo acceso', 'Fecha y hora'],
                datos
            )
        except Exception as e:
            print('Error cargando accesos:', e)

    def _cargar_clientes(self):
        # Carga la pantalla de clientes.
        v = self.ventana

        try:
            v.set_total_clientes(str(self.modelo.recepcion_total_clientes_lista()))
        except Exception:
            v.set_total_clientes('0')

        try:
            v.set_nuevos_mes(str(self.modelo.recepcion_nuevos_clientes_mes()))
        except Exception:
            v.set_nuevos_mes('0')

        # Aplica los filtros actuales y carga la tabla.
        self.filtrar_clientes_recepcionista()

    def _cargar_perfil(self):
        # Carga los datos del perfil del recepcionista autenticado.
        v = self.ventana

        try:
            perfil = self.modelo.perfil_usuario(self.usuario['id_usuario'])

            if not perfil:
                return

            # El controlador pasa datos a la vista
            v.set_nombre(str(perfil[2]))
            v.set_email(str(perfil[4]))
            v.set_username(str(perfil[1]))
            v.set_direccion(str(perfil[7]))

        except Exception as e:
            print('Error cargando perfil:', e)

    # Acciones

    def registrar_cliente(self):
        """
        Registra un nuevo cliente desde recepción.
        La vista nos da los datos con getters.
        El controlador valida llamando al modelo.
        Luego crea un VO y delega el alta al modelo.
        """

        v = self.ventana

        try:
            # Recogemos los datos del formulario mediante getters de la vista.
            dni = v.get_dni()
            nombre = v.get_nombre()
            telefono = v.get_telefono()
            direccion = v.get_direccion()
            email = v.get_email()
            fecha = v.get_fecha()
            username = v.get_username()
            password = v.get_password()
            confirmar = v.get_confirmar()
            dni_tutor = v.get_dni_tutor()
            nombre_tutor = v.get_nombre_tutor()
            plan = v.get_plan()
            es_menor = v.es_menor()
            es_adulto = v.es_adulto()

            try:
                # La validación se delega al modelo/lógica.
                self.modelo.validar_datos_registro_cliente(
                    dni, nombre, telefono, direccion, email, fecha,
                    username, password, confirmar, es_adulto, es_menor, plan
                )

                # El modelo transforma la fecha al formato de la base de datos.
                fecha_bd = self.modelo.convertir_fecha_a_bd(fecha)

            except ValueError as e:
                # Si hay error de validación, se informa a la vista.
                v.mostrar_error(str(e))
                return

            # Creamos un VO para transportar los datos del formulario.
            nuevo_vo = NuevoUsuarioFormVO(
                dni, nombre, telefono, email, username, password, 1, direccion, fecha_bd
            )

            # El alta real se delega al modelo.
            id_cliente = self.modelo.crear_cliente_desde_recepcion(
                nuevo_vo.dni,
                nuevo_vo.nombre,
                nuevo_vo.telefono,
                nuevo_vo.email,
                nuevo_vo.username,
                nuevo_vo.password,
                nuevo_vo.direccion,
                nuevo_vo.fecha_nacimiento,
                es_menor,
                dni_tutor,
                nombre_tutor,
                plan
            )

            # Se informa a la vista del resultado.
            v.mostrar_exito(f'Cliente registrado correctamente con ID {id_cliente}')

            # Se limpia el formulario después del alta.
            v.limpiar_formulario()

        except Exception as e:
            v.mostrar_error(f'Error al registrar cliente: {str(e)}')

    def buscar_cliente_control_acceso(self):
        # Busca un cliente para registrar entrada o salida.
        v = self.ventana

        # Se obtiene el texto escrito en la vista.
        texto = v.get_dni_id()

        if not texto:
            v.limpiar_cliente()
            self.cliente_control_actual = None
            return

        try:
            # La búsqueda se delega al modelo.
            cliente = self.modelo.buscar_cliente_acceso_por_dni_o_id(texto)
        except Exception:
            cliente = None

        if not cliente:
            v.set_cliente_no_encontrado()
            self.cliente_control_actual = None
            return

        # El modelo devuelve datos básicos del cliente.
        id_usuario, dni, nombre, estado_pago = cliente

        # Guardamos temporalmente el cliente encontrado para usarlo al registrar acceso.
        self.cliente_control_actual = {
            'id_usuario': id_usuario,
            'dni': dni,
            'nombre': nombre
        }

        # La vista muestra los datos del cliente encontrado.
        v.set_cliente_encontrado(nombre, dni, id_usuario, estado_pago)

    def registrar_acceso_control(self, tipo_acceso):
        # Registra una entrada o salida del cliente seleccionado.
        v = self.ventana

        if not self.cliente_control_actual:
            v.mostrar_error('Primero busca un cliente por DNI o ID')
            return

        try:
            # Delegamos el registro del acceso al modelo.
            self.modelo.registrar_acceso_cliente_control(
                self.cliente_control_actual['id_usuario'],
                tipo_acceso
            )

            v.mostrar_exito(f'{tipo_acceso.capitalize()} registrada correctamente')

            # Recargamos la tabla de accesos.
            datos = self.modelo.listar_ultimos_accesos_control()

            v.cargar_tabla_accesos(
                ['Cliente', 'DNI', 'Tipo acceso', 'Fecha y hora'],
                datos
            )

        except Exception as e:
            v.mostrar_error(str(e))

    def filtrar_clientes_recepcionista(self):
        # Filtra clientes por DNI, tipo o plan.
        v = self.ventana

        try:
            # La vista proporciona los valores seleccionados.
            dni = v.get_filtro_dni()
            tipo = v.get_filtro_tipo()
            plan = v.get_filtro_plan()

            # El modelo devuelve los clientes filtrados.
            datos = self.modelo.recepcion_listar_clientes_filtrados(dni, tipo, plan)

            cabeceras = [
                'ID', 'DNI', 'Nombre', 'Teléfono', 'Email',
                'Dirección', 'Nacimiento', 'Estado pago'
            ]

            # La vista muestra la tabla.
            v.cargar_tabla_clientes(cabeceras, datos)

        except Exception as e:
            print('Error filtrando clientes:', e)

    def guardar_cambios_clientes_recepcionista(self):
        """
        Guarda los cambios editados en la tabla de clientes.
        La vista entrega cada fila de la tabla.
        El controlador envía los datos al modelo.
        El modelo actualizará la BD mediante DAO.
        """

        v = self.ventana

        try:
            for fila in range(v.num_filas()):
                fila_datos = v.get_fila_tabla(fila, 8)

                id_str = fila_datos[0]

                if not id_str:
                    continue

                id_cliente = int(id_str)

                (
                    id_str,
                    dni,
                    nombre,
                    telefono,
                    email,
                    direccion,
                    nacimiento,
                    estado_pago
                ) = fila_datos

                # Delegamos la actualización en el modelo.
                self.modelo.recepcion_guardar_cambios_cliente(
                    id_cliente,
                    dni,
                    nombre,
                    telefono,
                    email,
                    direccion,
                    nacimiento,
                    estado_pago
                )

            v.mostrar_exito('Cambios guardados correctamente')

            # Recargamos la tabla para ver los datos actualizados.
            self.filtrar_clientes_recepcionista()

        except Exception as e:
            v.mostrar_error(f'Error al guardar cambios: {str(e)}')

    # cerrar sesión

    def cerrar_sesion(self):
        # Cierra la ventana actual y vuelve al login.
        if self.ventana:
            self.ventana.close()

        self.vista_login.show()

    # Boton ayuda ?

    def _añadir_boton_ayuda(self):
        # Añade un botón de ayuda común a las pantallas de recepción.
        BotonesView.crear_boton_ayuda(self.ventana, 1005, 30, self._mostrar_ayuda)

    def _mostrar_ayuda(self):
        # Muestra un texto de ayuda diferente según la pantalla actual.
        v = self.ventana

        if isinstance(v, VistaRecepcionistaInicio):
            MensajeView.information(
                v,
                'Ayuda — Inicio',
                'Panel de control de la recepción.\n\n'
                '• Resumen del día: clientes totales, entradas y clases de hoy.\n'
                '• La tabla muestra los últimos accesos registrados.\n'
                '• Usa el menú lateral para navegar entre secciones.'
            )

        elif isinstance(v, VistaRecepcionistaRegistrarUsuario):
            MensajeView.information(
                v,
                'Ayuda — Registrar usuario',
                'Formulario para dar de alta un nuevo cliente.\n\n'
                '• Rellena todos los campos: nombre, DNI, email, teléfono y dirección.\n'
                '• Selecciona si es adulto o menor de edad.\n'
                '• Elige el plan de tarifa y pulsa el botón de registrar.'
            )

        elif isinstance(v, VistaRecepcionistaControlAcceso):
            MensajeView.information(
                v,
                'Ayuda — Control de acceso',
                'Gestiona entradas y salidas del gimnasio.\n\n'
                '• Introduce el DNI o ID del cliente en el buscador.\n'
                '• Pulsa Entrada cuando el cliente entre al gimnasio.\n'
                '• Pulsa Salida cuando el cliente abandone el gimnasio.'
            )

        elif isinstance(v, VistaRecepcionistaClientes):
            MensajeView.information(
                v,
                'Ayuda — Clientes',
                'Consulta y edita los datos de los clientes.\n\n'
                '• Filtra por DNI, tipo o plan con los controles superiores.\n'
                '• Haz doble clic en una celda para editar sus datos.\n'
                '• Pulsa Guardar cambios para confirmar la edición.'
            )

        elif isinstance(v, VistaRecepcionistaPerfil):
            MensajeView.information(
                v,
                'Ayuda — Mi perfil',
                'Información de tu cuenta de recepcionista.\n\n'
                '• Aquí puedes consultar tus datos personales registrados.\n'
                '• Contacta con el administrador si necesitas modificar tu información.'
            )