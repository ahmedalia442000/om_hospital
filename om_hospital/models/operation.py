
from odoo import api, fields, models

class HospitalPatient(models.Model):
    _name = "hospital.operation"
    _description = "Hospital Operation"
    _log_access = False
    _rec_name = 'operation_name'
    _order = 'sequence,id'

    operation_name = fields.Char(string="Name")
    doctor_id = fields.Many2one('res.users', string="Doctor")
    ref_record = fields.Reference(selection=[('hospital.patient', 'Patient'), ('hospital.appointment', 'Appointment')], string="Record")
    sequence = fields.Integer(string="Sequence", default=10)

    @api.model
    def name_create(self, name):
        print('ffffffffffffffffff', name)
        return self.create({'operation_name': name}).name_get()[0]




