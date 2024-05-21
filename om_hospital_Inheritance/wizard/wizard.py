
from odoo import models, fields, api


class SaleOrderLineRegistration(models.TransientModel):
    _name = 'sale.order.line.registration'
    _description = 'Register Order Lines'

    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Integer(string='Quantity')
    order_id = fields.Many2one('sale.order', string='Order')

    def save_order_line(self):
        self.ensure_one()
        if self.order_id:
            self.order_id.write({
                'order_line': [(0, 0, {
                    'product_id': self.product_id.id,
                    'product_uom_qty': self.quantity,
                    # Add other fields if necessary
                })]
            })