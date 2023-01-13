# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models


class aa_resource(models.Model):
    _inherit = 'resource.resource'

    aa_code = fields.Char(string='Code', size=7)
    aa_prod_time_norm = fields.Float('Prod Time Normal')
    aa_machine_group_id = fields.Many2one(
        'aa.machine.group', string='Machine Group'
    )
    aa_zero = fields.Boolean(string='Zero')
    aa_parent_resource = fields.Many2one('resource.resource', string='Parent Resource')
