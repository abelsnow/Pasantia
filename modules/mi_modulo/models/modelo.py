from odoo import fields, models,api
from datetime import datetime, timedelta
from odoo.exceptions import UserError

class TestModel(models.Model):
    _name = "estate.property"
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
    type_id = fields.Many2one("estate.property.type")
    tag_ids = fields.Many2many("estate.property.tag")
    salesman_id = fields.Many2one("res.users", string="Salesman")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    offer_ids = fields.One2many(
        'estate.property.offer', 
        'property_id',
        string="Offers" 
    )


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

   
    @api.ondelete(at_uninstall=False)
    def prevent_delete(self):
            for reco in self:
                if reco.stat not in ['New','Cancelled']:
                    raise UserError('No se puede eliminar una propiedad que no sea Nueva o este Cancelada')
                
                

    

