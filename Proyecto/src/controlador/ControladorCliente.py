"""
Controlador del rol Cliente.
Responsabilidad:
- Recibir las acciones que la Vista delega.
- Decidir qué operación debe ejecutarse.
- Pedir datos al Modelo/Logica.
- Enviar datos a la Vista para que los muestre.
"""

import os
from src.vista.componentes import MensajeView, BotonesView

# VO usado para transportar los datos modificados del perfil.
from src.modelo.VO.ModificacionPerfilVO import ModificacionPerfilVO

# Importamos las clases Vista del rol cliente.
# Cada clase Vista carga su .ui, conoce sus botones y delega acciones al controlador.
from src.vista.vistas.vista_cliente import (
    VistaClienteInicio,
    VistaClienteClasesTodas,
    VistaClienteReservas,
    VistaClienteEstadisticas,
    VistaClientePerfil,
    VistaClienteInformacion,
)


# Diccionario que relaciona cada archivo .ui con su clase Vista.
_VISTAS = {
    'interfaz_cliente_inicio.ui': VistaClienteInicio,
    'interfaz_cliente_clases_todas.ui': VistaClienteClasesTodas,
    'interfaz_cliente_clases_reservas.ui': VistaClienteReservas,
    'interfaz_cliente_estadisticas.ui': VistaClienteEstadisticas,
    'interfaz_cliente_perfil.ui': VistaClientePerfil,
    'interfaz_cliente_informacion.ui': VistaClienteInformacion,
}


class ControladorCliente:

    def __init__(self, modelo, usuario, ruta_ui, vista_login):
        # Desde aquí se accede a clases, pagos, perfil, estadísticas, etc.
        self.modelo = modelo

        # Datos del usuario cliente que ha iniciado sesión.
        self.usuario = usuario

        # Ruta donde están los archivos .ui.
        self.ruta_ui = ruta_ui

        # Vista de login, se guarda para volver a ella al cerrar sesión.
        self.vista_login = vista_login

        # Ventana actual del cliente.
        self.ventana = None

        # VO con los datos principales del cliente.
        # Se carga al abrir cada pantalla para tener datos actualizados.
        self._vo = None

    def abrir(self):
        # Al entrar como cliente, se abre la pantalla de inicio.
        self.ir_inicio()

    def abrir_pantalla(self, archivo):
        """
        Abre una pantalla del cliente.
        Flujo:
        Controlador -> elige pantalla -> crea Vista -> set_controlador -> carga datos -> muestra.
        """

        # Si hay una ventana abierta, se cierra antes de abrir otra.
        if self.ventana:
            self.ventana.close()

        # Construimos la ruta completa del .ui.
        ruta = os.path.join(self.ruta_ui, archivo)

        # Buscamos la clase Vista que corresponde a ese .ui.
        ClaseVista = _VISTAS[archivo]

        # Antes de mostrar la pantalla cargamos el VO actualizado del cliente.
        self._cargar_vo_cliente()

        # Creamos la vista.
        self.ventana = ClaseVista(ruta)

        # Pasamos el controlador a la vista para que pueda delegarle acciones.
        self.ventana.set_controlador(self)

        # Añadimos botón de ayuda.
        self._añadir_boton_ayuda()

        # Cargamos los datos de la pantalla.
        self.cargar_datos()

        # Mostramos la ventana.
        self.ventana.show()

    # interfaces

    def ir_inicio(self):
        self.abrir_pantalla('interfaz_cliente_inicio.ui')

    def ir_clases(self):
        self.abrir_pantalla('interfaz_cliente_clases_todas.ui')

    def ir_reservas(self):
        self.abrir_pantalla('interfaz_cliente_clases_reservas.ui')

    def ir_estadisticas(self):
        self.abrir_pantalla('interfaz_cliente_estadisticas.ui')

    def ir_perfil(self):
        self.abrir_pantalla('interfaz_cliente_perfil.ui')

    def ir_informacion(self):
        self.abrir_pantalla('interfaz_cliente_informacion.ui')

    # VO

    def _cargar_vo_cliente(self):
        """
        Carga el VO principal del cliente.
        El VO agrupa la información necesaria para pintar las pantallas:
        nombre, tarifa, pagos, próximas clases, estadísticas, etc.
        """
        try:
            self._vo = self.modelo.datos_inicio_cliente(self.usuario['id_usuario'])

        except Exception as e:
            print('ERROR AL CARGAR VO CLIENTE:', repr(e))
            self._vo = None

    # Cargar datos

    def cargar_datos(self):
        """
        Decide qué datos cargar según la pantalla actual.
        El controlador pide los datos al modelo y se los pasa a la vista.
        """

        if self._vo is None:
            MensajeView.warning(
                self.ventana,
                'Error',
                'No se pudieron cargar los datos del cliente'
            )
            return

        # Rellena la cabecera común de todas las pantallas.
        self._rellenar_cabecera()

        v = self.ventana

        # Según el tipo de vista abierta, se carga una información u otra.
        if isinstance(v, VistaClienteInicio):
            self._cargar_inicio()

        elif isinstance(v, VistaClienteClasesTodas):
            self._cargar_clases_todas()

        elif isinstance(v, VistaClienteReservas):
            self._cargar_reservas()

        elif isinstance(v, VistaClienteEstadisticas):
            self._cargar_estadisticas()

        elif isinstance(v, VistaClientePerfil):
            self._cargar_perfil()

    def _rellenar_cabecera(self):
        """
        Rellena datos comunes de la cabecera:
        nombre del cliente y fecha de alta.
        """
        vo = self._vo
        v = self.ventana

        v.set_nombre_cliente(str(vo.nombre))
        v.set_fecha_alta(f'Cliente desde {vo.fecha_registro}')

    def _cargar_inicio(self):
        """
        Carga la pantalla inicial del cliente.
        Muestra resumen de clases, pago, calorías y próximas clases.
        """
        v = self.ventana
        vo = self._vo

        v.set_bienvenida(f'Bienvenida, {vo.nombre}')
        v.set_num_clases(str(len(vo.proximas_clases)))
        v.set_estado_pago(str(vo.estado_pagado).capitalize())
        v.set_sub_pago(self.modelo.texto_estado_pago(vo.estado_pagado))
        v.set_calorias_semana(f'{vo.calorias_semana} kcal')
        v.set_asistencias(vo.get_asistencias_str())
        v.set_cuota(str(vo.nombre_tarifa))
        v.set_cantidad_pago(vo.get_precio_str())
        v.set_mes_pago(str(vo.ultimo_pago_fecha))
        v.set_pendiente_pago(str(vo.ultimo_pago_estado).capitalize())

        # La vista se encarga de pintar la tabla.
        v.cargar_tabla_proximas(vo.proximas_clases)

    def _cargar_clases_todas(self):
        """
        Carga la pantalla de clases disponibles.
        Aquí se muestran todas las clases con opción de reservar o cancelar (una vez esten reservadas).
        """
        v = self.ventana
        id_c = self.usuario['id_usuario']

        try:
            # Pedimos al modelo las clases con ocupación.
            clases = self.modelo.clases_ocupacion_cliente()

            # Clases en las que el cliente está inscrito.
            inscritas = self.modelo.clases_inscritas_cliente(id_c)

            # Clases a las que ya ha asistido.
            asistidas = self.modelo.clases_asistidas_cliente(id_c)

            # IDs de clases ya inscritas.
            ids_ins = [ins.id_clase for ins in inscritas]

            # Preparamos los valores de los filtros de tipo de clase.
            nombres = sorted(set(
                str(c.nombre_actividad).strip()
                for c in clases
                if c.nombre_actividad
            ))

            # Preparamos los valores de los filtros de horario.
            horarios = sorted(set(
                f"{str(c.hora_inicio)[:5]} - {str(c.hora_fin)[:5]}"
                for c in clases
                if c.hora_inicio and c.hora_fin
            ))

            # Mandamos los filtros a la vista.
            v.poblar_combo_tipo(nombres)
            v.poblar_combo_horario(horarios)

            # Mandamos el periodo de la semana.
            v.set_periodo(self.modelo.periodo_semana_actual())

            # La vista pinta las cards de clases (donde sale info)
            v.cargar_cards(clases, ids_ins, asistidas)

            # Calculamos una próxima clase sugerida.
            proxima = next((c for c in clases if c.id_clase not in asistidas), None)

            if proxima:
                v.set_prox_datos(
                    f"{proxima.nombre_actividad}\n"
                    f"{proxima.dia_semana} · {str(proxima.hora_inicio)[:5]} - {str(proxima.hora_fin)[:5]}\n"
                    f"{proxima.sala}"
                )
            else:
                v.set_prox_datos("No tienes próximas clases")

        except Exception as e:
            print('Error cargar clases todas:', e)

    def _cargar_reservas(self):
    
    # Carga la pantalla de reservas del cliente.
        
        v = self.ventana

        try:
            reservas = self._vo.proximas_clases
            clases_ocupacion = self.modelo.clases_ocupacion_cliente()

            # Diccionario para consultar ocupación por nombre de clase.
            ocup = {
                str(c.nombre_actividad).lower(): (c.inscritos, c.aforo_maximo)
                for c in clases_ocupacion
            }

            # La vista pinta las reservas.
            v.cargar_cards(reservas, ocup)

        except Exception as e:
            print('Error cargar reservas:', e)

    def _cargar_estadisticas(self):
        
        # Carga la pantalla de estadísticas del cliente.
        
        v = self.ventana
        vo = self._vo

        v.set_periodo(self.modelo.periodo_semana_actual())

        v.set_entrenos(str(vo.entrenos_semana), vo.get_delta_entrenos_str())
        v.set_tiempo(vo.get_tiempo_semana_str(), vo.get_delta_tiempo_str())
        v.set_calorias(f'{vo.calorias_semana} kcal')

        try:
            # El modelo calcula el porcentaje de objetivo semanal.
            objetivo = self.modelo.calcular_objetivo_semanal(vo.calorias_semana)
            v.set_objetivo(objetivo['texto_porcentaje'], objetivo['texto_objetivo'])

        except Exception as e:
            print('Error objetivo:', e)

        v.set_mini(f'Total semanal: {vo.calorias_semana} kcal')

        try:
            # Datos para el gráfico de calorías por día.
            calorias_dias = self.modelo.calorias_semana_por_dia(self.usuario['id_usuario'])
            v.actualizar_barras(calorias_dias)
            v.set_total_calorias(f'Total semanal: {sum(calorias_dias.values())} kcal')

        except Exception as e:
            print('Error barras:', e)

        v.set_dias_label('Lun          Mar          Mié          Jue          Vie          Sáb          Dom')
        v.set_racha(vo.racha_dias)
        v.set_leyendas_distribucion(vo.distribucion_tipos)

    def _cargar_perfil(self):
        
    # Carga la pantalla de perfil del cliente.
        
        v = self.ventana
        vo = self._vo

        v.set_perfil(
            str(vo.nombre),
            str(vo.email),
            str(vo.telefono),
            str(vo.fecha_nacimiento),
            str(vo.direccion),
            f'{vo.asistencias_mes} / {vo.inscripciones_mes} clases'
        )

        try:
            objetivo = self.modelo.calcular_objetivo_semanal(vo.calorias_semana)
            v.set_objetivo(objetivo['texto_porcentaje'])
            v.set_barra_progreso(objetivo['porcentaje'])

        except Exception as e:
            print('Error objetivo perfil:', e)

    # Acciones que se pueden hacer dentro de interfaces

    def reservar_clase_card(self, numero_card):
        """
        Acción para reservar o cancelar una clase desde una card.
        Si la card está en estado cancelar, se desapunta al cliente.
        Si no, se inscribe al cliente en la clase.
        """
        v = self.ventana

        # La vista nos da el nombre de la clase asociada a la card.
        nombre_clase = v.get_nombre_clase_card(numero_card)

        if not nombre_clase:
            MensajeView.warning(v, 'Error', 'No se ha encontrado la clase seleccionada')
            return

        # La vista indica si el botón significa reservar o cancelar.
        accion = v.get_accion_boton_card(numero_card)

        try:
            if accion == 'cancelar':
                # Cancelación de inscripción.
                self.modelo.desapuntarse_clase_por_nombre(
                    self.usuario['id_usuario'],
                    nombre_clase
                )

                MensajeView.information(
                    v,
                    'Reserva cancelada',
                    f'Te has desapuntado de {nombre_clase}.'
                )

            else:
                # Alta de inscripción.
                self.modelo.inscribirse_clase_por_nombre(
                    self.usuario['id_usuario'],
                    nombre_clase
                )

                MensajeView.information(
                    v,
                    'Reserva confirmada',
                    f'Te has inscrito en {nombre_clase}.'
                )

            # Recargamos el VO y la pantalla para ver los cambios.
            self._cargar_vo_cliente()
            self.cargar_datos()

        except Exception as e:
            MensajeView.warning(v, 'Error al gestionar la reserva', str(e))

    def filtrar_clases(self):
        """
        Filtra las cards de clases disponibles.
        """
        v = self.ventana

        if not isinstance(v, VistaClienteClasesTodas):
            return

        v.aplicar_filtro_cards(
            v.get_texto_buscar(),
            v.get_filtro_tipo(),
            v.get_filtro_horario()
        )

    def guardar_perfil(self):
        """
        Guarda cambios del perfil del cliente.
        Usa un VO para transportar los datos modificados.
        """
        v = self.ventana

        telefono = v.get_telefono()
        email = v.get_email()
        direccion = v.get_direccion()

        if not email:
            v.mostrar_error('El email no puede estar vacío')
            return

        try:
            # VO de modificación de perfil.
            perfil_vo = ModificacionPerfilVO(
                self.usuario['id_usuario'],
                telefono,
                email,
                direccion
            )

            # El modelo se encarga de actualizar los datos.
            self.modelo.modificar_usuario(
                perfil_vo.id_usuario,
                perfil_vo.telefono,
                perfil_vo.email,
                perfil_vo.direccion
            )

            v.mostrar_exito('Los cambios se han guardado correctamente')

            # Recargamos el VO y la pantalla.
            self._cargar_vo_cliente()
            self.cargar_datos()

        except Exception as e:
            v.mostrar_error(str(e))

    # Cerrar sesion

    def cerrar_sesion(self):
        """
        Cierra la ventana actual y vuelve al login.
        """
        if self.ventana:
            self.ventana.close()

        self.vista_login.show()

    # Botón ayuda ?

    def _añadir_boton_ayuda(self):
        """
        Añade un botón de ayuda común a las pantallas del cliente.
        """
        BotonesView.crear_boton_ayuda(self.ventana, 1015, 20, self._mostrar_ayuda)

    def _mostrar_ayuda(self):
        """
        Muestra ayuda distinta según la pantalla actual.
        """
        v = self.ventana

        if isinstance(v, VistaClienteInicio):
            MensajeView.information(
                v,
                'Ayuda — Inicio',
                'Esta es tu pantalla de inicio.\n\n'
                '• Aquí ves un resumen de tus próximas clases.\n'
                '• Consulta el estado de tu último pago.\n'
                '• Las calorías muestran tu actividad semanal.'
            )

        elif isinstance(v, VistaClienteClasesTodas):
            MensajeView.information(
                v,
                'Ayuda — Clases disponibles',
                'Aquí puedes ver y reservar clases del gimnasio.\n\n'
                '• Usa el buscador para filtrar por nombre.\n'
                '• El desplegable Categoría filtra por tipo.\n'
                '• Pulsa Reservar para inscribirte.\n'
                '• Pulsa Cancelar si quieres darte de baja.'
            )

        elif isinstance(v, VistaClienteReservas):
            MensajeView.information(
                v,
                'Ayuda — Mis reservas',
                'Aquí aparecen las clases en las que estás inscrito.\n\n'
                '• Solo se muestran tus próximas reservas activas.\n'
                '• Para cancelar ve a Clases disponibles.'
            )

        elif isinstance(v, VistaClienteEstadisticas):
            MensajeView.information(
                v,
                'Ayuda — Estadísticas',
                'Resumen de tu actividad semanal.\n\n'
                '• El gráfico muestra calorías quemadas por día.\n'
                '• La racha indica días consecutivos entrenando.'
            )

        elif isinstance(v, VistaClientePerfil):
            MensajeView.information(
                v,
                'Ayuda — Mi perfil',
                'Visualiza tus datos personales.'
            )

        else:
            MensajeView.information(
                v,
                'Ayuda — Información',
                'Información general del gimnasio.\n\n'
                '• Usa el menú lateral para navegar.'
            )