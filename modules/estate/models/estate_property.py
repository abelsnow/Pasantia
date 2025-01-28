from odoo import fields, models
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
    garden = fields.Boolean()
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


class TestComputed(models.Model):
    _name = 'test.computed'
    _description = 'Test Computed'

    total = fields.Float(compute='_compute_total')
    ammount = fields.Float()

    @api.depends('ammount')
    def _compute_total(self):
        for record in self:
            record.total = 2.0 * record.amount  