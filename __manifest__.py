# -*- coding: utf-8 -*-
{
    'name': "hism_fieldservice_extras",

    'summary':  "Extra functionality for the fieldservice module",

    'description': "Extends Activities into custom Tasks; Adds reporting for Tasks."
    ,

    'author': "Marlo Longley",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'fieldservice',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'fieldservice', 'fieldservice_activity'],

    # always loaded
    'data': [
        'views/order.xml',
        #'views/report.xml',
        'views/location_history_list_view.xml',
        'views/template.xml',
        'reports/custom_service_order_report.xml',
        'reports/custom_report_header.xml',
        'reports/custom_report_address.xml',
    ],
}