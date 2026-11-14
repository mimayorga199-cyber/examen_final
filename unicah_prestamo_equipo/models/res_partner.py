from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    prestamo_ids = fields.One2many("unicah.prestamo", "partner_id", string="Préstamos")
    prestamo_count = fields.Integer(
        string="Préstamos", compute="_compute_prestamo_count"
    )

    def _compute_prestamo_count(self):
        for partner in self:
            partner.prestamo_count = len(partner.prestamo_ids)

    def action_ver_prestamos(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Préstamos",
            "res_model": "unicah.prestamo",
            "view_mode": "list,form",
            "domain": [("partner_id", "=", self.id)],
            "context": {"default_partner_id": self.id},
        }
