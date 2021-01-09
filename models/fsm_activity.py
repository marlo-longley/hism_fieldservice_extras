# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HISMFieldserviceActivity(models.Model):
    _inherit = "fsm.activity"

    @api.one
    @api.depends('fsm_order_id')
    def _compute_location(self):
        if self.fsm_order_id:
            order = self.env['fsm.order'].browse(self.fsm_order_id.id)
            location = self.env['fsm.location'].browse(order.location_id.id)
            self.location_name = location.complete_name

    # Computed fields used in 'groupby' (e.g. graphs in views/report.xml) must be set to store=True
    # Note, store=True fields are not recomputed if a value exists in DB
    location_name = fields.Char(compute='_compute_location', string='Location',
                                type='Char',
                                store=True)

    # Fix spelling in inherited model from "Requireid" to "Required"
    required = fields.Boolean('Required', default=False,
                              readonly=True,
                              states={'todo': [('readonly', False)]})

    # Optional field to store numeric test results. Can be used as filter in reports.
    result = fields.Float('Result/Score')


