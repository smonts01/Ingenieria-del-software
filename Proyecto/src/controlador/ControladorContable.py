import os
import ctypes.wintypes

from src.vista.componentes import MensajeView, BotonesView, ArchivoView
from src.modelo.VO.RegistroPagoVO import RegistroPagoVO
from src.vista.vistas.vista_contable import (
    VistaContableInicio,
    VistaContableRegistrarPago,
    VistaContablePagosPendientes,
    VistaContableGestionEconomica,
    VistaContableInformes,
    VistaContablePerfil,
    VistaContableInfo,
    VistaContableInformeGestionEconomica,
    VistaContableInformeDePagos,
    VistaContableInformePagosPendientes,
    VistaContableInformeBalanceMensual,
)



# Relaciona cada archivo .ui del contable con su clase Vista correspondiente.
# abrir_pantalla() usa este diccionario para saber qué vista debe crear.
# Si añado una pantalla nueva del contable, tendría que añadirla aquí.
_VISTAS = {
    'interfaz_contable.ui': VistaContableInicio,
    'interfaz_contable_registrar_pago.ui':  VistaContableRegistrarPago,
    'interfaz_contable_pagos_pendientes.ui': VistaContablePagosPendientes,
    'interfaz_contable_gestion_economica.ui': VistaContableGestionEconomica,
    'interfaz_contable_informes.ui': VistaContableInformes,
    'interfaz_contable_perfil.ui': VistaContablePerfil,
    'interfaz_contable_info.ui': VistaContableInfo,
    'interfaz_contable_informes_gestion_economica.ui':  VistaContableInformeGestionEconomica,
    'interfaz_contable_informes_de_pagos.ui': VistaContableInformeDePagos,
    'interfaz_contable_informes_pagos_pendientes.ui': VistaContableInformePagosPendientes,
    'interfaz_contable_informes_balance_mensual.ui': VistaContableInformeBalanceMensual,
}


class ControladorContable:

    def __init__(self, modelo, usuario, ruta_ui, vista_login):
        
        self.modelo = modelo  # Modelo principal. Desde aquí se accede a la lógica y a la base de datos
        self.usuario = usuario # Datos del usuario que ha iniciado sesión como contable
        self.ruta_ui = ruta_ui
        self.vista_login = vista_login # Referencia a la pantalla de login para volver al cerrar sesión.
        self.ventana = None      # Ventana actual abierta del contable. Al principio no hay ninguna.
        self._tipo_informe_actual = 'informe'  # Guarda qué tipo de informe se está viendo actualmente.
        self.id_pago_seleccionado = None   # Guarda el pago seleccionado en la pantalla de registrar pago
        self.id_cliente_seleccionado = None  # Guarda el cliente asociado al pago seleccionado

    # Abre la pantalla principal del contable.
    def abrir(self):
        self.ir_inicio()

    # Abre una pantalla concreta del contable
    def abrir_pantalla(self, archivo):
        if self.ventana:
            self.ventana.close() # Cierra la ventana anterior si ya había una abierta


        ruta = os.path.join(self.ruta_ui, archivo) # Construye la ruta completa del .ui

        ClaseVista = _VISTAS[archivo] # Busca la clase Vista asociada al archivo .ui

        self.ventana = ClaseVista(ruta) # Crea la ventana concreta
        self.ventana.set_controlador(self)   # Pasa el controlador a la vista para conectar botones

        self._añadir_boton_ayuda()
        self.cargar_datos() # Carga los datos iniciales de esa pantalla
        self.ventana.show() #muetsro la pantalla

    
    # NAVEGACIÓN entre pantallas
    # Métodos de navegación del menú lateral.
    # Cada botón de la vista llama a uno de estos métodos
    # Todos abren una pantalla usando abrir_pantalla()
    def ir_inicio(self):             
        self.abrir_pantalla('interfaz_contable.ui')
    
    def ir_registrar_pago(self):      
        self.abrir_pantalla('interfaz_contable_registrar_pago.ui')
    
    def ir_pagos_pendientes(self):    
        self.abrir_pantalla('interfaz_contable_pagos_pendientes.ui')
    
    def ir_gestion_economica(self):   
        self.abrir_pantalla('interfaz_contable_gestion_economica.ui')
    
    def ir_informes(self):            
        self.abrir_pantalla('interfaz_contable_informes.ui')
    
    def ir_perfil(self):              
        self.abrir_pantalla('interfaz_contable_perfil.ui')
    
    def ir_informacion(self):        
        self.abrir_pantalla('interfaz_contable_info.ui')

    def generar_y_abrir_informe(self, tipo, archivo):
        self._tipo_informe_actual = tipo
        self.abrir_pantalla(archivo)

    
    # CARGAR DATOS
    #decide que datos cargar segun la ventana abierta
    def cargar_datos(self):
        v = self.ventana #ventana abierta actual
        
        if isinstance(v, VistaContableInicio):              
            self._cargar_inicio()
        
        elif isinstance(v, VistaContableRegistrarPago):     
            self._cargar_registrar_pago()
        
        elif isinstance(v, VistaContablePagosPendientes):   
            self._cargar_pagos_pendientes()
        
        elif isinstance(v, VistaContableGestionEconomica):  
            self._cargar_gestion_economica()
        
        elif isinstance(v, VistaContableInformes):          
            self._cargar_informes()
        
        elif isinstance(v, VistaContablePerfil):            
            self._cargar_perfil()
        
        
        elif isinstance(v, VistaContableInformeGestionEconomica):
            try: 
                v.cargar_tabla(self.modelo.informe_gestion_economica_contable())
            except Exception as e:
                print('Error informe gestion eco:', e)
        
        
        elif isinstance(v, VistaContableInformeDePagos):
            try: 
                v.cargar_tabla(self.modelo.informe_pagos_realizados())
            except Exception as e: 
                print('Error informe pagos:', e)
        
        
        elif isinstance(v, VistaContableInformePagosPendientes):
            try: 
                v.cargar_tabla(self.modelo.pagos_pendientes())
            except Exception as e: 
                print('Error informe pendientes:', e)

        elif isinstance(v, VistaContableInformeBalanceMensual):
            try: 
                v.cargar_tabla(self.modelo.informe_balance_mensual_contable())
            except Exception as e: 
                print('Error informe balance:', e)


    # Carga la pantalla del inicio del contable
    def _cargar_inicio(self):
        v = self.ventana #vista actual

        # Cada try pide un dato al modelo y lo manda a la vista.
        try: 
            v.set_num_pagos_pendientes(str(self.modelo.num_pagos_pendientes_contable()))
        except: 
            v.set_num_pagos_pendientes('0')
        
        try: 
            v.set_ingresos_mes(f'{float(self.modelo.ingresos_mes_contable()):.2f} €')
        except: 
            v.set_ingresos_mes('0.00 €')
        
        try: 
            v.set_num_tarifas(str(self.modelo.num_tarifas_activas_contable()))
        except: 
            v.set_num_tarifas('0')

        try: 
            v.set_num_informes(str(self.modelo.num_informes_mes_contable()))
        except: 
            pass

        try: 
            v.cargar_tabla_ultimos_pagos(self.modelo.ultimos_pagos_inicio_contable())
        except Exception as e: 
            print('Error tabla ultimos pagos:', e)

        try: 
            v.cargar_tabla_pagos_pendientes(self.modelo.pagos_pendientes_inicio_contable())
        except Exception as e: 
            print('Error tabla pagos pendientes inicio:', e)

    
    # Carga la pantalla para registrar pagos.
    # Muestra contadores y, si existe, carga el primer pago pendiente
    def _cargar_registrar_pago(self):
        v = self.ventana
        try: 
            v.set_num_pendientes(str(self.modelo.num_pagos_pendientes_contable())) 
        except: 
            pass
        
        try: 
            v.set_cobros_hoy(str(self.modelo.cobros_hoy_contable()))
        except: 
            pass
        
        try: 
            v.set_num_informes(str(self.modelo.num_informes_mes_contable()))
        except: 
            pass
        
        try:
            # Pido al modelo el primer pago pendiente para mostrarlo 
            pago = self.modelo.primer_pago_pendiente() 

            #si hay pago pendiente
            if pago:
                self._mostrar_pago_en_vista(pago)
            else:
                v.set_sin_pago()
        except Exception as e: 
            print('Error primer pago:', e)

    def _cargar_pagos_pendientes(self):
        
        v = self.ventana

        #se obtienen todos los datos de pagos pendientes del modelo y se le pasan a la vista a set resumen
        try:
            v.set_resumen(
                self.modelo.contable_clientes_con_deuda(),
                self.modelo.contable_importe_pendiente(),
                self.modelo.contable_pagos_vencidos(),
                self.modelo.contable_pagos_vencen_semana(),
                self.modelo.num_pagos_pendientes_contable()
            )
        except Exception as e: 
            print('Error resumen pagos pend:', e)
        
        # Carga la tabla inferior teniendo en cuenta el filtro del desplegable
        self.cargar_pagos_pendientes_filtrados()

   

    # Carga la tabla de pagos pendientes aplicando el filtro elegido en la vista.
    # El *args está porque PyQt puede llamar a este método pasando argumentos
    # cuando cambia un combo, aunque aquí no los usemos

    def cargar_pagos_pendientes_filtrados(self, *args):
        v = self.ventana

        try:
            filtro = v.get_filtro() #leo el FILTRO SELECCIONADO EN LA VISTA

            datos = self.modelo.pagos_pendientes() #obtengo todos los pagos pendientes del modelo

            if filtro == 'vencido': #SI EL FILTRO MARCA VENCIDO
                datos_filtrados = []

                for fila in datos:
                    fecha_pago = fila.fecha if hasattr(fila, "fecha") else fila[4]

                    # El modelo decide si la fecha está vencida
                    if self.modelo.es_pago_vencido(fecha_pago):
                        datos_filtrados.append(fila)

            else: # Si el filtro no es vencido, se muestran todos los pagos pendientes
                datos_filtrados = datos

            # Envío los datos filtrados a la vista para pintar la tabla
            v.cargar_tabla(datos_filtrados)

        except Exception as e:
            print('Error filtrar pagos pendientes:', e)



    # Carga la pantalla de gestión económica
    def _cargar_gestion_economica(self):
        v = self.ventana
        try:
            # Obtengo las tarifas del modelo y actualizo los labels de la vista.
            tarifas = self.modelo.contable_tarifas_economica()

            for t in tarifas:
                v.set_tarifa(str(t[0]).lower(), str(t[1]), str(t[2]))
        except Exception as e: 
            print('Error tarifas:', e)
        
        try: 
            # Cargo la tabla de salarios del personal
            v.cargar_tabla_salarios(self.modelo.contable_salarios_personal())
        except Exception as e: 
            print('Error salarios:', e)
        
        try: 
            v.set_num_tarifas(str(self.modelo.num_tarifas_activas_contable()))
        except: 
            pass
        
        try: 
            v.set_nominas(f'{float(self.modelo.contable_total_nominas()):.2f} €')
        except: 
            pass
        
        try: 
            v.set_pagos_pendientes(f'{float(self.modelo.contable_importe_pendiente()):.2f} €')
        except: 
            pass
        
        try:
            # El modelo devuelve ingresos, gastos y balance económico
            ingresos, gastos, balance = self.modelo.contable_balance_economico()
            v.set_balance(f'{float(ingresos):.2f} €',
                          f'{float(gastos):.2f} €',
                          f'{float(balance):.2f} €')
        except Exception as e: 
            print('Error balance eco:', e)

   
   
   # Carga la pantalla principal de informes
    def _cargar_informes(self):
        v = self.ventana
        try: 
            v.set_num_informes(str(self.modelo.num_informes_mes_contable()))
        except: 
            pass
        
        try: 
            v.set_ingresos_mes(f'{float(self.modelo.ingresos_mes_contable()):.2f} €')
        except: 
            pass
        
        try: 
            v.set_gastos_mes(f'{float(self.modelo.contable_gastos_mes()):.2f} €')
        except: 
            pass
        
        try: 
            v.set_balance_mes(f'{float(self.modelo.contable_balance_mes()):.2f} €')
        except: 
            pass
        
        try: 
            # Cargo la tabla con el historial de informes.
            v.cargar_tabla_historial(self.modelo.historial_informes_contable())
        except Exception as e: 
            print('Error historial informes:', e)


    # Carga el perfil del contable.
    # Muestra sus datos personales y estadísticas de trabajo.
    def _cargar_perfil(self):
        v = self.ventana
        try:
            #pido al modelo los datos del usuario
            perfil = self.modelo.perfil_usuario(self.usuario['id_usuario'])
            if perfil:
                fecha_alta = f'Miembro desde: {perfil[8]}' if perfil[8] else 'Miembro desde: -'
                v.set_perfil(str(perfil[2]), str(perfil[6]).capitalize(),
                             str(perfil[4]), str(perfil[3]),
                             str(perfil[7]), fecha_alta)
            
            # Cargo estadísticas del contable:
            # pagos registrados, pendientes revisados, informes generados e importe gestionado.
            v.set_stats(
                self.modelo.contable_pagos_registrados(self.usuario['id_usuario']),
                self.modelo.contable_pendientes_revisados(),
                self.modelo.contable_informes_generados_usuario(self.usuario['id_usuario']),
                self.modelo.contable_importe_gestionado(self.usuario['id_usuario'])
            )
        except Exception as e: print('Error perfil:', e)

    # ACCIONES 

    # Busca un pago pendiente usando el DNI escrito en la pantalla de registrar pago.
    def buscar_cliente_registrar_pago(self):
        v = self.ventana
        
        dni = v.get_dni() #leo el dni que ha escrito el usuario
        if not dni:
            return
        try:
            #pido al modelo el pago pendiente asociado con ese dni 
            pago = self.modelo.buscar_pago_pendiente_por_dni(dni)
            
            if pago:
                self._mostrar_pago_en_vista(pago) #si existe lo muestro
            else:
                v.set_sin_pago(dni)
        except Exception as e:
            v.mostrar_error(str(e))


    # Recibe un pago devuelto por el modelo y lo muestra en la pantalla.
    # También guarda el id del pago y del cliente seleccionados.
    def _mostrar_pago_en_vista(self, pago):

        #separo los datos del pago
        id_pago, id_cliente, nombre, dni_real, id_tarifa, tarifa, importe, fecha_pago = pago[:8]

        #guardo el pago seleccionado
        self.id_pago_seleccionado = id_pago
        self.id_cliente_seleccionado = id_cliente #guardo el cliente seleccionado


        #paso datos a la vista para que los pinte
        self.ventana.set_cliente(nombre, dni_real, id_cliente, 'pendiente', tarifa, importe, fecha_pago)



    # Registra un pago realizado por un cliente.
    # Lee datos de la vista, crea un RegistroPagoVO y llama al modelo para guardar.
    def registrar_pago(self):
        v = self.ventana

        try:
            dni = v.get_dni() # DNI introducido por el contable.
            
            if not dni:
                v.mostrar_error('Introduce el DNI del cliente.')
                return
            

            metodo_pago = v.get_metodo_pago() #método de pago selccionado se lo pide a la vista

            try:
                metodo_pago = self.modelo.normalizar_metodo_pago(metodo_pago) #normalizo para que sea válido para la BD y se l paos al modelo
            except ValueError as e:
                v.mostrar_error(str(e))
                return
            
            fecha_texto = v.get_fecha_texto() #fecha escrita en la vista

            # Si hay fecha escrita, uso esa. Si no, uso la fecha actual del modelo.
            fecha_pago = (fecha_texto + ' 00:00:00') if fecha_texto else self.modelo.fecha_pago_actual()

            # Creo un VO para transportar los datos del pago.
            pago_vo = RegistroPagoVO(dni, self.usuario['id_usuario'], metodo_pago, fecha_pago)

            #el modelo registra el pago en la base de datos
            correcto, mensaje = self.modelo.registrar_pago_contable(
                pago_vo.dni_cliente, pago_vo.id_contable,
                pago_vo.metodo_pago, pago_vo.fecha_pago
            )
            
            
            if correcto: #si se guarda correctamente actualizo la pantalla
                v.mostrar_exito(mensaje)
                v.limpiar_dni()
                v.set_estado_abonado()
                self.cargar_datos()
            else:
                v.mostrar_error(mensaje)
        except Exception as e:
            v.mostrar_error(str(e))

    
    #marca como abonado un pago seleccionado en la vista
    def marcar_abonado(self):
        v = self.ventana
        
        try:
            id_pago = v.get_id_pago_seleccionado() #leo el pago seleccionado

            if id_pago is None:
                v.mostrar_error('Selecciona un pago primero')
                return
            
            #el modelo actualiza el estado del pago en la BD
            self.modelo.marcar_pago_abonado(id_pago)
            
            v.mostrar_exito('Pago marcado como abonado')
            self.cargar_datos() #recargo la pantalla para ver los cambios

        except Exception as e:
            v.mostrar_error(str(e))

    #genera un informe general para el contable actual
    def generar_informe(self):
        v = self.ventana

        try:
            self.modelo.generar_informe(self.usuario['id_usuario'], 'general')

            v.mostrar_exito('Informe generado correctamente')

            #recargo los datos para que aparezca el nuevo informe
            if isinstance(v, VistaContableInformes):
                self._cargar_informes()
            else:
                self.cargar_datos()

        except Exception as e:
            v.mostrar_error(str(e))

    
    # Exporta a PDF el informe que se está viendo actualmente.
    # La vista aporta las cabeceras y filas, y el modelo genera el archivo.
    def exportar_pdf(self):
        v = self.ventana

        try:
            tipo = self._tipo_informe_actual #tipo de informe actual

            #obtengo de la vista los datos de la tabla del informe
            cabeceras, filas = v.obtener_datos_tabla_informe()

            #el modelo genera el pdf y devuelve la ruta donde se ha guardado
            ruta = self.modelo.exportar_pdf_informe(
                self.usuario['id_usuario'],
                tipo,
                cabeceras,
                filas
            )

            self.cargar_datos()

            v.mostrar_exito(f'Guardado en:\n{ruta}')

        except Exception as e:
            v.mostrar_error(str(e))

    

    # CERRAR SESIÓN

    def cerrar_sesion(self):
        if self.ventana:
            self.ventana.close()
        self.vista_login.show()




    # botón de Ayuda 
    def _añadir_boton_ayuda(self):
        BotonesView.crear_boton_ayuda(self.ventana, 1015, 30, self._mostrar_ayuda)

    def _mostrar_ayuda(self):
        v = self.ventana
        if isinstance(v, VistaContableInicio):
            MensajeView.information(v, 'Ayuda — Inicio',
                'Panel de control del contable.\n\n'
                '• Resumen económico: ingresos, pagos pendientes e informes.\n'
                '• Las tablas muestran últimos pagos y pendientes.')
        elif isinstance(v, VistaContableRegistrarPago):
            MensajeView.information(v, 'Ayuda — Registrar pago',
                'Registra el pago de un cliente.\n\n'
                '• Busca al cliente por DNI y pulsa Enter.\n'
                '• Selecciona el método de pago.\n'
                '• Pulsa Registrar Pago para registrar el pago.')
        elif isinstance(v, VistaContablePagosPendientes):
            MensajeView.information(v, 'Ayuda — Pagos pendientes',
                'Clientes con pagos pendientes.\n\n'
                '• Filtra por estado con el desplegable.\n')
        elif isinstance(v, VistaContableGestionEconomica):
            MensajeView.information(v, 'Ayuda — Gestión económica',
                'Situación económica del gimnasio.\n\n'
                '• Tarifas activas, nóminas y balance del mes.')
        elif isinstance(v, VistaContableInformes):
            MensajeView.information(v, 'Ayuda — Informes',
                'Generación de informes económicos.\n\n'
                '• Selecciona el tipo de informe y pulsa el botón.\n'
                '• Usa Exportar infome a PDF para guardar el informe.')
        elif isinstance(v, VistaContablePerfil):
            MensajeView.information(v, 'Ayuda — Mi perfil',
                'Información de tu cuenta de contable.')
        else:
            MensajeView.information(v, 'Ayuda',
                'Usa el menú lateral para navegar entre secciones.')