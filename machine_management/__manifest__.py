# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': "machine management",
    'summary': """""",
    'description': """
       
    """,
    'author': "Aardug, Arjan Rosman",
    'website': "http://www.aardug.nl/",
    'support': 'arosman@aardug.nl',
    'category': 'Project',
    'license': 'LGPL-3',
    'version': '16.0',
    'depends': ['project', 'sale_management', 'product', 'hr',
                'resource', 'sale', 'base', 'sale_project','web'],
    'data': [
        'security/ir.model.access.csv',
        'data/project_data.xml',
        'views/machine_group_view.xml',
        'views/order_line_view.xml',
        'views/product_template_view.xml',
        'views/resource_view.xml',
        'views/project_task_view.xml',
        'views/capacity_machine_view.xml',
        'wizard/procedure_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'machine_management/static/src/scss/*',
            # 'machine_management/static/src/js/all_machine_kanban.js',
            'machine_management/static/src/js/edit_kanban.js',
            '/machine_management/static/src/xml/aa_templates.xml'
        ],
        'web.assets_qweb': [
            # '/machine_management/static/src/xml/aa_templates.xml'
        ],
    },
    'application': False,
    'auto_install': False,
    'installable': True,
}
