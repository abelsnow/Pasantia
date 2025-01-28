from odoo import api,fields, models
from datetime import datetime, timedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    
    name = fields.Char(required=True)
    buyer_id = fields.Many2one('res.users', string='Buyer', copy=False)
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
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer received', 'Offer received'),
        ('offer accepted', 'Offer accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], default='new', copy=False, required=True)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    type_id = fields.Many2one('estate.property.type', string='Property Type')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    best_price = fields.Float(compute='_compute_best_price',string='Mejor Precio', store=True)
    total_area = fields.Float(compute='_compute_total_area',string= 'Total Area', store=True)
    
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
    name = fields.Char(required=True)

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Type'
    name = fields.Char(required=True)
    estate_property_ids = fields.One2many('estate.property', 'type_id', string='Properties')

class Offer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer'
    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity= fields.Integer(string='Validity (days)', default=7)
    date_deadline= fields.Date(string='Deadline', inverse='_compute_deadline', store=True)
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