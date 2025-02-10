from odoo import models, fields, api
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'  # Heredar modelo de facturas

    check_restablecer_borrador = fields.Boolean(
        string="Restablecer a Borrador",default=False
        
    )

   
  
        
    def _compute_show_reset_to_draft_button(self):
        super()._compute_show_reset_to_draft_button
        for move in self:

            if move.show_reset_to_draft_button:
            
                move.show_reset_to_draft_button = move.check_restablecer_borrador
                
            
