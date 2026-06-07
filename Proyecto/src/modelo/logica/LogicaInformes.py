import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from src.modelo.dao.InformeDaoJDBC import InformeDaoJDBC
from src.modelo.VO.InformeVO import InformeVO
from src.modelo.dao.InformeConsultasDaoJDBC import InformeConsultasDaoJDBC


class LogicaInformes:
    """Lógica de negocio para la generación y exportación de informes económicos.
    Gestiona el registro de informes en la base de datos y la exportación
    de su contenido a PDF usando ReportLab. Los PDF se guardan en la carpeta
    de descargas del usuario con el nombre: <tipo>_<fecha_hora>.pdf
    """

    def __init__(self):
        self._informe_dao          = InformeDaoJDBC()
        self._informe_consultas_dao = InformeConsultasDaoJDBC()

    # Generar informes

    def generar_informe(self, id_contable, tipo):
        """Registra un nuevo informe en la base de datos.

        Crea un InformeVO con la fecha y hora actuales y lo inserta.
        Lanza ValueError si falta el contable o el tipo de informe.
        Devuelve el número de filas afectadas.
        """
        if not id_contable:
            raise ValueError("Debe indicarse el contable")
        if not tipo:
            raise ValueError("Debe indicarse el tipo de informe")

        informe = InformeVO(
            id_informe=None,
            id_contable=id_contable,
            tipo_informe=tipo,
            fecha_generacion=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        return self._informe_dao.insert(informe)

    # Consultas sobre informes

    def num_informes_mes_contable(self):
        """Devuelve el número de informes generados en el mes actual."""
        return self._informe_consultas_dao.num_informes_mes_contable()

    def historial_informes_contable(self):
        """Devuelve el historial completo de informes como lista de HistorialInformeVO."""
        return self._informe_consultas_dao.historial_informes_contable()

    def contable_informes_generados_usuario(self, id_contable):
        """Devuelve el número de informes generados por un contable concreto.
        Lanza ValueError si no se indica el contable."""
        if not id_contable:
            raise ValueError("Debe indicarse el contable")
        return self._informe_consultas_dao.contable_informes_generados_usuario(id_contable)

    # Exportar a PDF

    def exportar_pdf(self, id_contable, tipo, cabeceras, filas):
        """Exporta un informe a PDF y lo guarda en la carpeta de descargas del usuario.

        Pasos:
        1. Valida los parámetros de entrada.
        2. Construye el nombre del archivo con el tipo y la fecha actual.
        3. Genera el PDF con ReportLab (título, fecha de generación y tabla de datos).
        4. Registra el informe en la base de datos.


        Devuelve la ruta completa del archivo PDF generado.
        Lanza ValueError si faltan parámetros o si el informe no tiene datos.
        """
        # Validar parámetros
        if not id_contable:
            raise ValueError("Debe indicarse el contable")
        if not tipo:
            raise ValueError("Debe indicarse el tipo de informe")
        if not cabeceras:
            raise ValueError("El informe no tiene cabeceras")
        if not filas:
            raise ValueError("El informe no tiene datos para exportar")

        # Combinar cabeceras y filas para la tabla del PDF
        datos_pdf = [cabeceras] + filas

        # Construir la ruta de destino en la carpeta de descargas
        fecha_str      = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"{tipo.replace(' ', '_')}_{fecha_str}.pdf"
        carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
        os.makedirs(carpeta_descargas, exist_ok=True)
        ruta = os.path.join(carpeta_descargas, nombre_archivo)

        # Crear el documento PDF
        doc     = SimpleDocTemplate(ruta, pagesize=A4)
        estilos = getSampleStyleSheet()

        # Cabecera del documento: título y fecha de generación
        elementos = [
            Paragraph(f"StayFit — {tipo}", estilos["Title"]),
            Paragraph(
                f"Generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}",
                estilos["Normal"]
            ),
            Spacer(1, 20),
        ]

        # Tabla de datos con estilo corporativo
        tabla_pdf = Table(datos_pdf, repeatRows=1)
        tabla_pdf.setStyle(TableStyle([
            # Cabecera: fondo verde, texto blanco y negrita
            ("BACKGROUND", (0, 0), (-1, 0),  colors.HexColor("#1D9E75")),
            ("TEXTCOLOR",  (0, 0), (-1, 0),  colors.white),
            ("FONTNAME",   (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("FONTSIZE",   (0, 0), (-1, 0),  11),
            # Filas de datos: fondo alterno blanco y verde claro
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F1FFF8")]),
            ("FONTSIZE",   (0, 1), (-1, -1),  9),
            # Bordes y alineación
            ("GRID",       (0, 0), (-1, -1),  0.5, colors.HexColor("#9FE1CB")),
            ("ALIGN",      (0, 0), (-1, -1),  "CENTER"),
            ("VALIGN",     (0, 0), (-1, -1),  "MIDDLE"),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        elementos.append(tabla_pdf)

        # Generar el archivo PDF
        doc.build(elementos)

        # Registrar el informe en la base de datos
        self.generar_informe(id_contable, tipo)

        return ruta