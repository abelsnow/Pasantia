from odoo import models, fields, api
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError

class Producto(models.Model):
    _name = 'producto'
    _description = 'Modelo de Productos'
    name = fields.Char(string="Nombre del Producto", required=True)
    stock = fields.Integer(string="Stock", default=0)
    precio_compra = fields.Float(string="Precio de Compra")
    precio_venta = fields.Float(string="Precio de Venta")
    proveedor_id = fields.Many2one("res.partner", string="Proveedor")
    estado = fields.Selection([
        ('disponible', "Disponible"),
        ('agotado', "Agotado"),
        ('en_camino', "En camino")
    ], string="Estado", default="agotado")
    cantidad = fields.Integer(default=0)
    cantidad_minima = fields.Integer(string="Cantidad Mínima",default=10)
    vencimiento = fields.Date(string="Fecha de Vencimiento", default=lambda self: datetime.today() + timedelta(days=90))
    compra_total = fields.Float(compute='_compute_compra_total', store=True)
    venta_total = fields.Float(compute='_compute_venta_total', store=True)
    ubicacion_id = fields.Many2one("inventario_ubicacion", string="Ubicación de almacenamiento")
    almacen_id = fields.Many2one('inventario_almacen', string="Almacén", compute="_compute_almacen", store=True)
    perecedero = fields.Boolean(default=False)
    cantidad_vendida=fields.Integer(default=0)
    lote_ids=fields.Many2many('inventario_lote')

    ubicacion_ids = fields.Many2many(
        'inventario_ubicacion', 
        string="Ubicaciones",
        
        store=True
    )
  
    @api.depends('ubicacion_id')
    def _compute_almacen(self):
        for reco in self:
            if reco.ubicacion_id:
                almacen = self.env['inventario_almacen'].search([('ubicacion_id', '=', reco.ubicacion_id.id)], limit=1)
                reco.almacen_id = almacen.id if almacen else False

    _sql_constraints = [
    ('product_name', 'UNIQUE(name)', 'El nombre del producto debe ser único'),
    ('precio_venta', 'CHECK(precio_venta > 0)', 'El precio debe ser mayor a 0'),
    ('precio_compra', 'CHECK(precio_compra > 0)', 'El precio de compra debe ser mayor a 0')
]

    def action_comprar(self):
        for reco in self:
            if reco.cantidad <= 0:
                raise ValidationError("La cantidad de artículos comprados debe ser mayor a 0")

            if not reco.ubicacion_id:
                raise ValidationError("Debe seleccionar una ubicación para almacenar el producto")
        
            reco.stock += reco.cantidad
            


            almacen = self.env['inventario_almacen'].search([('ubicacion_id', '=', reco.ubicacion_id.id)], limit=1)
            if almacen:
                almacen.cantidad += reco.cantidad
            else:
                raise ValidationError("No se encontró un almacén asociado a esta ubicación")

            if reco.estado == 'agotado' :
                reco.estado = 'disponible'

    def action_vender(self):
        for reco in self:
            almacen = self.env['inventario_almacen'].search([('ubicacion_id', '=', reco.ubicacion_id.id)], limit=1)
            if reco.cantidad <= 0:
                raise ValidationError("No puede vender 0 productos")
            if reco.estado == 'agotado':
                raise ValidationError("El producto está agotado")
            if reco.estado == 'en_camino':
                raise ValidationError("El producto estará disponible próximamente")
            if reco.stock >= reco.cantidad:
                if(almacen.cantidad < reco.cantidad):
                    raise ValidationError("Esta ubicacion no tiene el stock suficiente")
                almacen.cantidad -= reco.cantidad
                reco.stock -=reco.cantidad
                reco.cantidad_vendida+=reco.cantidad
                if reco.stock == 0:
                    reco.estado = 'agotado'
            else:
                raise ValidationError("No hay stock suficiente")

    @api.depends('cantidad', 'precio_compra')
    def _compute_compra_total(self):
        for reco in self:
            reco.compra_total = reco.cantidad * reco.precio_compra

    @api.depends('cantidad', 'precio_venta')
    def _compute_venta_total(self):
        for reco in self:
            reco.venta_total = reco.cantidad * reco.precio_venta
