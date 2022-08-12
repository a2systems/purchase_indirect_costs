from odoo import tools, models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date,datetime

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    account_move_ids = fields.One2many(comodel_name='account.move',inverse_name='purchase_order_id',string='Facturas')

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def _compute_total_unit_cost(self):
        res = 0
        for rec in self:
            if rec.order_id.amount_untaxed == 0:
                res = 0
            else:
                amount_invoices = 0
                for invoice in rec.order_id.account_move_ids:
                    tax_percent = invoice.amount_total / invoice.amount_untaxed
                    amount_invoices = amount_invoices + (abs(invoice.amount_total_in_currency_signed) / tax_percent)
                percent = rec.price_subtotal / rec.order_id.amount_untaxed
                res = (rec.price_subtotal + amount_invoices * percent) / rec.product_qty
            rec.total_unit_cost = res

    total_unit_cost = fields.Float('Costo total unitario',compute=_compute_total_unit_cost)


class AccountMove(models.Model):
    _inherit = 'account.move'

    purchase_order_id = fields.Many2one('purchase.order','Orden de compra')

