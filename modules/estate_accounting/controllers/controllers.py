# -*- coding: utf-8 -*-
# from odoo import http


# class EstateAccounting(http.Controller):
#     @http.route('/estate_accounting/estate_accounting', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/estate_accounting/estate_accounting/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('estate_accounting.listing', {
#             'root': '/estate_accounting/estate_accounting',
#             'objects': http.request.env['estate_accounting.estate_accounting'].search([]),
#         })

#     @http.route('/estate_accounting/estate_accounting/objects/<model("estate_accounting.estate_accounting"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('estate_accounting.object', {
#             'object': obj
#         })

