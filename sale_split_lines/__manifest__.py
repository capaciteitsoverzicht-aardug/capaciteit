# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'SO Split Lines',
    'version': '16.0.0.0',
    'summary': 'Module to Split order lines on Sale Order',
    'description': """ 
        Module to select wizard for split sale 
        order line based on number of order lines selection
        Split line based on delivery qty and schedule date
        Carry forward info to task related to sales lines
        """,
    'category': 'sales',
    'author': 'Aardug, Arjan Rosman',
    'website': 'arosman@aardug.nl',
    'depends': ['sale_management', 'project_enterprise', 'sale_ext_fields'],
    'data': [
            'security/ir.model.access.csv',
            'wizard/split_line_views.xml',
            'views/sale_order_view.xml',
            'views/project_task_view.xml',
            ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
