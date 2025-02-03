from odoo import api,models,fields
from odoo.exceptions import UserError

class EstateAccount(models.Model):
    _inherit="estate.property"
    def action_sold(self):
        print("Metodo action_sold sobreescrito correctamente")
        res = super().action_sold()
        
        for property in self:
            if not property.buyer_id:
                raise UserError("No se puede vender una propiedad sin comprador")
            
            invoice = self.env["account.move"].create({
                "partner_id": property.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    (0,0, {
                        "name" : "6% of selling price",
                        "quantity" : 1,
                        "price_unit": property.selling_price * 0.06,
                    }),
                    (0,0, {
                        "name" : "Admin fees",
                        "quantity" : 1,
                        "price_unit": 100,
                    })
                ]
            })

        return res
    