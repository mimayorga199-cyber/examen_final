from odoo import api, fields, models


class UnicahEquipo(models.Model):
    _name = "unicah.equipo"
    _description = "Equipo prestable"

    name = fields.Char(string="Nombre", required=True)
    codigo = fields.Char(string="Código de inventario", required=True, copy=False)
    categoria = fields.Selection(
        [
            ("proyector", "Proyector"),
            ("laptop", "Laptop"),
            ("camara", "Cámara"),
            ("otro", "Otro"),
        ],
        string="Categoría",
        required=True,
        default="otro",
    )
    active = fields.Boolean(string="Activo", default=True)
    prestamo_ids = fields.One2many("unicah.prestamo", "equipo_id", string="Préstamos")
    disponible = fields.Boolean(string="Disponible", compute="_compute_disponible")

    _codigo_unico = models.Constraint(
        "UNIQUE(codigo)", "El código de inventario debe ser único."
    )

    @api.depends("prestamo_ids.state")
    def _compute_disponible(self):
        for equipo in self:
            equipo.disponible = not any(
                p.state == "prestado" for p in equipo.prestamo_ids
            )
