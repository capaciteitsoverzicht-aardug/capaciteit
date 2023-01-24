# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################
from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    x_aa_av_mu_ids = fields.One2many(related='product_tmpl_id.x_aa_av_mu_ids')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_aa_av_mu_ids = fields.One2many('ansova.mu', 'x_aa_av_product_id', string='MUs')
