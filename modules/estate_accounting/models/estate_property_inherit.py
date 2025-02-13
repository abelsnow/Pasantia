from odoo import fields, models, api, exceptions
from odoo.exceptions import UserError

# -----------------------------------------------------------------------------------------------------------
# Clase EstateAccounting (que hereda test_model)
# -----------------------------------------------------------------------------------------------------------
class EstateAccounting(models.Model):
    _inherit = "test_model"

    def vender(self):
        # Función heredada de "test_model".
        # Si la propiedad es vendida se genera una factura automáticamente.
        invoice_vals = super().vender()
        if(not self.comprador_id):
            raise UserError("No se puede generar la factura sin un comprador")

        if not self.selling_price:
            raise exceptions.ValidationError("El precio de venta no puede estar vacío.")
        
        invoice_vals = {
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
        }

        invoice = self.env["account.move"].create(invoice_vals)

        return invoice
    

