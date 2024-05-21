from odoo import api, fields, models
class PatientTag(models.Model):
    _name = "patient.tag"
    _description = "Patient Tag"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char(string="Name", required=True, trim=False)
    active = fields.Boolean(string="Active", default=True, copy=False)
    color = fields.Integer(string="Color")
    color_2 = fields.Char(string="Color 2")
    sequence = fields.Integer(string="Sequence")

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if not default:
            default = {}
            default['name'] = self.name + "(copy)"
            default['sequence'] = 10
        return super(PatientTag, self).copy(default=default)



    _sql_constraints = [('unique_tag_name', 'unique(name, active)', 'name must be unique'),
    ('check_sequence', 'check (sequence > 0)', 'sequence must be > 0')]
