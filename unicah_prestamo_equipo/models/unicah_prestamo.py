from odoo import api, fields, models
from odoo.exceptions import ValidationError

DIAS_MAXIMOS = 7
PRESTAMOS_MAXIMOS_ACTIVOS = 3


class UnicahPrestamo(models.Model):
    _name = "unicah.prestamo"
    _description = "Préstamo de equipo"
    _inherit = ["mail.thread"]
    _order = "fecha_prestamo desc, id desc"

    name = fields.Char(string="Referencia", readonly=True, copy=False, default="Nuevo")
    equipo_id = fields.Many2one(
        "unicah.equipo", string="Equipo", required=True, tracking=True
    )
    partner_id = fields.Many2one(
        "res.partner", string="Solicitante", required=True, tracking=True
    )
    fecha_prestamo = fields.Date(
        string="Fecha de préstamo", required=True, default=fields.Date.context_today
    )
    fecha_prevista = fields.Date(string="Devolución prevista", required=True)
    fecha_devolucion = fields.Date(string="Devuelto el", readonly=True, copy=False)
    dias_prestamo = fields.Integer(
        string="Días de préstamo", compute="_compute_dias_prestamo", store=True
    )
    dias_retraso = fields.Integer(
        string="Días de retraso", compute="_compute_dias_retraso"
    )
    state = fields.Selection(
        [("borrador", "Borrador"), ("prestado", "Prestado"), ("devuelto", "Devuelto")],
        string="Estado",
        default="borrador",
        tracking=True,
        copy=False,
    )
    notas = fields.Text(string="Notas")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nuevo") == "Nuevo":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("unicah.prestamo") or "Nuevo"
                )
        return super().create(vals_list)

    @api.depends("fecha_prestamo", "fecha_prevista")
    def _compute_dias_prestamo(self):
        for p in self:
            if p.fecha_prestamo and p.fecha_prevista:
                p.dias_prestamo = (p.fecha_prevista - p.fecha_prestamo).days
            else:
                p.dias_prestamo = 0

    @api.depends("fecha_prevista", "fecha_devolucion", "state")
    def _compute_dias_retraso(self):
        hoy = fields.Date.context_today(self)
        for p in self:
            p.dias_retraso = 0
            if not p.fecha_prevista or p.state == "borrador":
                continue
            fin = p.fecha_devolucion or hoy
            p.dias_retraso = max((fin - p.fecha_prevista).days, 0)

    @api.constrains("fecha_prestamo", "fecha_prevista")
    def _check_fechas(self):
        for p in self:
            if p.fecha_prevista < p.fecha_prestamo:
                raise ValidationError(
                    "La devolución prevista no puede ser anterior al préstamo."
                )
            if (p.fecha_prevista - p.fecha_prestamo).days > DIAS_MAXIMOS:
                raise ValidationError(
                    f"Un préstamo no puede durar más de {DIAS_MAXIMOS} días."
                )

    def action_entregar(self):
        for p in self:
            if p.state != "borrador":
                continue
            if not p.equipo_id.disponible:
                raise ValidationError(
                    f"El equipo {p.equipo_id.name} ya está prestado."
                )
            activos = self.search_count([
                ("partner_id", "=", p.partner_id.id),
                ("state", "=", "prestado"),
            ])
            if activos >= PRESTAMOS_MAXIMOS_ACTIVOS:
                raise ValidationError(
                    f"{p.partner_id.name} ya tiene {activos} préstamos activos "
                    f"(máximo {PRESTAMOS_MAXIMOS_ACTIVOS})."
                )
            p.state = "prestado"

    def action_devolver(self):
        for p in self:
            if p.state == "prestado":
                p.write({
                    "state": "devuelto",
                    "fecha_devolucion": fields.Date.context_today(self),
                })
                if p.dias_retraso:
                    p.message_post(
                        body=f"Devuelto con {p.dias_retraso} día(s) de retraso."
                    )
