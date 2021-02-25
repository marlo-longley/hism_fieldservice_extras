# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HISMFieldserviceOrder(models.Model):
    _inherit = "fsm.order"

    # Fix spelling in inherited model from "Activites" to "Activities"
    order_activity_ids = fields.One2many('fsm.activity', 'fsm_order_id',
                                         'Activities')
    def get_activity_data(self):
        if self.order_activity_ids:
            activity_list = []
            for activity in self.order_activity_ids:
                activity_list.append({'name': activity.name,
                                      'required': activity.required,
                                      'completed_on': activity.completed_on,
                                      'score': activity.score,
                                      'after': activity.after,
                                      'ref': activity.ref,
                                      'notes': activity.notes,
                                      'state': activity.state})
            return activity_list

    @api.onchange('template_id')
    # Need to avoid calling parent fieldservice_activity/fsm_order.py because it contains a bug https://github.com/OCA/field-service/issues/509
    # This workaround isn't ideal but it prevents tasks being deleted from templates
    # Code below from fieldservice/models/fsm_order.py (grandparent) and fieldservice_activity/fsm_order.py (parent) as a result
    def _onchange_template_id(self):
        if self.template_id:
            activity_list = []
            for temp_activity in self.template_id.temp_activity_ids:
                activity_list.append({'name': temp_activity.name,
                                       'required': temp_activity.required,
                                       'ref': temp_activity.ref,
                                       'state': temp_activity.state})
            self.order_activity_ids = activity_list
            self.category_ids = self.template_id.category_ids
            self.scheduled_duration = self.template_id.hours
            self.copy_notes()
            if self.template_id.type_id:
                self.type = self.template_id.type_id
            if self.template_id.team_id:
                self.team_id = self.template_id.team_id


