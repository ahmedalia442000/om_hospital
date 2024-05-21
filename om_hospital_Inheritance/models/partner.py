from odoo import api, fields, models


class PartnerCategory(models.Model):
    _name = 'res.partner.category'
    _inherit = ['res.partner.category', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char(tracking=True)

