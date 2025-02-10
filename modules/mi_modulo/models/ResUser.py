from odoo import fields, models,api
class ResUser(models.Model):
    _inherit="res.users"
    property_ids=fields.One2many(
        comodel_name="estate.property",
        inverse_name="salesman_id",
        string='Properties',
        domain=[('active','=','True')]
        
    )