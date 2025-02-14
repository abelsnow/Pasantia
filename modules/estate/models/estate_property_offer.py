from odoo import fields, models, api, exceptions
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError

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
    offer_type = fields.Char(related='property_type_id.name')
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
