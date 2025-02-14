from odoo import fields, models, api, exceptions
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError

# -----------------------------------------------------------------------------------------------------------
# Clase TestModel (estate_property)
# -----------------------------------------------------------------------------------------------------------
class TestModel(models.Model):
    _name = "test_model"
    _description = "Test Model"
    _order = "id desc"

    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default = lambda self: datetime.today() + timedelta(days=90))
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean(default = False)
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north','North'),('south','South'),('east','East'),('west','West')])
    active = fields.Boolean('Activate', default = True)
    state = fields.Selection([('nuevo','Nuevo'),('oferta_recibida','Oferta recibida'),('oferta_aceptada','Oferta aceptada'),('vendido','Vendido'),('cancelado','Cancelado')], default = 'nuevo', required = True)
    tag_ids = fields.Many2many('estate_property_tag', string='tags')
    type_id = fields.Many2one('estate_property_type', string='types')
    vendedor_id = fields.Many2one('res.users', string='vendedor', default = lambda self: self.env.user, readonly=True)
    comprador_id = fields.Many2one('res.partner', string='comprador')
    offer_ids = fields.One2many('estate_property_offer', 'property_id', string='offer_ids')
    total_area = fields.Integer(compute="_compute_total", string="area total")
    best_price = fields.Float(compute="_compute_best_price", string="mejor precio", store=True)
    imagen_1 = fields.Binary(string="imagen")
    imagen_2 = fields.Binary(string="imagen")
    imagen_3 = fields.Binary(string="imagen")
    
    _sql_constraints = [
        ('expected_price_positive', 'CHECK(expected_price > 0)', 'El precio debe ser estrictamente mayor que cero'),
        ('selling_price_positive', 'CHECK(selling_price >= 0)', 'El precio de venta debe ser mayor o igual a cero'),
        ('name_unique', 'UNIQUE(name)', 'Ya existe una propiedad con el mismo nombre')
    ]
        
    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
            
    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids else 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10
        else:
            self.garden_orientation = False
            self.garden_area = 0

    @api.ondelete(at_uninstall=False)
    def delete(self):
        for record in self:
            if record.state not in ['nuevo', 'cancelado']:
                raise UserError("No se puede eliminar una propiedad en ese estado")

    def vender(self):
        for record in self:
            if record.state == "cancelado":
                raise UserError("No se puede vender, se encuentra en estado cancelado")
            if record.state == "vendido":
                raise UserError("La propiedad ya se encuentra vendida")
            else:
                record.state = "vendido"
        return True
    
    def cancelar(self):
        for record in self:
            if record.state == "vendido":
                raise UserError("No se puede cancelar, se encuentra en estado vendido")
            if record.state == "cancelado":
                raise UserError("La propiedad ya se encuentra cancelada")
            else:
                record.state = "cancelado"
        return True
