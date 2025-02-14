from odoo import fields, models, api, exceptions
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError

# -----------------------------------------------------------------------------------------------------------
# Clase tag (estate_property_tag)
# -----------------------------------------------------------------------------------------------------------
class tag(models.Model):
    _name = "estate_property_tag"
    _description = "La etiqueta"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Selection([('0','Blanco'),('1','Naranja'),('2','Naranja claro'),('3','Amarillo'),('4','Celeste'),('5','Marron'),('6','Salmón'),('7','Azul marino'),('8','Azul oscuro'),('9','Rojo'),('10','Verde'),('11','Lila')])
