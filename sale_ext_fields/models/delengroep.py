# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################
from odoo import api, fields, models


class Delengroep(models.Model):
    _name = 'ansova.delengroep'
    _description = 'Delengroep'
    _rec_name = 'x_aa_av_name'

    def _get_default_currency_id(self):
        return self.env.company.currency_id.id

    x_aa_av_currency_id = fields.Many2one('res.currency', default=_get_default_currency_id)

    x_aa_av_name = fields.Char(string='Name')
    x_aa_av_price = fields.Monetary(string='Extra per m2', currency_field='x_aa_av_currency_id')
