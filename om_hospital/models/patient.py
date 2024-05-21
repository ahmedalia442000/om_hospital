from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta
class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"
    name = fields.Char(string="Name", tracking=True, trim= False)
    ref = fields.Char(string="Reference")
    age = fields.Integer(string="Age", compute="_compute_age", inverse='_inverse_compute_age', search='_search_age', tracking=True)
    date_of_birth = fields.Date(string="Date Of Birth")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True, default='female')
    active = fields.Boolean(string="Active", default=True)
    image_id = fields.Image(string="Image")
    tags_ids = fields.Many2many('patient.tag', 'hospital_patient_rel', 'patient_id', 'tag_id', string="Tags")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointments")
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count', store=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointment_ids")
    parent = fields.Char(string="Parent")
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')], string="Marital Status", tracking=True)
    partner_name = fields.Char(string="Partner Name")
    is_birthday = fields.Boolean(string="Birthday", compute='_compute_is_birthday')
    phone_number = fields.Char(string="Phone")
    e_mail = fields.Char(string="Email")
    website = fields.Char(string="Website")


    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                if date.today().day == rec.date_of_birth.day and date.today().month == rec.date_of_birth.month:
                    is_birthday = True
            rec.is_birthday = is_birthday



    def action_view_appointment(self):
        return {
            'name': _('Appointment'),
            'view_mode': 'list,form',
            'res_model': 'hospital.appointment',
            'target': 'current',
            'domain': [('patient_id', '=', self.id)],
            'type': 'ir.actions.act_window',
            'context': {'default_patient_id': self.id}
        }
    @api.ondelete(at_uninstall=False)
    def _check_appointment(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_("you can't delete patient with appoint"))


    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("The entered date is not acceptable"))


    @api.model
    def create(self, vals):
        print('jjjjjjjjjjj', vals)
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).create(vals)



    def write(self, vals):
        print('jjjjjjjjjjj', vals)
        if not self.ref:
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).write(vals)


    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 1


    @api.depends('age')
    def _inverse_compute_age(self):
        for rec in self:
            rec.date_of_birth = date.today() - relativedelta.relativedelta(years=rec.age)

    def _search_age(self, operator, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '<=', end_of_year)]



    def name_get(self):
            return [(rec.id, "%s[%s]" % (rec.ref, rec.name)) for rec in self]

    def action_test(self):
        print('click')


    # def name_get(self):
    #     patient_list = []
    #     for rec in self:
    #         dd = rec.ref + ' ' + rec.name
    #         patient_list.append((rec.id, dd))
    #     return patient_list






