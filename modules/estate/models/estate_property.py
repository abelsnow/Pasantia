from odoo import fields, models, api
from datetime import datetime, timedelta

class TestModel(models.Model):
    _name = "test_model"
    _description = "Test Model"

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
    vendedor_id = fields.Many2one('res.users', string='vendedor', default = lambda self: self.env.user)
    comprador_id = fields.Many2one('res.users', string='comprador')
    offer_ids = fields.Many2many('estate_property_offer', string='ofertas')
    total_area = fields.Integer(compute="_compute_total", string="area total")
    best_price = fields.Float(compute="_compute_best_price", string="mejor precio")
        
    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
            
    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'))

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10
        else:
            self.garden_orientation = False
            self.garden_area = 0

class tipo(models.Model):
    _name = "estate_property_type"
    _description = "Los tipos de propiedades (casa, apartamento, ático, castillo)"

    name = fields.Char(required=True)

class tag(models.Model):
    _name = "estate_property_tag"
    _description = "La etiqueta"

    name = fields.Char(required=True)

class oferta(models.Model):
    _name = "estate_property_offer"
    _description = "Ofertas y esas cosas"

    price = fields.Float()
    status = fields.Selection([('disponible','indispuesto')], copy=False)
    validity = fields.Integer(inverse="_inverse_validity", string="validez de la oferta")
    date_deadline = fields.Date(string="fecha limite de la oferta")
    partner_id = fields.Many2one('res.partner', string='Cliente', required=True)
    property_id = fields.Many2one('test_model', string='Propiedad', required=True)

    @api.depends('validity')
    def _inverse_validity(self):
        for record in self:
            record.date_deadline = record.date_deadline.today() + timedelta(days=record.validity)