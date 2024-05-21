{
    'name':"om odoo Inheritance",
'sammary' :'',
    'description':""" """,
   'category':'',
    'author': 'Abo Ali',
    'sequence':-100,
    'version':'0.1',
 'depends': ['sale', 'mail'],
'data': [

    'security/ir.model.access.csv',
    'wizard/wizard.xml',
    'views/sale_order_view.xml',
    'views/account_move.xml',
    'views/partner.xml',

],
 'demo':[],
    'application': True,
    'auto_install': False,
    'lisence':'LGPL-3',
}
