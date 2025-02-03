from odoo import api,models,fields

class EstateAccount(models.Model):
    _inherit="estate.property"
    def action_sold(self):
        print("Metodo action_sold sobreescrito correctamente")
        res = super().action_sold()
        self.env["account.move"].create({
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
        })

        return res