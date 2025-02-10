from odoo import  models,fields,api

class PropertiesType(models.Model):
    _name = "estate.property.type"
    _description = "Type Properties"
    _order='name'
    
    offer_ids=fields.One2many('estate.property.offer', 'property_type_id', string= 'Offers')
    sequence=fields.Integer('Sequence')
    offer_count=fields.Integer()
    name = fields.Char(required=True)
    property_ids = fields.One2many(
        'estate.property',
        'type_id',
        string='Properties'
    )
    _sql_constraints=[('unique_type_name','UNIQUE(name)','El nombre del tipo  de propiedad debe ser unico')]
    def state_property_offer_action(self):
        return{
            'name': 'Offers',
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property.offer',
            'view_mode': 'tree,form',
            
            'domain': [('property_type_id', '=', self.id)],
            'context': {'default_property_type_id': self.id},
        }