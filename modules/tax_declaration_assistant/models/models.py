# -*- coding: utf-8 -*-

from odoo import models, fields, api


class tax_declaration_assistant(models.Model):
    _name = 'tax_declaration_assistant.tax_declaration_assistant'
    _description = 'tax_declaration_assistant.tax_declaration_assistant'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()
#
    

