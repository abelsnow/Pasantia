from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CompraLote(models.Model):
    _name = 'inventario.lote'
    _description = 'Lote de Compra de Productos'
    name = fields.Char(string="Referencia", required=True, copy=False, default=lambda self: self.env['ir.sequence'].next_by_code('compra.lote'))
    proveedor_id = fields.Many2one('res.partner', string="Proveedor", required=True)
    fecha_compra = fields.Date(string="Fecha de Compra", default=fields.Date.today, required=True)
    lineas_compra_id = fields.One2many('inventario.lote.linea', 'lote_id', string="Productos Comprados")
    costo_total = fields.Float(string="Costo Total", compute='_compute_costo_total', store=True)
    productos_id=fields.Many2many("producto")
    @api.depends('lineas_compra.subtotal')
    def _compute_costo_total(self):
        for lote in self:
            lote.costo_total = sum(lote.lineas_compra.mapped('subtotal'))

    def action_confirmar_compra(self):
        for lote in self:
            for linea in lote.lineas_compra:
                producto = linea.producto_id
                producto.stock += linea.cantidad
                producto.ubicacion_id = lote.ubicacion_id
                producto.almacen_id = lote.almacen_id
                producto.fecha_compra = lote.fecha_compra
                if producto.stock > 0:
                    producto.estado = 'disponible'

class CompraLoteLinea(models.Model):
    _name = 'inventario.lote.linea'
    _description = 'Línea de Productos en un Lote de Compra'

    lote_id = fields.Many2one('inventario.lote', string="Lote de Compra", required=True, ondelete='cascade')
    producto_id = fields.Many2one('producto', string="Producto", required=True)
    cantidad = fields.Integer(string="Cantidad", required=True, default=1)
    precio_unitario = fields.Float(string="Precio Unitario", related='producto_id.precio_compra', readonly=True)
    subtotal = fields.Float(string="Subtotal", compute='_compute_subtotal', store=True)

    @api.depends('cantidad', 'precio_unitario')
    def _compute_subtotal(self):
        for linea in self:
            linea.subtotal = linea.cantidad * linea.precio_unitario
            