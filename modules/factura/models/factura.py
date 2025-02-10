from odoo import api,models,fields
from odoo.exceptions import UserError

class EstateAccount(models.Model):
    _inherit="estate.property"
    def action_sold(self):
        

        for property in self:
            if not property.buyer_id:
                raise UserError("No se puede vender una propiedad sin comprador")
            
            res = super().action_sold()
            invoice = self.env["account.move"].create({
                "partner_id": property.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    (0,0, {
                        "name" : "6% of selling price",
                        "quantity" : 1,
                        "price_unit": property.price_sold * 0.06,
                    }),
                    (0,0, {
                        "name" : "Admin fees",
                        "quantity" : 1,
                        "price_unit": 100,
                    })
                ]
            })
        print(f"Factura creada con ID {invoice.id}")
        return res