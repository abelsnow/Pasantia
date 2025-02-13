from odoo import fields, models, api, exceptions
from odoo.exceptions import UserError

# -----------------------------------------------------------------------------------------------------------
# Clase AccountMoveInherit (que hereda test_model)
# -----------------------------------------------------------------------------------------------------------
class AccountMoveInherit(models.Model):
    _inherit="account.move"

    resetDraftAccess = fields.Boolean(default=False, string="Permiso para restablecer a borrador")

    def _compute_show_reset_to_draft_button(self):
        # Función heredada de account.move
        # Realiza la misma función, luego se activa o desactiva el botón de restablecer de acuerdo al campo resetDraftAccess si tiene permiso.
        super()._compute_show_reset_to_draft_button()
        
        # Se asigna valor booleano de boton de permiso a boton de restabler.
        for move in self:
            if move.show_reset_to_draft_button:
                move.show_reset_to_draft_button = move.resetDraftAccess        
                # Verificación de grupo a nivel lógico.
                if not self.env.user.has_group('estate_accounting.usuarios_admin'):
                    move.show_reset_to_draft_button = False