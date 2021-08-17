# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HISMAccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.one
    @api.depends('partner_id')
    # Method to be called by modified invoice template
    def get_billing_address(self):
        if self.partner_id:
            # First, assume there is no separate billing address and use the main contact
            billing_contact = self.env['res.partner'].browse(self.partner_id.id)
            # Get sibling/related contacts, and see if any of those are marked with type=invoice
            sibling_contacts = self.env['res.partner'].search([('parent_id', '=', self.partner_id.id)])
            for contact in sibling_contacts:
                if contact.type == 'invoice':
                    billing_contact = contact
            # This was returning a list with 1 item, so using [0]
            return billing_contact[0]