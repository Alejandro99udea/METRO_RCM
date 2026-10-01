# -*- coding: utf-8 -*-

from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


# ============================================================
# COLORES METRO_RCM
# ============================================================

VERDE = colors.HexColor("#006B54")
VERDE_OSCURO = colors.HexColor("#004F3D")
VERDE_CLARO = colors.HexColor("#E8F3EF")
AMARILLO = colors.HexColor("#F2C94C")
GRIS = colors.HexColor("#64748B")
GRIS_CLARO = colors.HexColor("#F4F6F5")


# ============================================================
# GENERAR PDF
# ============================================================

def generar_informe_pdf(
    titulo,
    subtitulo,
    secciones,
):
    """
    Genera un PDF dinámico a partir de la información actual.

    Parámetros
    ----------
    titulo : str
        Título principal del informe.

    subtitulo : str
        Descripción del módulo.

    secciones : list
        Lista de diccionarios con la estructura:

        [
            {
                "titulo": "Sección",
                "datos": [
                    ["Campo", "Valor"],
                    ["Campo", "Valor"],
                ]
            }
        ]

    Retorna
    -------
    bytes
        PDF generado en memoria.
    """

    buffer = BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.6 * cm,
        leftMargin=1.6 * cm,
        topMargin=1.7 * cm,
        bottomMargin=1.7 * cm,
        title=titulo,
        author="METRO_RCM",
    )

    estilos = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        "TituloMetro",
        parent=estilos["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        textColor=VERDE_OSCURO,
        alignment=TA_CENTER,
        spaceAfter=8,
    )

    estilo_subtitulo = ParagraphStyle(
        "SubtituloMetro",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=GRIS,
        alignment=TA_CENTER,
        spaceAfter=18,
    )

    estilo_seccion = ParagraphStyle(
        "SeccionMetro",
        parent=estilos["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=17,
        textColor=VERDE,
        spaceBefore=12,
        spaceAfter=8,
    )

    estilo_normal = ParagraphStyle(
        "NormalMetro",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#263238"),
    )

    contenido = []

    # --------------------------------------------------------
    # ENCABEZADO
    # --------------------------------------------------------

    contenido.append(
        Paragraph(
            "METRO_RCM",
            estilo_titulo,
        )
    )

    contenido.append(
        Paragraph(
            titulo,
            estilo_titulo,
        )
    )

    contenido.append(
        Paragraph(
            subtitulo,
            estilo_subtitulo,
        )
    )

    fecha = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )

    contenido.append(
        Paragraph(
            f"Informe generado en tiempo real: {fecha}",
            estilo_subtitulo,
        )
    )

    contenido.append(Spacer(1, 0.25 * cm))


    # --------------------------------------------------------
    # SECCIONES
    # --------------------------------------------------------

    for seccion in secciones:

        titulo_seccion = seccion.get(
            "titulo",
            "Sección"
        )

        datos = seccion.get(
            "datos",
            []
        )

        contenido.append(
            Paragraph(
                titulo_seccion,
                estilo_seccion,
            )
        )

        tabla_datos = []

        for fila in datos:

            if len(fila) < 2:
                continue

            campo = str(fila[0])
            valor = str(fila[1])

            tabla_datos.append(
                [
                    Paragraph(
                        campo,
                        estilo_normal
                    ),
                    Paragraph(
                        valor,
                        estilo_normal
                    ),
                ]
            )

        if tabla_datos:

            tabla = Table(
                tabla_datos,
                colWidths=[
                    6.0 * cm,
                    10.5 * cm,
                ],
                repeatRows=0,
            )

            tabla.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (0, -1),
                            VERDE_CLARO,
                        ),
                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.4,
                            colors.HexColor("#DCE3E0"),
                        ),
                        (
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "TOP",
                        ),
                        (
                            "LEFTPADDING",
                            (0, 0),
                            (-1, -1),
                            7,
                        ),
                        (
                            "RIGHTPADDING",
                            (0, 0),
                            (-1, -1),
                            7,
                        ),
                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, -1),
                            6,
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            6,
                        ),
                    ]
                )
            )

            contenido.append(tabla)

            contenido.append(
                Spacer(
                    1,
                    0.35 * cm
                )
            )


    # --------------------------------------------------------
    # PIE
    # --------------------------------------------------------

    contenido.append(
        Spacer(
            1,
            0.8 * cm
        )
    )

    contenido.append(
        Paragraph(
            "METRO_RCM · Gestión de Activos y RCM · Universidad de Antioquia",
            estilo_subtitulo,
        )
    )

    documento.build(
        contenido
    )

    buffer.seek(0)

    return buffer.getvalue()