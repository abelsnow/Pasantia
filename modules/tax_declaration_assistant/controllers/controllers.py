# -*- coding: utf-8 -*-
# from odoo import http


# class TaxDeclarationAssistant(http.Controller):
#     @http.route('/tax_declaration_assistant/tax_declaration_assistant', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tax_declaration_assistant/tax_declaration_assistant/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tax_declaration_assistant.listing', {
#             'root': '/tax_declaration_assistant/tax_declaration_assistant',
#             'objects': http.request.env['tax_declaration_assistant.tax_declaration_assistant'].search([]),
#         })

#     @http.route('/tax_declaration_assistant/tax_declaration_assistant/objects/<model("tax_declaration_assistant.tax_declaration_assistant"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tax_declaration_assistant.object', {
#             'object': obj
#         })

