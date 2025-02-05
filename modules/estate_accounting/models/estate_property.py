from odoo import fields, models, api, exceptions

class EstateAccounting(models.Model):
    _inherit = "test_model"

    def vender(self):
        print("FUNCAAAAAAAAAAAAAAAAAAAAA")
        return super().vender()
    
