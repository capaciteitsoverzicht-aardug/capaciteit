# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models


class MachineProductTemplate(models.Model):
    _inherit = 'product.template'

    aa_resource_id = fields.Many2one('resource.resource', string='Machine')
    aa_setup_time_est1 = fields.Float(string='Setup Time EST 1')
    aa_setup_time_est2 = fields.Float(string='Setup Time EST 2')
    aa_prod_time_est = fields.Float(string='Production Time')
