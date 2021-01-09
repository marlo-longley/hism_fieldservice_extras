# -*- coding: utf-8 -*-
from odoo import models, fields

class HISMFieldserviceTemplate(models.Model):
    _inherit = "fsm.template"

    # Fix spelling in inherited model from "Activites" to "Activities"
    temp_activity_ids = fields.One2many('fsm.activity', 'fsm_template_id',
                                        'Activities')

