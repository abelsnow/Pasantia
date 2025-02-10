from odoo import models,fields,api 
from odoo.exceptions import UserError,ValidationError
from datetime import datetime,timedelta
    
class Offer(models.Model):
    _name = 'estate.property.offer'
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
    'estate.property.type', 'type_id'
    
)

    
    validy=fields.Integer(string="Validy",default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_compute_inverse_date_deadline",
        store=True
    )
    @api.depends('validy')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = datetime.today() + timedelta(days=record.validy)
    def _compute_inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                delta = (record.date_deadline - datetime.today().date()).days
                record.validy = delta    
                  
    property_id = fields.Many2one(
        'estate.property',
        string="Property",
        required=True
    )
    def action_accept(self):
        for reco in self:
            if reco.property_id.stat == 'Sold':
                raise UserError("No puedes  aceptar una oferta  para una propiedad vendida")
            elif(reco.price>=reco.property_id.expected_price *0.9):
                
                reco.stat='acepted'
                reco.property_id.stat='Offer Accepted'
                reco.property_id.price_sold=reco.price
                reco.property_id.buyer_id=reco.partner_id
            else:
                raise ValidationError("El precio debe al menos el 90 % del precio esperado ;")
                 
            return True
   
    def action_refuse(self):
        for reco in self:
            reco.stat="refused"
        return True
    
    @api.model
    def create (self, vals):
        property_id = self.env['estate.property'].browse(vals['property_id'])
        if property_id.offer_ids and vals['price'] < max(property_id.offer_ids.mapped('price')):
            raise UserError("No se puede crear una oferta menor a las ya existentes!")
        offer =super(Offer,self).create(vals)
        property_id.stat = 'Offer Received'
        
        return offer
    