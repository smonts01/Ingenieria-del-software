import os
from datetime import date

from src.vista.componentes import MensajeView, TablaView, BotonesView
from src.modelo.VO.AsistenciaVO import AsistenciaVO
from src.vista.vistas.vista_entrenador import (       #importamos todas las vistas
    VistaEntrenadorInicio,
    VistaEntrenadorClases,
    VistaEntrenadorListaClientes,
    VistaEntrenadorOcupacion,
    VistaEntrenadorRegistrarAsistencia,
    VistaEntrenadorPerfil,
    VistaEntrenadorInformacion,
)


#Instanciar Vista y asignarle set_controlador(self)
#Responder a eventos  Vista
#Llamar al Modelo para obtener/guardar datos
#Llamar a métodos de la Vista para actualizar la UI




# Diccionario que relaciona cada archivo .ui con su clase Vista.
# abrir_pantalla() usa este diccionario para saber qué clase debe instanciar.
# Si añado una nueva pantalla del entrenador tendría que añadirla aqui

_VISTAS = {
    'interfaz_entrenador.ui': VistaEntrenadorInicio,
    'interfaz_entrenador_clases.ui': VistaEntrenadorClases,
    'interfaz_entrenador_verListaClientes.ui': VistaEntrenadorListaClientes,
    'interfaz_entrenador_ocupacionClases.ui': VistaEntrenadorOcupacion,
    'interfaz_entrenador_registrar_asistencia.ui': VistaEntrenadorRegistrarAsistencia,
    'interfaz_entrenador_perfil.ui': VistaEntrenadorPerfil,
    'interfaz_entrenador_informacion.ui': VistaEntrenadorInformacion,
}


class ControladorEntrenador:

    def __init__(self, modelo, usuario, ruta_ui, vista_login):
        self.modelo = modelo #para acceder a logica y daos
        self.usuario = usuario #datos del entrenador
        self.ruta_ui = ruta_ui 
        self.vista_login = vista_login #pantalla del login para volver al cerrar sesion
        self.ventana = None #pantalla actual abierta


    #primero se abre la pantalla principal del entrenador
    def abrir(self):
        self.ir_inicio()

    #abrir pantallas concretas
    def abrir_pantalla(self, archivo):
        if self.ventana:      #si ya existía una ventana anterior la cierra
            self.ventana.close()
        
        ruta = os.path.join(self.ruta_ui, archivo) #obtengo la ruta al ui

        ClaseVista = _VISTAS[archivo]   #obtiene la  vista correspondiente buscandola en el diccionario
        self.ventana = ClaseVista(ruta) #creo esa vista concreta pasandole la ruta del ui
        self.ventana.set_controlador(self) #le paso el controlador a la vista para que pueda llamar a los metdos
        self._añadir_boton_ayuda()
        self.cargar_datos()   #cargo datos de la ventana
        self.ventana.show()    #muestro la ventana

    
    # NAVEGACIÓN ENTRE PANTALLAS (menú lateral)
    # los botones de la vista llaman a estos métodos para abrir la pantalla correspondiente
    def ir_inicio(self):
        self.abrir_pantalla('interfaz_entrenador.ui') #llamo a abrir y le paso el nombre del archivo, (en abrir se busca la ruta)

    def ir_clases(self):
        self.abrir_pantalla('interfaz_entrenador_clases.ui')

    def ir_inscritos(self):
        self.abrir_pantalla('interfaz_entrenador_verListaClientes.ui')

    def ir_ocupacion(self):
        self.abrir_pantalla('interfaz_entrenador_ocupacionClases.ui')

    def ir_asistencia(self):
        self.abrir_pantalla('interfaz_entrenador_registrar_asistencia.ui')

    def ir_perfil(self):
        self.abrir_pantalla('interfaz_entrenador_perfil.ui')

    def ir_informacion(self):
        self.abrir_pantalla('interfaz_entrenador_informacion.ui')

    # CARGAR DATOS
    # segun ventana abierta llamo a los metodos que cargan sus datos
    def cargar_datos(self):
        v = self.ventana #pantalla abierta (vista abierta)
        
        if isinstance(v, VistaEntrenadorInicio): #si es la pantanlla de inicio (instancia de la vista de inicio)
            self._cargar_inicio() #cargo el inicio

        elif isinstance(v, VistaEntrenadorClases): 
            self._cargar_clases()

        elif isinstance(v, VistaEntrenadorListaClientes): 
            self._cargar_inscritos()

        elif isinstance(v, VistaEntrenadorOcupacion): 
            self._cargar_ocupacion()

        elif isinstance(v, VistaEntrenadorRegistrarAsistencia): 
            self._cargar_asistencia()

        elif isinstance(v, VistaEntrenadorPerfil): 
            self._cargar_perfil()
    
    
    # métodos para cargar datos en cada pantalla

    def _cargar_inicio(self):
        v = self.ventana #ventana actual
        id_u = self.usuario['id_usuario'] #usuario actual

        try:
            datos = self.modelo.clases_entrenador_tabla(id_u) #EXTRAE DATOS DEL MODELO

            # Convierto los objetos en filas para mostrarlas en la tabla.
            filas = [(d.nombre_actividad, d.sala, d.horario, d.dia_semana, d.capacidad) for d in datos]
            
            #paso los datos ya preparados a la vista
            # ventana actual (vista llama a sus métodos para cargar datos)
            v.cargar_tabla_proximas(filas)
            v.set_num_clases_hoy(str(self.modelo.clases_hoy_entrenador(id_u)))
            v.set_num_asistencias(str(self.modelo.total_inscritos_clases_entrenador(id_u)))
            v.set_ocupacion_media(f'{self.modelo.ocupacion_media_entrenador(id_u)}%')
            
            # Si hay clases, muestro la primera como próxima clase
            if datos:
                nombre = datos[0].nombre_actividad
                sala = datos[0].sala
                hora = str(datos[0].horario).split(' - ')[0]
                #vista pinta la proxima clase con los datos que ha obtenido el controlador
                v.set_proxima_clase(nombre, hora, sala)

        except Exception as e:
            print('Error cargar inicio entrenador:', e)

    def _cargar_clases(self):
        v = self.ventana
        id_u = self.usuario['id_usuario']
        
        try:
            datos = self.modelo.clases_entrenador_tabla(id_u) #EXTRAE DATOS DEL MODELO
           
            # Transformo los objetos recibidos del modelo en tuplas para poder pintarlas en la tabla.
            filas = [(d.nombre_actividad, d.sala, d.horario, d.dia_semana, d.capacidad) for d in datos]

            v.cargar_tabla(filas)
            v.set_total_clases(str(len(datos))) # Total de clases asignadas al entrenador.
            v.set_clases_hoy(str(self.modelo.clases_hoy_entrenador(id_u)))
            media = self.modelo.ocupacion_media_entrenador(id_u)
            v.set_ocupacion_media(f'{float(media):.1f}%')

            if datos:
                nombre = datos[0].nombre_actividad
                horario = datos[0].horario
                dia = datos[0].dia_semana
                hora = str(horario).split(' - ')[0]
                v.set_proxima_clase(nombre, f'{dia} {hora}')

        except Exception as e:
            print('Error cargar clases entrenador:', e)


    def _cargar_inscritos(self):
        v = self.ventana
        id_u = self.usuario['id_usuario']

        try:
            clases = self.modelo.clases_de_entrenador(id_u) #EXTRAE DATOS DEL MODELO (clases del entrenador)
            v.poblar_combo_clases(clases) #se las pasa al combo de laa vista para que las pinte
            self.cargar_clientes_inscritos() #carga datos en la tabla
        
        except Exception as e:
            print('Error cargar inscritos:', e)

    def cargar_clientes_inscritos(self):
        v = self.ventana
        id_clase = v.get_id_clase_seleccionada() # Lee de la vista qué clase está seleccionada en el combo.
        if not id_clase: # Si no hay clase seleccionada, no se puede cargar ningún alumno.
            return
        
        try:
            datos = self.modelo.clientes_inscritos_clase(id_clase) #EXTRAE DATOS DEL MODELO

            v.cargar_tabla_inscritos(datos) #pasa los datos a la vista
            v.set_num_inscritos(str(len(datos)))

            info = self.modelo.informacion_clase_con_sala(id_clase) #EXTRAE DATOS DEL MODELO
            #se los pasa a la vista
            if info:
                v.set_info_clase(str(info.nombre_actividad), str(info.sala), str(info.dia_semana), f'{info.hora_inicio} - {info.hora_fin}')
        
        except Exception as e:
            print('Error cargar clientes inscritos:', e)

    def _cargar_ocupacion(self):
        v = self.ventana
        id_u = self.usuario['id_usuario']

        try:
            datos = self.modelo.ocupacion_clases_entrenador(id_u) #EXTRAE DATOS OCUPACIÓN DEL MODELO
           
            filas = [(d.id_clase, d.nombre_actividad, d.inscritos, d.aforo_maximo, d.porcentaje) for d in datos]

            v.cargar_tabla(filas) #le pasa los datos a la vista

            resumen = self.modelo.resumen_ocupacion_entrenador(id_u) #EXTRAE DATOS DEL RESUEMN OCUPACION DEL MODELO
            clase_ml = resumen.get('clase_mas_llena') #toma la clase mas llena
            
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
            # Obtengo las clases del entrenador para rellenar el desplegable.
            clases = self.modelo.clases_de_entrenador(id_u)

            # Relleno el combo de clases en la vista.
            v.poblar_combo_clases(clases)

            # Cargo la asistencia de la clase seleccionada por defecto.
            self.cargar_inscritos_asistencia()

        except Exception as e:
            print('Error cargar asistencia:', e)

    
    
    def cargar_inscritos_asistencia(self):
        v = self.ventana
        id_clase = v.get_id_clase_seleccionada()
        if id_clase is None:
            return
        try:
            fecha = date.today().isoformat()
            resumen = self.modelo.resumen_asistencia_clase(id_clase, fecha)  # Obtiene alumnos y estado de asistencia de hoy.
            
            v.cargar_tabla_asistencia(resumen['datos'], resumen['mapa']) # vista pinta la tabla con los alumnos y sus estados.
            # Actualiza los contadores de asistencia
            v.set_resumen_asistencia(resumen['total'], resumen['presentes'], resumen['ausentes'], resumen['pendientes'])

            clase = self.modelo.datos_clase_asistencia(id_clase) #obtengo datos de asistencia
            if clase: # Después cargo la información completa con sala
                v.set_info_clase(str(clase.get('nombre', '')), str(clase.get('dia', '')), f"{clase.get('hora_inicio','')} - {clase.get('hora_fin','')}",'')

            info_sala = self.modelo.informacion_clase_con_sala(id_clase) #obtengo datos de clases 
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
            perfil = self.modelo.perfil_usuario(id_u) # Obtiene los datos personales del usuario entrenador (devuelve tupla)
            if perfil:
                # Pasa a la vista los campos del perfil.
                v.set_perfil_info(
                    str(perfil[2]), str(perfil[4] or ''),
                    str(perfil[3] or ''), str(perfil[7] or ''),
                    str(perfil[8] or '')
                )

            clases = self.modelo.clases_de_entrenador(id_u) #obtengo clases del entrenador
            stats = self.modelo.estadisticas_perfil_entrenador(id_u) #obtengo estadisticas del entrenador

            #desde vista cargo su informacion en el perfil 
            v.set_stats(len(clases), self.modelo.clases_hoy_entrenador(id_u), stats['total_clientes'], stats['pct_asistencia'])
        
        except Exception as e:
            print('Error cargar perfil entrenador:', e)

    
    
    # ACCIONES
    def guardar_asistencia(self):
        v = self.ventana
        try:
            id_clase = v.get_id_clase_seleccionada()
            if id_clase is None:
                v.mostrar_error('Selecciona una clase')
                return
            fecha = date.today().isoformat()
            filas = v.get_datos_asistencia()
            presentes = 0
            ausentes = 0
            pendientes = 0

            for texto_cliente, estado in filas:
                id_cliente = int(texto_cliente.split(' - ')[0])
                estado_norm = self.modelo.normalizar_estado_asistencia(estado) #LLAMA modelo TOMA DATOS escritos DE LA TABLA

                #si hay un si o no
                if estado_norm in ('si', 'no'):

                    asistencia_vo = AsistenciaVO(None, id_cliente, id_clase, fecha, estado_norm) #CREA UN VO DONDE GUARDA LA ASISTENCIA
                    
                    self.modelo.registrar_asistencia_normalizada(        # se llama al modelo para GUARDAR DE VUELTA LA ASISTENCIA
                        asistencia_vo.id_cliente, asistencia_vo.id_clase,
                        asistencia_vo.fecha, asistencia_vo.presente
                    )

                #sumo asistencias y ausencias para refrescar el resumen de la pantalla.
                if estado_norm == 'si':   
                    presentes += 1
                elif estado_norm == 'no': 
                    ausentes += 1
                else: 
                    pendientes += 1

            v.set_resumen_asistencia(len(filas), presentes, ausentes, pendientes) # se las paso a la vista 

            v.mostrar_exito(f'Asistencia guardada correctamente.\nAsistieron: {presentes}')
        except Exception as e:
            v.mostrar_error(str(e))


    # CERRAR SESIÓN

    def cerrar_sesion(self):
        if self.ventana: #cierro la vista , la interfaz
            self.ventana.close()
        self.vista_login.show() #muestro el login

    

    
    # BOTÓN ADICIONAL DE AYUDA 
    def _añadir_boton_ayuda(self):
        BotonesView.crear_boton_ayuda(self.ventana, 955, 27, self._mostrar_ayuda)

    # Muestra un mensaje de ayuda distinto según la pantalla abierta.
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