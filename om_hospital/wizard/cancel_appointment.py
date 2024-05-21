from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    reason = fields.Text(string="Reason")
    date_cancel = fields.Date(string="Cancellation Date")

    @api.model
    def default_get(self, fields):
        print('yyyyyyyyyyy', self.env.context)
        print('yyyyyyyyyyy', fields)
        ss = super(CancelAppointmentWizard, self).default_get(fields)
        ss['date_cancel'] = date.today()
        # if self.env.context.get('active_id'):
        #     ss['appointment_id'] = self.env.context.get('active_id')
        return ss

    def action_cancel(self):
        cancel_day = self.env['ir.config_parameter'].get_param('om_hospital.cancel_days')
        allowed_date = self.appointment_id.booking_date - relativedelta.relativedelta(days=int(cancel_day))
        if allowed_date < date.today():
            raise ValidationError(_("cancellation not allowed because booking date"))
        self.appointment_id.state = 'cancel'
        # dd = """"select name from hospital_patient"""
        # self.env.cr.execute(dd)
        # ss = self.env.cr.fetchall()
        # print("ss", ss)
        return {

            'view_mode': 'form',
            'res_model': 'cancel.appointment.wizard',
            'res_id': self.id,
            'target': 'new',
            'type': 'ir.actions.act_window',

        }
        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        # }

        # if self.appointment_id.booking_date == fields.date.today():
        #     raise ValidationError(_("SORRY NOT CANCELL ALLOWED THE SAME BOOKING DATE"))
        #
        # return
