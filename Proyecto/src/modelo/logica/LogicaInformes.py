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

    def __init__(self):
        self._informe_dao = InformeDaoJDBC()
        self._informe_consultas_dao = InformeConsultasDaoJDBC()

    def generar_informe(self, id_contable, tipo):
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
    
    def num_informes_mes_contable(self):
        return self._informe_consultas_dao.num_informes_mes_contable()


    def historial_informes_contable(self):
        return self._informe_consultas_dao.historial_informes_contable()


    def contable_informes_generados_usuario(self, id_contable):
        if not id_contable:
            raise ValueError("Debe indicarse el contable")

        return self._informe_consultas_dao.contable_informes_generados_usuario(id_contable)

    def exportar_pdf(self, id_contable, tipo, cabeceras, filas):
        if not id_contable:
            raise ValueError("Debe indicarse el contable")

        if not tipo:
            raise ValueError("Debe indicarse el tipo de informe")

        if not cabeceras:
            raise ValueError("El informe no tiene cabeceras")

        if not filas:
            raise ValueError("El informe no tiene datos para exportar")

        datos_pdf = [cabeceras] + filas

        fecha_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"{tipo.replace(' ', '_')}_{fecha_str}.pdf"

        carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
        os.makedirs(carpeta_descargas, exist_ok=True)

        ruta = os.path.join(carpeta_descargas, nombre_archivo)

        doc = SimpleDocTemplate(ruta, pagesize=A4)
        estilos = getSampleStyleSheet()

        elementos = [
            Paragraph(f"StayFit — {tipo}", estilos["Title"]),
            Paragraph(
                f"Generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}",
                estilos["Normal"]
            ),
            Spacer(1, 20)
        ]

        tabla_pdf = Table(datos_pdf, repeatRows=1)

        tabla_pdf.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1D9E75")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 11),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F1FFF8")]),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#9FE1CB")),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))

        elementos.append(tabla_pdf)
        doc.build(elementos)

        self.generar_informe(id_contable, tipo)

        return ruta