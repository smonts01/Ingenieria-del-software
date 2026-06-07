"""
Controlador del rol Entrenador — Patrón MVC según ejemplo de la profesora.

Responsabilidad:
- Instanciar la Vista y asignarle set_controlador(self)
- Responder a los eventos que la Vista delega
- Llamar al Modelo para obtener/guardar datos
- Llamar a métodos de la Vista para actualizar la UI
- NO conecta botones, NO toca widgets directamente
"""
import os
from datetime import date

from src.vista.componentes import MensajeView, TablaView, BotonesView
from src.modelo.VO.AsistenciaVO import AsistenciaVO
from src.vista.vistas.vista_entrenador import (
    VistaEntrenadorInicio,
    VistaEntrenadorClases,
    VistaEntrenadorListaClientes,
    VistaEntrenadorOcupacion,
    VistaEntrenadorRegistrarAsistencia,
    VistaEntrenadorPerfil,
    VistaEntrenadorInformacion,
)

_VISTAS = {
    'interfaz_entrenador.ui':                      VistaEntrenadorInicio,
    'interfaz_entrenador_clases.ui':               VistaEntrenadorClases,
    'interfaz_entrenador_verListaClientes.ui':     VistaEntrenadorListaClientes,
    'interfaz_entrenador_ocupacionClases.ui':      VistaEntrenadorOcupacion,
    'interfaz_entrenador_registrar_asistencia.ui': VistaEntrenadorRegistrarAsistencia,
    'interfaz_entrenador_perfil.ui':               VistaEntrenadorPerfil,
    'interfaz_entrenador_informacion.ui':          VistaEntrenadorInformacion,
}


class ControladorEntrenador:

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
    def ir_inicio(self):       self.abrir_pantalla('interfaz_entrenador.ui')
    def ir_clases(self):       self.abrir_pantalla('interfaz_entrenador_clases.ui')
    def ir_inscritos(self):    self.abrir_pantalla('interfaz_entrenador_verListaClientes.ui')
    def ir_ocupacion(self):    self.abrir_pantalla('interfaz_entrenador_ocupacionClases.ui')
    def ir_asistencia(self):   self.abrir_pantalla('interfaz_entrenador_registrar_asistencia.ui')
    def ir_perfil(self):       self.abrir_pantalla('interfaz_entrenador_perfil.ui')
    def ir_informacion(self):  self.abrir_pantalla('interfaz_entrenador_informacion.ui')

    # ── Carga de datos ────────────────────────────────────────────────────
    def cargar_datos(self):
        v = self.ventana
        if isinstance(v, VistaEntrenadorInicio): self._cargar_inicio()
        elif isinstance(v, VistaEntrenadorClases): self._cargar_clases()
        elif isinstance(v, VistaEntrenadorListaClientes): self._cargar_inscritos()
        elif isinstance(v, VistaEntrenadorOcupacion): self._cargar_ocupacion()
        elif isinstance(v, VistaEntrenadorRegistrarAsistencia): self._cargar_asistencia()
        elif isinstance(v, VistaEntrenadorPerfil): self._cargar_perfil()

    def _cargar_inicio(self):
        v = self.ventana
        id_u = self.usuario['id_usuario']
        try:
            datos = self.modelo.clases_entrenador_tabla(id_u)
            filas = [(d.nombre_actividad, d.sala, d.horario, d.dia_semana, d.capacidad) for d in datos]
            v.cargar_tabla_proximas(filas)
            v.set_num_clases_hoy(str(self.modelo.clases_hoy_entrenador(id_u)))
            v.set_num_asistencias(str(self.modelo.total_inscritos_clases_entrenador(id_u)))
            v.set_ocupacion_media(f'{self.modelo.ocupacion_media_entrenador(id_u)}%')
            if datos:
                nombre = datos[0].nombre_actividad
                sala   = datos[0].sala
                hora   = str(datos[0].horario).split(' - ')[0]
                v.set_proxima_clase(nombre, hora, sala)
        except Exception as e:
            print('Error cargar inicio entrenador:', e)

    def _cargar_clases(self):
        v = self.ventana
        id_u = self.usuario['id_usuario']
        try:
            datos = self.modelo.clases_entrenador_tabla(id_u)
            # ClaseEntrenadorVO: nombre_actividad, sala, horario, dia_semana, capacidad
            filas = [(d.nombre_actividad, d.sala, d.horario, d.dia_semana, d.capacidad) for d in datos]
            v.cargar_tabla(filas)
            v.set_total_clases(str(len(datos)))
            v.set_clases_hoy(str(self.modelo.clases_hoy_entrenador(id_u)))
            media = self.modelo.ocupacion_media_entrenador(id_u)
            v.set_ocupacion_media(f'{float(media):.1f}%')
            if datos:
                nombre  = datos[0].nombre_actividad
                horario = datos[0].horario
                dia     = datos[0].dia_semana
                hora    = str(horario).split(' - ')[0]
                v.set_proxima_clase(nombre, f'{dia} {hora}')
        except Exception as e:
            print('Error cargar clases entrenador:', e)

    def _cargar_inscritos(self):
        v = self.ventana
        id_u = self.usuario['id_usuario']
        try:
            clases = self.modelo.clases_de_entrenador(id_u)
            v.poblar_combo_clases(clases)
            self.cargar_clientes_inscritos()
        except Exception as e:
            print('Error cargar inscritos:', e)

    def cargar_clientes_inscritos(self):
        v = self.ventana
        id_clase = v.get_id_clase_seleccionada()
        if not id_clase:
            return
        try:
            datos = self.modelo.clientes_inscritos_clase(id_clase)
            # datos[i] = (id, nombre, telefono, email, ...)
            filas = [(d.nombre, d.telefono, d.email) for d in datos]
            v.cargar_tabla_inscritos(filas)
            v.set_num_inscritos(str(len(datos)))
            info = self.modelo.informacion_clase_con_sala(id_clase)
            if info:
                v.set_info_clase(str(info.nombre_actividad), str(info.sala), str(info.dia_semana), f'{info.hora_inicio} - {info.hora_fin}')
        except Exception as e:
            print('Error cargar clientes inscritos:', e)

    def _cargar_ocupacion(self):
        v = self.ventana
        id_u = self.usuario['id_usuario']
        try:
            datos = self.modelo.ocupacion_clases_entrenador(id_u)
            # datos[i] es OcupacionClaseVO o tupla (id, nombre, inscritos, aforo, pct)
            filas = [(d.id_clase, d.nombre_actividad,
                      d.inscritos, d.aforo_maximo, d.porcentaje) for d in datos]
            v.cargar_tabla(filas)
            resumen = self.modelo.resumen_ocupacion_entrenador(id_u)
            clase_ml = resumen.get('clase_mas_llena')
            if clase_ml:
                nombre_ml = clase_ml.nombre_actividad if hasattr(clase_ml, 'nombre_actividad') else str(clase_ml)
                ins = clase_ml.inscritos if hasattr(clase_ml, 'inscritos') else 0
                afo = clase_ml.aforo_maximo if hasattr(clase_ml, 'aforo_maximo') else 0
                plazas = resumen.get('plazas_libres_mas_llena', 0)
                media  = resumen.get('ocupacion_media', 0)
                v.set_resumen(
                    resumen.get('clases_llenas', 0),
                    f'{media}%', nombre_ml,
                    f'{ins}/{afo} inscritos', plazas
                )
        except Exception as e:
            print('Error cargar ocupacion:', e)

    def _cargar_asistencia(self):
        v = self.ventana
        id_u = self.usuario['id_usuario']
        try:
            clases = self.modelo.clases_de_entrenador(id_u)
            v.poblar_combo_clases(clases)
            self.cargar_inscritos_asistencia()
        except Exception as e:
            print('Error cargar asistencia:', e)

    def cargar_inscritos_asistencia(self):
        v = self.ventana
        id_clase = v.get_id_clase_seleccionada()
        if id_clase is None:
            return
        try:
            datos = self.modelo.clientes_inscritos_clase(id_clase)
            fecha = date.today().isoformat()
            asistencias = self.modelo.asistencia_clase_fecha(id_clase, fecha)
            mapa = {a.id_cliente: a.presente for a in asistencias}
            v.cargar_tabla_asistencia(datos, mapa)

            presentes = sum(1 for a in mapa.values() if a == 'si')
            ausentes  = sum(1 for a in mapa.values() if a == 'no')
            pendientes = len(datos) - presentes - ausentes
            v.set_resumen_asistencia(len(datos), presentes, ausentes, pendientes)

            clase = self.modelo.datos_clase_asistencia(id_clase)
            if clase:
                v.set_info_clase(
                    str(clase.get('nombre', '')),
                    str(clase.get('dia', '')),
                    f"{clase.get('hora_inicio','')} - {clase.get('hora_fin','')}",
                    ''
                )
            info_sala = self.modelo.informacion_clase_con_sala(id_clase)
            if info_sala:
                v.set_info_clase(
                    str(info_sala.nombre_actividad), str(info_sala.dia_semana),
                    f'{info_sala.hora_inicio} - {info_sala.hora_fin}', str(info_sala.sala)
                )
        except Exception as e:
            print('Error cargar inscritos asistencia:', e)

    def _cargar_perfil(self):
        v = self.ventana
        id_u = self.usuario['id_usuario']
        try:
            perfil = self.modelo.perfil_usuario(id_u)
            if perfil:
                v.set_perfil_info(
                    str(perfil[2]), str(perfil[4] or ''),
                    str(perfil[3] or ''), str(perfil[7] or ''),
                    str(perfil[8] or '')
                )
            clases = self.modelo.clases_de_entrenador(id_u)
            total_clientes = sum(
                len(self.modelo.clientes_inscritos_clase(c.id_clase)) for c in clases
            )
            total_reg = total_pres = 0
            for c in clases:
                for a in self.modelo.consultar_asistencia_clase(c.id_clase):
                    total_reg += 1
                    if a.presente == 'si':
                        total_pres += 1
            pct = f'{round(total_pres*100/total_reg,2)}%' if total_reg > 0 else '0%'
            v.set_stats(len(clases), self.modelo.clases_hoy_entrenador(id_u),
                        total_clientes, pct)
        except Exception as e:
            print('Error cargar perfil entrenador:', e)

    # ── Acciones ──────────────────────────────────────────────────────────
    def guardar_asistencia(self):
        v = self.ventana
        try:
            id_clase = v.get_id_clase_seleccionada()
            if id_clase is None:
                v.mostrar_error('Selecciona una clase')
                return
            fecha = date.today().isoformat()
            filas = v.get_datos_asistencia()
            presentes = ausentes = pendientes = 0
            for texto_cliente, estado in filas:
                id_cliente = int(texto_cliente.split(' - ')[0])
                estado_norm = self.modelo.normalizar_estado_asistencia(estado)
                if estado_norm in ('si', 'no'):
                    asistencia_vo = AsistenciaVO(None, id_cliente, id_clase, fecha, estado_norm)
                    self.modelo.registrar_asistencia_normalizada(
                        asistencia_vo.id_cliente, asistencia_vo.id_clase,
                        asistencia_vo.fecha, asistencia_vo.presente
                    )
                if estado_norm == 'si':   presentes += 1
                elif estado_norm == 'no': ausentes += 1
                else:                     pendientes += 1
            v.set_resumen_asistencia(len(filas), presentes, ausentes, pendientes)
            v.mostrar_exito(f'Asistencia guardada correctamente.\nAsistieron: {presentes}')
        except Exception as e:
            v.mostrar_error(str(e))

    # ── Cerrar sesión ─────────────────────────────────────────────────────
    def cerrar_sesion(self):
        if self.ventana:
            self.ventana.close()
        self.vista_login.show()

    # ── Ayuda ─────────────────────────────────────────────────────────────
    def _añadir_boton_ayuda(self):
        BotonesView.crear_boton_ayuda(self.ventana, 955, 27, self._mostrar_ayuda)

    def _mostrar_ayuda(self):
        v = self.ventana
        if isinstance(v, VistaEntrenadorInicio):
            MensajeView.information(v, 'Ayuda — Inicio',
                'Panel de control del entrenador.\n\n'
                '• Aquí ves tus clases del día y las próximas de la semana.\n'
                '• Usa el menú lateral para gestionar tus clases y alumnos.')
        elif isinstance(v, VistaEntrenadorClases):
            MensajeView.information(v, 'Ayuda — Mis clases',
                'Lista de todas las clases que tienes asignadas.\n\n'
                '• La tabla muestra nombre, sala, horario, día y capacidad.\n'
                '• Próxima clase muestra la siguiente que debes impartir.')
        elif isinstance(v, VistaEntrenadorListaClientes):
            MensajeView.information(v, 'Ayuda — Alumnos inscritos',
                'Consulta los alumnos inscritos en cada clase.\n\n'
                '• Selecciona una clase en el desplegable para ver su lista.')
        elif isinstance(v, VistaEntrenadorOcupacion):
            MensajeView.information(v, 'Ayuda — Ocupación de clases',
                'Estadísticas de ocupación de tus clases.\n\n'
                '• Porcentaje de aforo ocupado en cada clase.')
        elif isinstance(v, VistaEntrenadorRegistrarAsistencia):
            MensajeView.information(v, 'Ayuda — Registrar asistencia',
                'Registra la asistencia de los alumnos.\n\n'
                '• Selecciona la clase en el desplegable.\n'
                '• Escribe si o no en la columna Estado.\n'
                '• Pulsa Guardar asistencia cuando termines.')
        elif isinstance(v, VistaEntrenadorPerfil):
            MensajeView.information(v, 'Ayuda — Mi perfil',
                'Información de tu cuenta de entrenador.')
        else:
            MensajeView.information(v, 'Ayuda — Información',
                'Información general del gimnasio.\n\n'
                '• Usa el menú lateral para navegar entre secciones.')