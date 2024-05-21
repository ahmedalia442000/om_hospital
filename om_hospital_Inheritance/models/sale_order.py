from odoo import api, fields, models



class SaleOrder(models.Model):
    _inherit = "sale.order"
    confirmed_user_id = fields.Many2one('res.users', string="Confirmed User")
    def open_order_line_registration_form(self):
        return {
            'name': 'Register Order Lines',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.line.registration',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id}
        }




    # How To Inherit A Function In Odoo
    def action_confirm(self):
        print("success........................", self.env.user.id)
        self.confirmed_user_id = self.env.user.id
        return super(SaleOrder, self).action_confirm()

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['so_confirmed_user_id'] = self.confirmed_user_id.id
        return invoice_vals

    def create_sale_contract(self):
        contract_obj = self.env['sale.contract']

        for order in self:
            contract = contract_obj.create({
                'customer': order.partner_id.name,
                'quotation_date': order.date_order,
                'sal_order': order.name,
                # Add other field values as needed
            })

            # Iterate over order lines and create corresponding contract lines
            contract_lines = []
            for order_line in order.order_line:
                contract_lines.append((0, 0, {
                    'products_id': order_line.product_id.id,
                    'quantaty': order_line.product_uom_qty,
                    # Add other field values as needed
                }))

            # Set the contract lines for the contract
            contract.update({'contract_lines_ids': contract_lines})

        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'يعم خلاص والله عملتلك فاتورة ',
                'type': 'rainbow_man',
            }
        }
        #         # for record in self:
        #     contract_values = {
        #         'customer': record.partner_id.name,
        #         'quotation_date': record.date_order,
        #         'sal_order': record.name,
        #         # Add other field values as needed
        #
        #     }
        #     self.env['sale.contract'].create(contract_values)
        #
        # return {
        #     'effect': {
        #         'fadeout': 'slow',
        #         'message': 'يعم خلاص والله عملتلك فاتورة ',
        #         'type': 'rainbow_man',
        #     }
        # }


