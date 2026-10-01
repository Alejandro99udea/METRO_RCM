# -*- coding: utf-8 -*-

# ============================================================
# METRO DE MEDELLÍN - BASE DE DATOS DEL PROYECTO RCM
# ============================================================

METRO = {
    'empresa': 'Empresa de Transporte Masivo del Valle de Aburrá Ltda.',
    'empleados_pdf': 2277,
    'empleados_2025': 2066,
    'mantenimiento_pct_planta': 35,
    'mantenimiento_personas_aprox_pdf': '790–800',

    'red_integrada_km': 85.12,
    'red_ferrea_km': 31.3,
    'estaciones_ferreas': 27,
    'trenes': 80,
    'coches_tren': 240,
    'metrocables': 6,
    'tranvia': 1,
    'brt': 3,

    'socios': {
        'Distrito de Medellín': 50,
        'Departamento de Antioquia': 50
    },

    'viajes_corporativos_2025_m': 310.2,
    'satisfaccion': 4.50,
    'experiencia': 4.53,
    'meta_satisfaccion': 4.40,

    'ingresos_2025_m': 939141,
    'ingresos_transporte_2025_m': 858886,
    'negocios_asociados_2025_m': 80255,
    'ebitda_2025_m': 224768,
    'utilidad_neta_2025_m': 98430,

    'activos_2025_m': 7639583,
    'ppe_neta_2025_m': 5032626,
    'pasivos_2025_m': 9041731,
    'patrimonio_2025_m': -1402148,

    'ppye_adquisiciones_2025_m': 421440,
    'mantenimiento_plan_2025_m_mas': 239000,

    'madurez_activos': {
        2021: 1.60,
        2022: 2.19,
        2023: 2.34,
        2024: 3.07,
        2025: 3.34
    },

    'viajes_integrales_2025': {
        'Usos': 550866653,
        'Viajes': 386751589
    },

    'afluencia_integral_2025': {
        'Férreo': {
            'Usos': 250078507,
            'Viajes': 180683350
        },
        'Tranvía': {
            'Usos': 18741378,
            'Viajes': 10015413
        },
        'Cable': {
            'Usos': 23706418,
            'Viajes': 21635775
        },
        'Cable turístico': {
            'Usos': 602422,
            'Viajes': 602422
        },
        'Bus': {
            'Usos': 44485751,
            'Viajes': 29708256
        },
        'Cuencas 3–6': {
            'Usos': 38058391,
            'Viajes': 22451627
        },
        'C-AMVA': {
            'Usos': 175193786,
            'Viajes': 121654746
        }
    },

    'valor': {
        'horas_ahorradas': 151624446,
        'ahorro_usuarios_m': 2286959,
        'desarrollo_economico_m': 2057821,
        'muertes_evitadas': 130,
        'afecciones_salud_evitadas': 95531,
        'accidentes_evitados': 15013,
        'co2_ev_t': 690913,
        'contaminantes_ev_t': 50432,
        'combustible_ev_gal': 59259119,
        'energia_tj': 406.8,
        'externalidades_billones': 9.44
    },

    'estrategia_2026_2035': [
        'OE1: Impulsar transformaciones en las personas y territorios.',
        'OE2: Alcanzar autonomía financiera.',
        'OE3: Ganar participación de mercado, generar nuevos negocios y expandirse internacionalmente.',
        'OE4: Impulsar la transformación y resiliencia climática.'
    ],

    'valores': [
        'Alegría y pasión',
        'Espíritu innovador',
        'Juntos',
        'Cultura de respeto',
        'Seguridad'
    ],

    'mantenimiento': {
        'modalidades': [
            'Predictivo',
            'Preventivo',
            'Correctivo',
            'Proyectivo'
        ],
        'modos_falla_2016': 5000,
        'modos_falla_2024': 20000,
        'regularidad_A_2022': 96.71,
        'regularidad_A_2023': 94.67,
        'fallas_criticas_incremento_pct': 20
    }
}


# ============================================================
# LÍNEAS DEL SISTEMA
# ============================================================

LINEAS = {
    'A': {
    'modo': 'Metro',
    'recorrido': 'Niquía – La Estrella',

    'longitud_km': 25.6,

    'numero_estaciones': 21,

    'estaciones_elevadas': 8,

    'tipo_sistema': 'Transporte ferroviario',

    'configuracion_tren': 'Tren de tres coches',

    'trenes_ab': 80,

    'vagones_ab': 240,

    'tiempo_recorrido_min': 42,

    'velocidad_comercial_kmh': 40,

    'velocidad_maxima_kmh': 80,

    'frecuencia_minima_min': 2.833333,

    'frecuencia_minima_texto': '2:50 min',

    'capacidad_pax_hora_sentido': 48653,

    'inicio_operacion': '30 de noviembre de 1995',

    'estaciones': [
        'La Estrella',
        'Sabaneta',
        'Itagüí',
        'Envigado',
        'Ayurá',
        'Aguacatala',
        'Poblado',
        'Industriales',
        'Exposiciones',
        'Alpujarra',
        'San Antonio',
        'Parque Berrío',
        'Prado',
        'Hospital',
        'Universidad',
        'Caribe',
        'Tricentenario',
        'Acevedo',
        'Madera',
        'Bello',
        'Niquía',
    ],

    'estaciones_transferencia': [
        'Acevedo',
        'San Antonio',
        'Hospital',
        'Industriales',
    ],

    'fuente_principal': (
        'Metro de Medellín — Página oficial de Línea A'
    ),
},

    'B': {
    'modo': 'Metro',
    'recorrido': 'San Antonio – San Javier',

    'longitud_km': 5.5,

    # La página oficial presenta 7 estaciones en el inventario,
    # pero la ficha técnica indica 6 (5 elevadas).
    'numero_estaciones_ficha': 6,
    'estaciones_elevadas': 5,

    'capacidad_coche': 300,

    'tipo_sistema': 'Férreo',

    'configuracion_tren': 'Tren de tres coches',

    'trenes_ab': 80,

    'vagones_ab': 240,

    'tiempo_recorrido_min': 10.5,

    'velocidad_comercial_kmh': 40,

    'velocidad_maxima_kmh': 80,

    'frecuencia_minima_texto': '3:50 min',

    'capacidad_pax_hora_sentido': 16231,

    'inicio_operacion': '29 de febrero de 1996',

    'estaciones': [
        'San Javier',
        'Santa Lucía',
        'Floresta',
        'Estadio',
        'Suramericana',
        'Cisneros',
        'San Antonio',
    ],

    'estaciones_transferencia': [
        'San Antonio',
        'San Javier',
    ],

    'fuente_principal': (
        'Metro de Medellín — Página oficial de Línea B'
    ),
},

    'J': {
        'modo': 'Metrocable',
        'recorrido': 'San Javier – La Aurora'
    },

    'K': {
        'modo': 'Metrocable',
        'recorrido': 'Acevedo – Santo Domingo'
    },

    'L': {
        'modo': 'Metrocable',
        'recorrido': 'Santo Domingo – Arví'
    },

    'H': {
        'modo': 'Metrocable',
        'recorrido': 'Oriente – Villa Sierra'
    },

    'M': {
        'modo': 'Metrocable',
        'recorrido': 'Miraflores – Trece de Noviembre'
    },

    'P': {
        'modo': 'Metrocable',
        'recorrido': 'Acevedo – El Progreso'
    },

    'T': {
        'modo': 'Tranvía',
        'recorrido': 'San Antonio – Oriente'
    },

    '1': {
        'modo': 'Bus',
        'recorrido': 'Universidad de Medellín – Parque Aranjuez'
    },

    '2': {
        'modo': 'Bus',
        'recorrido': 'Universidad de Medellín – Parque Aranjuez'
    },

    'O': {
        'modo': 'Bus',
        'recorrido': 'Caribe – La Palma'
    }
}


# ============================================================
# LÍNEA T - TRANVÍA DE AYACUCHO
# ============================================================

TRANVIA = {
    'codigo': 'T',
    'nombre': 'Tranvía de Ayacucho',
    'modo': 'Tranvía ferroviario urbano',
    'recorrido': 'San Antonio – Oriente',

    'longitud_km': 4.2,
    'vehiculos': 12,
    'estaciones': 3,
    'paradas': 6,

    'capacidad_vehiculo': 300,
    'recorrido_min': 19,
    'vel_comercial': 16,
    'vel_max': 80,
    'frecuencia_pico': 4.44,
    'capacidad_pax_hs': 3807,

    'inicio': '31 de marzo de 2016',
    'edad': '10 años y 4 meses (agosto 2026)',
    'km_acum_m': 5.1,

    'viajes_2025_m': 9.8,
    'viajes_2024_m': 9.6,
    'meta_2025_m': 9.6,
    'cumplimiento_meta': 102.1,

    'usuarios_dia': 65000,

    'incidentes_2023': 137,
    'peatones_2023': 71,
    'accidentes_2024': 174,

    'normas': [
        'Ley 86 de 1989',
        'Ley 105 de 1993',
        'Ley 310 de 1996',
        'Ley 336 de 1996',
        'Ley 769 de 2002',
        'Decreto 3109 de 1997',
        'Decreto 1008 de 2015'
    ],

    'integraciones': [
        'Línea A',
        'Línea B',
        'Metrocable H',
        'Metrocable M',
        'Línea 2 de buses'
    ],

    'sistemas_rcm': [
        'Guiado',
        'Rodadura y neumáticos',
        'Frenado',
        'Tracción',
        'Suspensión',
        'Neumática',
        'Puertas',
        'Eléctrico y alimentación',
        'Control y señalización',
        'Comunicaciones',
        'Infraestructura de vía',
        'Balizas',
        'Seguridad y emergencia'
    ],

    'horarios': {
        'San Antonio → Oriente': {
            'Lunes a viernes': ('04:35', '23:05'),
            'Sábados': ('04:33', '23:05'),
            'Domingos/festivos': ('05:05', '22:25')
        },

        'Oriente → San Antonio': {
            'Lunes a viernes': ('04:50', '23:33'),
            'Sábados': ('05:09', '23:33'),
            'Domingos/festivos': ('05:21', '22:41')
        }
    }
}


# ============================================================
# INFORMACIÓN PENDIENTE
# ============================================================

PENDIENTES = [
    (
        'Personal por línea',
        'Pendiente',
        'No hay desagregación suficiente en el PDF.'
    ),

    (
        'Inventario completo de activos',
        'Pendiente',
        'Requiere documentación técnica.'
    ),

    (
        'Fichas técnicas',
        'Pendiente',
        'Requiere activos específicos.'
    ),

    (
        'Histórico de fallas',
        'Pendiente',
        'No disponible en detalle suficiente.'
    ),

    (
        'MTBF',
        'Pendiente',
        'Debe calcularse con históricos reales.'
    ),

    (
        'MTTR',
        'Pendiente',
        'Debe calcularse con históricos reales.'
    ),

    (
        'Paradas por fallas',
        'Parcial',
        'Existen eventos públicos, no base completa.'
    ),

    (
        'Programa preventivo',
        'Parcial',
        'Hay rutinas públicas para algunos sistemas.'
    ),

    (
        'Costo de hora-hombre',
        'Pendiente',
        'Requiere información interna.'
    ),

    (
        'Repuestos críticos',
        'Pendiente',
        'Requiere inventario y criticidad.'
    ),

    (
        'Fabricantes',
        'Parcial',
        'Hay información pública de ciertos activos.'
    ),

    (
        'Capacidad por línea',
        'Parcial',
        'Debe desagregarse por modo y línea.'
    ),

    (
        'Demanda mensual',
        'Parcial',
        'Se requiere serie histórica.'
    ),

    (
        'Matriz de criticidad',
        'Pendiente',
        'Debe construirse en el proyecto.'
    ),

    (
        'FMECA / RCM',
        'Pendiente',
        'Etapa posterior.'
    ),

    (
        'Procedimientos de emergencia',
        'Parcial',
        'No todos están disponibles públicamente.'
    ),

    (
        'Costos por falla',
        'Pendiente',
        'Requiere información interna.'
    )
]


# ============================================================
# FUENTES
# ============================================================

FUENTES = [
    (
        'Investigacion_Metro (2).pdf',
        'Documento base consolidado suministrado para el proyecto.'
    ),

    (
        'CONTEXTO OPERACIONAL.pdf',
        'Documento base inicial del contexto operacional.'
    )
]# ============================================================
# SISTEMA DE BUSES - CONTEXTO OPERACIONAL
# Fuente: Contexto Operacional Buses DR000
# ============================================================

BUSES = {

    # --------------------------------------------------------
    # INFORMACIÓN GENERAL
    # --------------------------------------------------------

    "modo": "BRT - Buses de tránsito rápido",

    "operador": "Metro de Medellín",

    "gestores_mantenimiento": [
        "Fundación Pascual Bravo",
        "Equitel Buses"
    ],

    "infraestructura": "Metroplús",

    # --------------------------------------------------------
    # LÍNEAS
    # --------------------------------------------------------

    "lineas": {

        "Línea 1": {

            "longitud_km": 12.5,

            "estaciones": 20,

            "tipo_corredor": "Exclusivo",

            "descripcion": (
                "Corredor vehicular exclusivo que conecta "
                "Universidad de Medellín con Parque Aranjuez."
            ),

            "inicio": "Universidad de Medellín",

            "final": "Parque Aranjuez",

            "velocidad_maxima_kmh": 60,

            "pendiente_max_estacion_paradero_pct": 7,

            "pendiente_max_trazado_pct": 16,

            "radio_horizontal_min_m": 20,

            "altitud_min_msnm": 1474,

            "altitud_max_msnm": 1602.4,

            "ancho_min_via_m": 3.4,

            "tipo_trafico": "Exclusivo"
        },

        "Línea 2": {

            "longitud_km": 18.0,

            "estaciones": 22,

            "tipo_corredor": "Mixto",

            "descripcion": (
                "Corredor que combina tramo troncal con "
                "tramos de tráfico mixto compartidos con "
                "otros vehículos."
            ),

            "tipo_trafico": "Mixto"
        }
    },

    # --------------------------------------------------------
    # FLOTA
    # --------------------------------------------------------

    "flota": {

        "articulados": 30,

        "padrones": 47,

        "total_buses": 77,

        "combustible": "GNV",

        "pasajeros_dia_aprox": 135000,

        "ipk": 9.6
    },

    # --------------------------------------------------------
    # TIPOS DE VEHÍCULO
    # --------------------------------------------------------

    "tipos": {

        "Articulado BLK": {

            "cantidad": 20,

            "marca_motor": "Cummins",

            "modelo_motor": "ISLG 2180",

            "potencia_hp": 320,

            "rpm_potencia": 2000,

            "torque_nm": 1356,

            "rpm_torque": 1300,

            "rango_rpm_torque": "1300–1400",

            "rpm_max": 2100,

            "combustible": "GNV",

            "tanque_gnv_l": 1080,

            "capacidad_pasajeros": 154,

            "masa_admisible_kg": 30000,

            "marca_transmision": "ZF",

            "modelo_transmision": "6AP 1400 B",

            "modelo_convertidor": "W370-6-TP4 D",

            "relacion_diferencial": "1:6,14"
        },

        "Articulado ZT": {

            "cantidad": 10,

            "marca_motor": "Doosan",

            "modelo_motor": "GL11K",

            "potencia_hp": 340,

            "rpm_potencia": 2100,

            "torque_nm": 1392,

            "rpm_torque": 1300,

            "rango_rpm_torque": "1200–1400",

            "rpm_max": 2100,

            "combustible": "GNV",

            "tanque_gnv_l": 1080,

            "capacidad_pasajeros": 154,

            "masa_admisible_kg": 28000,

            "marca_transmision": "Allison",

            "modelo_transmision": "T375R",

            "modelo_convertidor": "TC-421",

            "relacion_diferencial": "1:7,16"
        },

        "Padrón": {

            "cantidad": 47,

            "marca_motor": "Cummins",

            "modelo_motor": "ISLG 2180",

            "potencia_hp": 280,

            "rpm_potencia": 2000,

            "torque_nm": 1220,

            "rpm_torque": 1300,

            "rango_rpm_torque": "1300–1500",

            "rpm_max": 2100,

            "combustible": "GNV",

            "tanque_gnv_l": 720,

            "capacidad_pasajeros": 90,

            "masa_admisible_kg": 19000,

            "marca_transmision": "Allison",

            "modelo_transmision": "T375R",

            "modelo_convertidor": "TC-418",

            "relacion_diferencial": "1:6,83"
        }
    },

    # --------------------------------------------------------
    # SISTEMAS DEL BUS
    # --------------------------------------------------------

    "sistemas": [

        "Motor principal",
        "Transmisión de potencia",
        "Sistema estructural",
        "Sistema de dirección",
        "Sistema de frenos",
        "Sistema eléctrico",
        "Suspensión",
        "Articulación",
        "Sistema de suministro de GNV"
    ],

    # --------------------------------------------------------
    # SISTEMA DE ADMISIÓN Y ESCAPE
    # --------------------------------------------------------

    "admision_escape": {

        "filtracion_particulas_pct": 99.98,

        "tamano_particula_um": 5,

        "presion_max_admision_kpa": 186,

        "flujo_max_lb_min": 32,

        "presion_max_escape_kpa": 17,

        "norma_emisiones": "EURO EEV",

        "restriccion_max_filtro_in_h2o": 25,

        "diferencia_max_intercooler_c": 11.1,

        "restriccion_intercooler_kpa": 13.5,

        "temperatura_max_egr_c": 127,

        "temperatura_proteccion_entrada_turbina_c": 636,

        "temperatura_derrateo_catalizador_c": 389,

        "temperatura_apagado_catalizador_c": 397,

        "ruido_max_escape_db": 85
    },

    # --------------------------------------------------------
    # MANTENIMIENTO MAYOR
    # --------------------------------------------------------

    "mantenimiento_mayor": {

        "kilometraje_aprox": 500000,

        "unidad": "km",

        "aplicaciones": [
            "Motor de combustión interna",
            "Transmisión automática",
            "Plataformas para personas con discapacidad",
            "Chasís",
            "Pisos"
        ]
    }
}# ============================================================
# SISTEMA DE BUSES - CONTEXTO OPERACIONAL
# Fuente: Contexto Operacional Buses DR000
# ============================================================

BUSES = {

    # --------------------------------------------------------
    # INFORMACIÓN GENERAL
    # --------------------------------------------------------

    "modo": "BRT - Buses de tránsito rápido",

    "operador": "Metro de Medellín",

    "gestores_mantenimiento": [
        "Fundación Pascual Bravo",
        "Equitel Buses"
    ],

    "infraestructura": "Metroplús",

    # --------------------------------------------------------
    # LÍNEAS
    # --------------------------------------------------------

    "lineas": {

        "Línea 1": {

            "longitud_km": 12.5,

            "estaciones": 20,

            "tipo_corredor": "Exclusivo",

            "descripcion": (
                "Corredor vehicular exclusivo que conecta "
                "Universidad de Medellín con Parque Aranjuez."
            ),

            "inicio": "Universidad de Medellín",

            "final": "Parque Aranjuez",

            "velocidad_maxima_kmh": 60,

            "pendiente_max_estacion_paradero_pct": 7,

            "pendiente_max_trazado_pct": 16,

            "radio_horizontal_min_m": 20,

            "altitud_min_msnm": 1474,

            "altitud_max_msnm": 1602.4,

            "ancho_min_via_m": 3.4,

            "tipo_trafico": "Exclusivo"
        },

        "Línea 2": {

            "longitud_km": 18.0,

            "estaciones": 22,

            "tipo_corredor": "Mixto",

            "descripcion": (
                "Corredor que combina tramo troncal con "
                "tramos de tráfico mixto compartidos con "
                "otros vehículos."
            ),

            "tipo_trafico": "Mixto"
        }
    },

    # --------------------------------------------------------
    # FLOTA
    # --------------------------------------------------------

    "flota": {

        "articulados": 30,

        "padrones": 47,

        "total_buses": 77,

        "combustible": "GNV",

        "pasajeros_dia_aprox": 135000,

        "ipk": 9.6
    },

    # --------------------------------------------------------
    # TIPOS DE VEHÍCULO
    # --------------------------------------------------------

    "tipos": {

        "Articulado BLK": {

            "cantidad": 20,

            "marca_motor": "Cummins",

            "modelo_motor": "ISLG 2180",

            "potencia_hp": 320,

            "rpm_potencia": 2000,

            "torque_nm": 1356,

            "rpm_torque": 1300,

            "rango_rpm_torque": "1300–1400",

            "rpm_max": 2100,

            "combustible": "GNV",

            "tanque_gnv_l": 1080,

            "capacidad_pasajeros": 154,

            "masa_admisible_kg": 30000,

            "marca_transmision": "ZF",

            "modelo_transmision": "6AP 1400 B",

            "modelo_convertidor": "W370-6-TP4 D",

            "relacion_diferencial": "1:6,14"
        },

        "Articulado ZT": {

            "cantidad": 10,

            "marca_motor": "Doosan",

            "modelo_motor": "GL11K",

            "potencia_hp": 340,

            "rpm_potencia": 2100,

            "torque_nm": 1392,

            "rpm_torque": 1300,

            "rango_rpm_torque": "1200–1400",

            "rpm_max": 2100,

            "combustible": "GNV",

            "tanque_gnv_l": 1080,

            "capacidad_pasajeros": 154,

            "masa_admisible_kg": 28000,

            "marca_transmision": "Allison",

            "modelo_transmision": "T375R",

            "modelo_convertidor": "TC-421",

            "relacion_diferencial": "1:7,16"
        },

        "Padrón": {

            "cantidad": 47,

            "marca_motor": "Cummins",

            "modelo_motor": "ISLG 2180",

            "potencia_hp": 280,

            "rpm_potencia": 2000,

            "torque_nm": 1220,

            "rpm_torque": 1300,

            "rango_rpm_torque": "1300–1500",

            "rpm_max": 2100,

            "combustible": "GNV",

            "tanque_gnv_l": 720,

            "capacidad_pasajeros": 90,

            "masa_admisible_kg": 19000,

            "marca_transmision": "Allison",

            "modelo_transmision": "T375R",

            "modelo_convertidor": "TC-418",

            "relacion_diferencial": "1:6,83"
        }
    },

    # --------------------------------------------------------
    # SISTEMAS DEL BUS
    # --------------------------------------------------------

    "sistemas": [

        "Motor principal",
        "Transmisión de potencia",
        "Sistema estructural",
        "Sistema de dirección",
        "Sistema de frenos",
        "Sistema eléctrico",
        "Suspensión",
        "Articulación",
        "Sistema de suministro de GNV"
    ],

    # --------------------------------------------------------
    # SISTEMA DE ADMISIÓN Y ESCAPE
    # --------------------------------------------------------

    "admision_escape": {

        "filtracion_particulas_pct": 99.98,

        "tamano_particula_um": 5,

        "presion_max_admision_kpa": 186,

        "flujo_max_lb_min": 32,

        "presion_max_escape_kpa": 17,

        "norma_emisiones": "EURO EEV",

        "restriccion_max_filtro_in_h2o": 25,

        "diferencia_max_intercooler_c": 11.1,

        "restriccion_intercooler_kpa": 13.5,

        "temperatura_max_egr_c": 127,

        "temperatura_proteccion_entrada_turbina_c": 636,

        "temperatura_derrateo_catalizador_c": 389,

        "temperatura_apagado_catalizador_c": 397,

        "ruido_max_escape_db": 85
    },

    # --------------------------------------------------------
    # MANTENIMIENTO MAYOR
    # --------------------------------------------------------

    "mantenimiento_mayor": {

        "kilometraje_aprox": 500000,

        "unidad": "km",

        "aplicaciones": [
            "Motor de combustión interna",
            "Transmisión automática",
            "Plataformas para personas con discapacidad",
            "Chasís",
            "Pisos"
        ]
    }
}# ============================================================
# SISTEMA DE BUSES
# ============================================================

BUSES = {
    "modo": "BRT - Buses de tránsito rápido",
    "flota": {
        "articulados": 30,
        "padrones": 47,
        "total_buses": 77,
        "combustible": "GNV",
        "pasajeros_dia_aprox": 135000,
        "ipk": 9.6
    },
    "lineas": {
        "Línea 1": {
            "longitud_km": 12.5,
            "estaciones": 20,
            "tipo_corredor": "Exclusivo"
        },
        "Línea 2": {
            "longitud_km": 18.0,
            "estaciones": 22,
            "tipo_corredor": "Mixto"
        }
    }
}