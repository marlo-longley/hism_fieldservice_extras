# -*- coding: utf-8 -*-
from odoo import models, fields

class HISMFieldserviceTemplate(models.Model):
    _inherit = "fsm.location"

    # change required to False
    # Fixes https://github.com/OCA/field-service/issues/683
    partner_id = fields.Many2one('res.partner', string='Related Partner',
                                 required=False, ondelete='restrict',
                                 delegate=True, auto_join=True)