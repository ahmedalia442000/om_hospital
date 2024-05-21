import random
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _rec_name = 'sequence'
    _order = 'id desc'

    patient_id = fields.Many2one('hospital.patient', string="Patient", ondelete='restrict')
    appointment_time = fields.Datetime(string="Appointment Time", default=fields.Datetime.now)
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today)
    gender = fields.Selection(string="Gender", related='patient_id.gender', readonly=False)
    ref = fields.Char(string="Reference", help="Reference for patient from patient record")
    sequence = fields.Char(string="sequence")
    prescription = fields.Html(string="Prescription")
    priority = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'very High')], string='Priority')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], string='Status', default='draft', reguired=True)
    doctor_id = fields.Many2one('res.users', string="Doctor", tracking=True)
    pharmacy_lines_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string="Pharmacy Lines")
    hide_sales_price = fields.Boolean(string="Hide Sales price")
    operation_id = fields.Many2one('hospital.operation', string="Operation")
    progress = fields.Integer(string="Progress", compute='_compute_progress')
    duration = fields.Float(string="Duration")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id')
    amount_total = fields.Monetary(string="Total", compute='_compute_amount_total', currency_field='currency_id')


    @api.depends('pharmacy_lines_ids')
    def _compute_amount_total(self):
        for rec in self:
            amount_total = 0
            for line in rec.pharmacy_lines_ids:
                amount_total += line.price_subtotal
            rec.amount_total = amount_total

    def action_notification(self):
        action = self.env.ref('om_hospital.action_hospital_patient')
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('click to open patient'),
                'message': '%s',
                'links': [{
                    'label': self.patient_id.name,
                    'url': f'#action={action.id}&id={self.patient_id.id}&model=hospital.patient'
                }],
                'sticky': False,
                # Return Action With Sticky Notification In Odoo
                    'next': {
                    'type': 'ir.actions.act_window',
                    'res_model': 'hospital.patient',
                    'res_id': self.patient_id.id,
                    'views': [(False, 'form')]

                }

            }
        }



    def action_share_whatsapp(self):
        if not self.patient_id.phone_number:
            raise ValidationError(_("missed phone"))
        dd = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.patient_id.phone_number, 'Hi *%s*' % self.patient_id.name)
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': dd
        }


    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = random.randrange(0, 25)
            elif rec.state == 'in_consultation':
                progress = random.randrange(25, 75)
            elif rec.state == 'done':
                progress = 100
            else:
                progress = 0
            rec.progress = progress

    @api.model
    def create(self, vals):
        print('fffffffff', vals)
        vals['sequence'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        ss = super(HospitalAppointment, self).create(vals)

        seq = 0
        for line in ss.pharmacy_lines_ids:
            seq += 1
            line.seq = seq
        return ss

    def write(self, vals):
        ss = super(HospitalAppointment, self).write(vals)
        seq = 0
        for line in self.pharmacy_lines_ids:
            seq += 1
            line.seq = seq
        return ss

    def unlink(self):
        for rec in self:
            if rec.state not in 'draft':
                raise ValidationError(_("you can delete record as (draft) only"))
        return super(HospitalAppointment, self).unlink()

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def action_test(self):
        print("Button Clicked")
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'https://www.odoo.com',
        }

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'خلاص حصل ياصحبي وطبع',
                    'type': 'rainbow_man',
                }
            }

    def action_cancel(self):
        ss = self.env.ref('om_hospital.action_cancel_appointment').read()[0]
        return ss

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'



class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"
    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(string="Price", related='product_id.list_price', readonly=False, digits='Product Price')
    qty = fields.Integer(string="Quantity", default="1")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    price_subtotal = fields.Monetary(string="Subtotal", compute='_compute_price_subtotal', currency_field='company_currency_id')
    company_currency_id = fields.Many2one('res.currency', string='Currency', related='appointment_id.currency_id')
    seq = fields.Integer(string = "line Num")


    @api.depends('price_unit', 'qty')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.price_unit * rec.qty