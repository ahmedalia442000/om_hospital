{
    'name':"Hospital Managment",
'sammary' :'Hospital Managment System',
    'description':""" Hospital Managment System """,
   'category':'Hospital',
    'author': 'Abo Ali',
    'sequence':-100,
    'version':'0.1',
 'depends': ['mail','product','base','report_xlsx'],
'data': [
    'security/ir.model.access.csv',

        'data/sequence_data.xml',
    'data/patient_tag.xml',
    'data/patient.tag.csv',
    'data/appointment.xml',
        'wizard/cancel_appointment_view.xml',
        'wizard/appointment_report_view.xml',
    'views/menu.xml',
    'views/patient.view.xml',
    'views/operation.view.xml',
    'views/res_config_settings_views.xml',
    'views/odoo_playground_view.xml',
    'views/female_patient_view.xml',
    'views/appointment.view.xml',
    'views/patient_tag.xml',
    'reports/report.xml',
    'reports/appointment_details_template.xml',
    'reports/patient_card.xml',


],
 'demo':[],
    'application': True,
    'auto_install': False,
    'lisence':'LGPL-3',
}