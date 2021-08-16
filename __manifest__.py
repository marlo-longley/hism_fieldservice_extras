# -*- coding: utf-8 -*-
{
    'name': "hism_fieldservice_extras",

    'summary': """
        Module for extending the Field Service addon to suit Advanced Water Systems. """,

    'description': "Extends Activities into custom Tasks; Adds reporting for Tasks; Creates custom printed reports."
    ,

    'author': "Marlo Longley",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'fieldservice',
    'version': '0.1',

    # any module necessary for this one to work correctly
    # need account dependency because we are extending an account template for modifying the invoice report
    'depends': ['base', 'account', 'fieldservice', 'fieldservice_activity', ],

    # always loaded
    'data': [
        'views/order.xml',
        'views/location_history_list_view.xml',
        'views/template.xml',
        'reports/custom_service_order_report.xml',
        'reports/custom_report_header.xml',
        'reports/custom_report_address.xml',
        'reports/modified_invoice_report.xml',
        'views/field_service_location_form.xml',
        'views/field_service_worker_form.xml'
    ],
}