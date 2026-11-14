{
    "name": "UNICAH Préstamo de Equipo",
    "version": "1.0",
    "summary": "Control de préstamo de equipo (proyectores, laptops, etc.) a estudiantes y docentes",
    "category": "Services",
    "author": "Michael Mayorga",
    "depends": ["base", "mail"],
    "data": [
        "security/ir.access.csv",
        "data/ir_sequence_data.xml",
        "views/unicah_equipo_views.xml",
        "views/unicah_prestamo_views.xml",
        "views/res_partner_views.xml",
        "views/menus.xml",
    ],
    "license": "LGPL-3",
    "application": True,
}
