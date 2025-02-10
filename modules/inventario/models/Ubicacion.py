from odoo import fields, models, api

class Ubicacion(models.Model):
    _name = 'inventario_ubicacion'
    _description = 'Lugares donde se guardan los productos'

    name = fields.Char(string="Nombre de la Ubicación", required=True)
    ciudad = fields.Selection([
        ('luque', "Luque"),
        ('limpio', "Limpio"),
        ('asuncion', "Asunción"),
        ('san_lorenzo', "San Lorenzo"),
        ('capiata', "Capiatá")
    ], required=True)
    almacen_id = fields.One2many('inventario_almacen', 'ubicacion_id', string="Almacén asociado", readonly=True)

    @api.model
    def create(self, vals):
        ubicacion = super(Ubicacion, self).create(vals)
        almacen = self.env['inventario_almacen'].create({
            'name': f"Almacén en {ubicacion.name}",
            'ubicacion_id': ubicacion.id
        })
        return ubicacion
