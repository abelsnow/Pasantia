from odoo import fields, models, api, exceptions
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError

# -----------------------------------------------------------------------------------------------------------
# Clase tipo (estate_property_type)
# -----------------------------------------------------------------------------------------------------------
class tipo(models.Model):
    _name = "estate_property_type"
    _description = "Los tipos de propiedades (casa, apartamento, ático, castillo)"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many('test_model', 'type_id', string='property')
    offer_ids = fields.One2many('estate_property_offer', 'property_type_id', string='offer_ids')
    offer_count = fields.Integer(compute='_compute_offer_count', string='Offer counts')
    sequence = fields.Integer('sequence')

    def open_type_offer_related_action(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Ofertas del Tipo",
            "res_model": "estate_property_offer",
            "view_mode": "tree,form",
            "domain": [("property_type_id", "=", self.id)],
            "context": {"default_property_type_id": self.id}
        }
    
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
