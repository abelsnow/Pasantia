from odoo import api,fields, models
from datetime import datetime, timedelta
from odoo.exceptions import UserError,ValidationError
class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order= 'id desc'
    
    name = fields.Char(required=True)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    description = fields.Char()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: datetime.today() + timedelta(days=90), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean(default=False)
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    type_id = fields.Many2one('estate.property.type', string='Property Type')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers', readonly=1, invisible= "[(state, 'in', ['offer_accepted', 'sold', 'canceled'])]")
    best_price = fields.Float(compute='_compute_best_price',string='Mejor Precio', store=True)
    total_area = fields.Float(compute='_compute_total_area',string= 'Total Area', store=True)
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    state = fields.Selection([
        ('new', 'New'),
        ('offer received', 'Offer received'),
        ('offer accepted', 'Offer accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], default='new', copy=False, required=True)
    
    @api.ondelete(at_uninstall=False)
    def _error_when_user_delete_property(self):
        for record in self:
            if record.state not in[
                'new',
                'canceled']:
                raise UserError('No se puede eliminar una propiedad en ese estado')
        
        


    _sql_constraints = [
        ('expected_price_positive', 'CHECK(expected_price > 0)', 'The expected price must be positive.'),
        ('selling_price_non_negative', 'CHECK(selling_price > 0)', 'The selling price must be positive.'),
        ('property_name_unique', 'UNIQUE(name)', 'The property name must be unique.'),
    ]

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError('Una propiedad vendida no puede cancelarse')
            record.state = 'canceled'

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError('Una propiedad cancelada no puede venderse')
            record.state = 'sold'

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = min(record.offer_ids.mapped('price')) if record.offer_ids else 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10
        else:
            self.garden_orientation = False
            self.garden_area = 0



class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tag'
    _order= 'name asc'

    name = fields.Char(required=True)
    color= fields.Selection([
        ('0', 'Red'),
        ('1', 'Blue'),
        ('2', 'Green'),
    ], string="Color", default='0')
    _sql_constraints = [
    ('tag_name_unique', 'UNIQUE(name)', 'The property tag name must be unique')
]

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Type'
    _order= 'sequence, name asc'

    offer_ids=fields.One2many('estate.property.offer', 'property_type_id', string= 'Offers')
    offer_count=fields.Integer(string='Offer count', compute='_compute_offer_count')
    sequence=fields.Integer('Sequence',default=1)
    name = fields.Char(required=True)
    estate_property_id = fields.One2many('estate.property', 'type_id', string='Properties')
    _sql_constraints     = [
    ('type_name_unique', 'UNIQUE(name)','The property type name must be unique')
]
    def action_view_offers(self):
        return{
            'name': 'Offers',
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property.offer',
            'view_mode': 'tree,form',
            'domain': [('property_type_id', '=', self.id)],
            'context': {'default_property_type_id': self.id},
        }
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
            
class Offer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer'
    _order = 'price desc'
    price = fields.Float()
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity= fields.Integer(string='Validity (days)', default=7)
    date_deadline= fields.Date(string='Deadline', inverse='_compute_deadline', store=True)
    property_type_id=fields.Many2one('estate.property.type', string = 'Ofertas de Tipo', related='property_id.type_id', store=True)
    active_id= fields.Many2one('estate.property')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False)

    _sql_constraints = [
        ('offer_price_positive', 'CHECK(price > 0)', 'The offer price must be positive')
    ]
    def action_refuse(self):
        for record in self:
            if record.property_id.state =='sold':
                raise UserError('No se puede cancelar una oferta ya aceptada')
            else:
                record.status = 'refused'
                record.property_id.state= 'canceled'
            return True
    
    def action_accepted(self):
        for record in self:
            if record.property_id.state == 'sold':
                raise UserError('No se puede aceptar una oferta de una casa ya vendida!')
            elif(record.price>= record.property_id.expected_price * 0.9):
                record.status = 'accepted'
                record.property_id.state = 'sold'
                record.property_id.buyer_id = record.partner_id.id
                record.property_id.selling_price = record.price
                record.property_id.state = 'sold'
            else:
                raise ValidationError('El precio tiene que ser de el 90%')


    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline=False
    def inverse_date_deadline(self):
        for record in self:
           if record.date_deadline and record.create_date:
            record.validity = (record.date_deadline - record.create_date).days 
        else:
            record.validity= 0

    @api.model
    def create (self, vals):
        property_id = self.env['estate.property'].browse(vals['property_id'])
        if property_id.offer_ids and vals['price'] < max(property_id.offer_ids.mapped('price'), default= 0):
            raise UserError("No se puede crear una oferta menor a las ya existentes!")
        offer =super(Offer,self).create(vals)
        if property.state == 'new':
            property_id.state = 'offer received'
        
        return offer
class resUser(models.Model):
    _inherit="res.users"
    property_ids= fields.One2many('estate.property', 'salesperson_id', domain=[('active', '=', True)])
