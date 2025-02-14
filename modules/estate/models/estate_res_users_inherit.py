from odoo import fields, models, api, exceptions
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError

# -----------------------------------------------------------------------------------------------------------
# Clase resUser (que hereda res.users)
# -----------------------------------------------------------------------------------------------------------
class resUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('test_model', 'vendedor_id', string='Propiedades', domain=[('active', '=', True)])