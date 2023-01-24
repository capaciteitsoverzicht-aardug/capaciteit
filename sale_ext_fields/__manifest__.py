# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'SO Fields',
    'version': '16.0.0.5',
    'summary': 'Add page and fields on sale order.',
    'description': """ 
        In this module add new page "ansova info"
        add new binary fields as well as project id field on sales order. 
        """,
    'category': 'sales',
    'author': 'Aardug, Arjan Rosman',
    'website': 'arosman@aardug.nl',
    'depends': ['sale_management', 'crm_location'],
    'data': [
        'security/ir.model.access.csv',
        'views/delengroep_views.xml',
        'views/vormgroep_views.xml',
        'views/product_views.xml',
        'views/sale_order_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sale_ext_fields/static/src/css/sale_order_view.css',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
