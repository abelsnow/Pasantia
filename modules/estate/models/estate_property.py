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
    vendedor_id = fields.Many2one('res.partner', string='vendedor', default = lambda self: self.env.user, readonly=True)
    comprador_id = fields.Many2one('res.partner', string='comprador')
    offer_ids = fields.One2many('estate_property_offer', 'property_id', string='offer_ids')
    total_area = fields.Integer(compute="_compute_total", string="area total")
    best_price = fields.Float(compute="_compute_best_price", string="mejor precio", store=True)
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

# -----------------------------------------------------------------------------------------------------------
# Clase tag (estate_property_tag)
# -----------------------------------------------------------------------------------------------------------
class tag(models.Model):
    _name = "estate_property_tag"
    _description = "La etiqueta"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Selection([('0','Blanco'),('1','Azul'),('2','Celeste')])

# -----------------------------------------------------------------------------------------------------------
# Clase oferta (estate_property_offer)
# -----------------------------------------------------------------------------------------------------------
class oferta(models.Model):
    _name = "estate_property_offer"
    _description = "Ofertas y esas cosas"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection([('aceptado','Aceptado'),('rechazado','Rechazado')], copy=False, readonly=True)
    validity = fields.Integer(string="validez de la oferta")
    date_deadline = fields.Date(string="fecha limite de la oferta", compute='_compute_validity', default=lambda self: datetime.today())
    partner_id = fields.Many2one('res.partner', string='Cliente', required=True)
    property_id = fields.Many2one('test_model', string='Propiedad', required=True, ondelete='cascade')
    property_type_id = fields.Many2one('estate_property_type', string='Ofertas del tipo')
    offer_type = fields.Char(related='property_type_id.name', default=lambda self: self.property_type_id.name)
    active_id = fields.Boolean(related='property_id.active')
    _sql_constraints = [('price_positive','CHECK(price > 0)','El precio debe ser estrictamente mayor que cero')]

    @api.depends('validity')
    def _compute_validity(self):
        for record in self:
            record.date_deadline = datetime.today() + timedelta(days=record.validity)

    def action_aceptar(self):
        for record in self:
            if record.property_id.state == 'vendido':
                raise UserError("Ya se encuentra vendido")
            
            elif record.property_id.state == 'oferta_aceptada':
                raise UserError("Esta propiedad ya tiene una oferta aceptada")
            
            elif record.property_id.state == 'cancelado':
                raise UserError("Esta propiedad se encuentra en estado cancelado")
            
            else:
                record.status = 'aceptado'
                record.property_id.state = 'oferta_aceptada'
                record.property_id.selling_price = record.price
                #record.property_id.vendedor_id = record.partner_id.id
                record._check_price()
            return True

    def action_rechazar(self):
        for record in self:
            record.status = 'rechazado'

    @api.constrains('price', 'property_id.expected_price', 'property_id.selling_price')
    def _check_price(self):
        for record in self:
            if record.price < 0.9 * record.property_id.expected_price:
                raise ValidationError("La propiedad no se puede vender a un valor menor que el 90%")
            
    @api.model
    def create(self, vals):
        property_id = self.env['test_model'].browse(vals['property_id'])
        if property_id.offer_ids and vals["price"]  >= max(property_id.offer_ids.mapped('price')):
            offer = super(oferta, self).create(vals)
            property_id.state = 'oferta_recibida'
            return offer
        elif not property_id.offer_ids:
            offer = super(oferta, self).create(vals)
            property_id.state = 'oferta_recibida'
            return offer
        else:
            raise UserError("No se puede crear la oferta porque es demasiado baja")

# -----------------------------------------------------------------------------------------------------------
# Clase resUser (que hereda res.users)
# -----------------------------------------------------------------------------------------------------------
class resUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('test_model', 'vendedor_id', string='Propiedades', domain=[('active', '=', True)])