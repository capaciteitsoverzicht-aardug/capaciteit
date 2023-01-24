# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################
from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    def _get_default_currency_id(self):
        return self.env.company.currency_id.id

    x_aa_av_currency_id = fields.Many2one('res.currency', default=_get_default_currency_id)
    x_aa_av_price_m2 = fields.Monetary(string='Color group price m2', currency_field='x_aa_av_currency_id')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    x_aa_av_is_color = fields.Boolean(related='product_tmpl_id.x_aa_av_is_color', readonly=False)
    x_aa_av_layer_title = fields.Char(related='product_tmpl_id.x_aa_av_layer_title', readonly=False)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_aa_av_is_color = fields.Boolean(string='Is Color')
    x_aa_av_layer_title = fields.Char(string='Layer Title')
