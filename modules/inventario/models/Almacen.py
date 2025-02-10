from odoo import fields, models,api

class Almacen(models.Model):
    _name = 'inventario_almacen'
    _description = 'Lugar donde se guardan los productos'

    name = fields.Char(string="Nombre del Almacén", required=True)
    ubicacion_id = fields.Many2one('inventario_ubicacion', string="Ubicación", ondelete="cascade", required=True)
    producto_ids = fields.One2many('producto', 'almacen_id', string="Productos en este almacén")
    cantidad = fields.Integer(string="Cantidad Total de Productos", compute="_compute_cantidad_total", store=True,default=0)
    productos_vendidos = fields.Integer(compute='_compute_productos_vendidos', store=True)
   
    @api.depends('cantidad_vendida', 'precio_venta')
    def _compute_ingresos_totales(self):
        for producto in self:
            producto.ingresos_totales = producto.cantidad_vendida * producto.precio_venta
    def _compute_cantidad_total(self):
        for almacen in self:
            almacen.cantidad = sum(almacen.producto_ids.mapped('stock'))

   
  