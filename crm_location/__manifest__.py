# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'CRM Location',
    'version': '16.0.0.0',
    'summary': 'Location model in CRM.',
    'description': """ 
        Adds a simpel location management model to CRM Configuration.
        """,
    'category': 'Sales/CRM',
    'author': 'Aardug, Arjan Rosman',
    'website': 'arosman@aardug.nl',
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/location_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
