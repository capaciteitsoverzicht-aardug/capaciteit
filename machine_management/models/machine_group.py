# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models


class MachineGroup(models.Model):
    _name = 'aa.machine.group'
    _description = 'group machine'
    _rec_name = 'aa_code'
    _order = 'aa_code'

    aa_code = fields.Char(string='Code', size=7)
    aa_name = fields.Char(string='Name', size=32)
