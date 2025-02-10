from odoo  import models,fields,api
class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"
    _order='name'
    name = fields.Char(required=True)
    _sql_constraints=[('unique_tag_name','UNIQUE(name)','El nombre de la etiqueta debe ser unico')]
    color = fields.Integer(string="Color") 
