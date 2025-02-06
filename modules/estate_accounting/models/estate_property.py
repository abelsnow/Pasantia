from odoo import fields, models, api, exceptions
from odoo.exceptions import UserError

# -----------------------------------------------------------------------------------------------------------
# Clase Estate_Accounting (que hereda test_model)
# -----------------------------------------------------------------------------------------------------------
class EstateAccounting(models.Model):
    _inherit = "test_model"

    def vender(self):
        factura = super().vender()
        if(not self.comprador_id):
            raise UserError("No se puede generar la factura sin un comprador")
        else:
            factura = self.env["account.move"].create({
                "partner_id": self.comprador_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    (0,0, {
                        "name" : "6% of selling price",
                        "quantity" : 1,
                        "price_unit": self.selling_price * 0.06,
                    }),
                    (0,0, {
                        "name" : "Admin fees",
                        "quantity" : 1,
                        "price_unit": 100,
                    })
                ]
            })

        return factura