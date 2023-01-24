# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################
from odoo import api, models, fields, _


class MU(models.Model):
    _name = 'ansova.mu'
    _description = 'MU/Grams'
    _rec_name = 'x_aa_av_name'

    x_aa_av_mu_m2 = fields.Integer(string='Mu', default=0)
    x_aa_av_grams = fields.Float(string='Gram/m²', default=0.0)
    x_aa_av_name = fields.Char(string='Name', compute='_compute_mu_name')
    x_aa_av_product_id = fields.Many2one('product.template', string='Product')

    @api.depends('x_aa_av_mu_m2', 'x_aa_av_grams')
    def _compute_mu_name(self):
        for rec in self:
            rec.x_aa_av_name = _("%s Mu = %s Gram/m²" % (rec.x_aa_av_mu_m2, rec.x_aa_av_grams))
