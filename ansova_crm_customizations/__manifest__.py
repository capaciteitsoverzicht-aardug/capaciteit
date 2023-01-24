# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Ansova CRM Customizations',
    'version': '16.0.0.1',
    'summary': 'Customizations to CRM.',
    'description': """ 
        Specific customizations for Ansova in the CRM app.
        """,
    'category': 'Sales/CRM',
    'author': 'Aardug, Arjan Rosman',
    'website': 'arosman@aardug.nl',
    'depends': ['crm', 'product', 'sale', 'sale_ext_fields', 'crm_location'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'views/product_views.xml',
        'views/sale_order_views.xml'
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
