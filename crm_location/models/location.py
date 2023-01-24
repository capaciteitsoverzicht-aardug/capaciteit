# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################
from odoo import models, fields


class Location(models.Model):
    _name = 'ansova.location'
    _description = 'Location'
    _rec_name = 'x_aa_av_name'

    x_aa_av_name = fields.Char(string='Name')
    x_aa_av_street = fields.Char(string='Street')
    x_aa_av_zip = fields.Char(change_default=True, string='ZIP')
    x_aa_av_city = fields.Char(string='City')
    x_aa_av_state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                                       domain="[('country_id', '=?', x_aa_av_country_id)]")
    x_aa_av_country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    x_aa_av_project_leader_id = fields.Many2one('res.users', string='Project leader')
    x_aa_av_project_leader_phone = fields.Char(related='x_aa_av_project_leader_id.phone')
