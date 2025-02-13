from odoo import models, field, api

class Usuarios(models.Model):
    _name = 'tax_declaration_assistant.users'
    _description = 'Usuarios registrados en el asistente.'