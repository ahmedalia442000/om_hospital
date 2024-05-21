# -*- coding: utf-8 -*-

import base64
import io
from odoo import models


class PatientAppointmentXlsx(models.AbstractModel):
    _name = 'report.om_hospital.report_patient_appointment_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):
        appointments = data.get('appointments', [])
        if not appointments:
            return

        print("ffffffffff", appointments)

        sheet = workbook.add_worksheet('Appointments')
        bold = workbook.add_format({'bold': True})
        row = 3
        col = 3
        sheet.write(row, col, 'Name', bold)
        sheet.write(row, col + 1, 'Sequence', bold)

        for appointment in appointments:
            patient_id = appointment.get('patient_id', '')  # Handle missing or incorrect 'patient_id'
            sequence = appointment.get('sequence', '')  # Handle missing 'sequence'

            row += 1
            # Ensure 'patient_id' is a list or tuple before accessing its elements
            if isinstance(patient_id, (list, tuple)) and len(patient_id) > 0:
                sheet.write(row, col, patient_id[1])
            else:
                sheet.write(row, col, '')

            sheet.write(row, col + 1, sequence)

# class PatientAppointmentXlsx(models.AbstractModel):
#     _name = 'report.om_hospital.report_patient_appointment_xls'
#     _inherit = 'report.report_xlsx.abstract'
#
#     def generate_xlsx_report(self, workbook, data, patients):
#         print("ffffffffff", data['appointments'])
#         sheet = workbook.add_worksheet('Appointments')
#         bold = workbook.add_format({'bold': True})
#         row = 3
#         col = 3
#         sheet.write(row, col, 'Name', bold)
#         sheet.write(row, col + 1, 'sequence', bold)
#         for appointment in data['appointments']:
#             row += 1
#             sheet.write(row, col, appointment['patient_id'][0])
#             sheet.write(row, col + 1, appointment['sequence'])



