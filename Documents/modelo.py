from odoo import fields, models,api
from datetime import datetime, timedelta
from odoo.exceptions import UserError,ValidationError
class TestModel(models.Model):
    _name = "test.model"
    _description = "Test Model"
    _order='id desc'
    name = fields.Char(required=True)
    description = fields.Text()
    postal_code = fields.Char()
    expected_price = fields.Float(required=True)
    price_sold = fields.Float(readonly=True, copy=False)
    rooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Integer(default=2)
    garden = fields.Boolean("Garden",default=False)
    garden_area = fields.Integer()
    date_available = fields.Date(copy=False, default=lambda self: datetime.today() + timedelta(days=90))
    active = fields.Boolean("Active", default=True)
    total_area= fields.Float(compute='_compute_total_area', store=True)
    best_price=fields.Float(compute='_compute_best_price', store=True)
    stat = fields.Selection(
        [
            ("New", "new"),
            ('Sold', 'sold'),
            ('Offer Received', 'offer received'),
            ('Cancelled', 'cancelled'),
            ('Offer Accepted', 'offer accepted')
        ],
        default="New", copy=False,
    )
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    type_id = fields.Many2one("type.properties")
    tag_ids = fields.Many2many("test.tag")
    salesman_id = fields.Many2one("res.users", string="Salesman")
    buyer_id = fields.Many2one("res.partner", string="Buyer")

    _sql_constraints = [
        ('expected_price', 'CHECK(expected_price > 0)',
         'The expected price must more than 0 .')
    ]
    _sql_constraints=[('unique_tag_name','UNIQUE(name)','El nombre de la propiedad debe ser unico')]

    def action_cancel(self):    
        for reco in self: 
            if reco.stat =="Sold":
                raise UserError("No puedes cancelar una propiedad vendida.")
            reco.stat='Cancelled'
            return True
        
    def action_sold(self):
        for reco in self :
            if reco.stat =="Cancelled":
                raise UserError("No puedes comprar una propiedad Cancelada")   
            reco.stat="Sold" 
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'),default=0.0)
    @api.onchange('garden')
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = False
        else:
            self.garden_area =10
            self.garden_orientation = 'north'

    offer_ids = fields.One2many(
        'test.offer', 
        'property_id',
        string="Offers"
        
       
    )
    @api.ondelete(at_uninstall=False)
    def prevent_delete(self):
            for reco in self:
                if reco.stat not in ['New','Cancelled']:
                    raise UserError('No se puede eliminar una propiedad que no sea Nueva o este Cancelada')
                
                

class EstatePropertyTag(models.Model):
    _name = "test.tag"
    _description = "Estate Property Tags"
    _order='name'
    name = fields.Char(required=True)
    _sql_constraints=[('unique_tag_name','UNIQUE(name)','El nombre de la etiqueta debe ser unico')]
    color = fields.Integer(string="Color") 
class PropertiesType(models.Model):
    _name = "type.properties"
    _description = "Type Properties"
    _order='name'
    offer_ids=fields.One2many('test.offer', 'property_type_id', string= 'Offers')
    sequence=fields.Integer('Sequence')
    offer_count=fields.Integer()
    name = fields.Char(required=True)
    property_ids = fields.One2many(
        'test.model',
        'type_id',
        string='Properties'
    )
    _sql_constraints=[('unique_type_name','UNIQUE(name)','El nombre del tipo  de propiedad debe ser unico')]
    def state_property_offer_action(self):
        return{
            'name': 'Offers',
            'type': 'ir.actions.act_window',
            'res_model': 'test.offer',
            'view_mode': 'tree,form',
            
            'domain': [('property_type_id', '=', self.id)],
            'context': {'default_property_type_id': self.id},
        }
    
class Offer(models.Model):
    _name = 'test.offer'
    _order='price desc'
    _description = "Offers related to properties"

    price = fields.Float(string="Offer Price")
    stat = fields.Selection([
        ('acepted', 'Acepted'),
        ('refused', 'Refused'),
    ], copy=False,)
    partner_id = fields.Many2one(
        'res.partner',
        string="Partner",
        required=True,
    )
    property_type_id = fields.Many2one(
    'type.properties', 'type_id'
    
)

    
    validy=fields.Integer(string="Validy",default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )
    @api.depends('validy')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = datetime.today() + timedelta(days=record.validy)
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                delta = (record.date_deadline - datetime.today().date()).days
                record.validy = delta    
                  
    property_id = fields.Many2one(
        'test.model',
        string="Property",
        required=True
    )
    def action_accept(self):
        for reco in self:
            if reco.property_id.stat == 'Sold':
                raise UserError("No puedes  aceptar una oferta  para una propiedad vendida")
            elif(reco.price>=reco.property_id.expected_price *0.9):
                
                reco.stat='acepted'
                reco.property_id.stat='Sold'
                reco.property_id.price_sold=reco.price
                reco.property_id.buyer_id=reco.partner_id
            else:
                raise ValidationError("El precio debe al menos el 90 porciento del precio esperado ;")
                 
            return True
   
    def action_refuse(self):
        for reco in self:
            reco.stat="refused"
        return True
    
    @api.model
    def create (self, vals):
        property_id = self.env['test.model'].browse(vals['property_id'])
        if property_id.offer_ids and vals['price'] < max(property_id.offer_ids.mapped('price')):
            raise UserError("No se puede crear una oferta menor a las ya existentes!")
        offer =super(Offer,self).create(vals)
        property_id.stat = 'Offer Received'
        
        return offer
    
    
class ResUser(models.Model):
    _inherit="res.users"
    property_ids=fields.One2many(
        comodel_name="test.model",
        inverse_name="salesman_id",
        string='Properties',
        domain=[('active','=','True')]
        
    )