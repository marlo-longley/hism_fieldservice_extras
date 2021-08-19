# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HISMFieldserviceOrder(models.Model):
    _inherit = "fsm.order"

    # Get the list of tasks performed on this order
    order_activity_ids = fields.One2many('fsm.activity', 'fsm_order_id',
                                         'Activitiy IDs')

    # Optional field to store additional maintenance tasks.
    additional_tasks = fields.Char(type='Text')


    # Called from custom service order report
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

    # Bugfix
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


    # Calculate a bunch of values needed for the custom Service order Report
    # Note, store=True fields are not recomputed if a value exists in DB (not set here)
    site_name = fields.Char(compute='_compute_partner_data', string='Site Name', type='Char')
    site_directions = fields.Char(compute='_compute_partner_data', string='Site Direction', type='Char')
    site_street = fields.Char(compute='_compute_partner_data', string='Site Street', type='Char')
    site_street2 = fields.Char(compute='_compute_partner_data', string='Site Street 2', type='Char')
    site_city = fields.Char(compute='_compute_partner_data', string='Site City', type='Char')
    site_state = fields.Char(compute='_compute_partner_data', string='Site State', type='Char')
    site_zip = fields.Char(compute='_compute_partner_data', string='Site Zip', type='Char')
    # TODO: is owner_id actually being set? OR used? Seems no.
    owner_id = fields.Char(compute='_compute_partner_data', string='Site Owner', type='Char')
    computed_address = fields.Char(compute='_compute_partner_data', string='Site Address', type='Char')

    @api.one
    @api.depends('location_id')
    def _compute_partner_data(self):
        if self.location_id:
            # Get the site information from fsm.location table
            site = self.env['fsm.location'].browse(self.location_id.id)
            self.site_name = site.complete_name
            self.site_directions = site.direction
            # Get the partner res.partner model of the site address
            partner_model = self.env['res.partner'].browse(self.location_id.partner_id.id)
            self.site_street = partner_model.street
            self.site_street2 = partner_model.street2
            self.site_city = partner_model.city
            self.site_state = partner_model.state_id.name
            self.site_zip = partner_model.zip
            # contact_address is a builtin computed field on res.partner we can access
            self.computed_address = partner_model.contact_address

    # Create fields for info on the most recent service order for this location
    last_service_order_id = fields.Char(compute='_compute_last_service_order', string='Last Order ID', type='Char')
    last_service_order_name = fields.Char(compute='_compute_last_service_order', string='Last Order Name', type='Char')
    last_service_order_date = fields.Date(compute='_compute_last_service_order', string='Last Order Date', type='Char')
    last_service_order_description = fields.Char(compute='_compute_last_service_order', string='Last Order Name', type='Char')

    # Called from the report view
    @api.multi
    def _compute_last_service_order(self):
        # Get the other service orders that started before the current record, are not actually the current record, and share the same service location
        # Then select the first item in list since list is ordered by desc. That will be the most recent order in this location.
        related_service_orders = self.env['fsm.order'].search([('location_id', '=', self.location_id.id),
                                                               ('id', '!=', self.id),
                                                               ('scheduled_date_start', '<', self.scheduled_date_start)],
                                                              order='scheduled_date_start desc')

        # If any orders meet all those criteria, set the fields
        # Also setting a return value that can be used in other functions
        if len(related_service_orders) > 0:
            self.last_service_order_id = related_service_orders[0].id
            self.last_service_order_name = related_service_orders[0].name
            self.last_service_order_date = related_service_orders[0].scheduled_date_start.date()
            self.last_service_order_description = related_service_orders[0].description
            return related_service_orders[0].id

    # Returns list of fsm.activities that belong to the last_service_order
    # Called from the report view
    # Only called if last_service_order has value
    @api.multi
    def get_last_tasks(self):
        id = self._compute_last_service_order()
        tasks = self.env['fsm.activity'].search([('fsm_order_id', '=', id)])
        return tasks

    # Returns list of res.partner that have the same parent_id has this order's fms.location's owner_id
    # Called from the report view
    @api.multi
    def get_sibling_contacts(self):
        owner_id = self.location_id.owner_id.id
        related_contacts = self.env['res.partner'].search(["|",('parent_id', '=', owner_id), ('id', '=', owner_id)])
        return related_contacts
