# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################
from odoo import api, fields, models


class Vormgroep(models.Model):
    _name = 'ansova.vormgroep'
    _description = 'Vormgroep'
    _rec_name = 'x_aa_av_vormgroep'

    def _get_default_currency_id(self):
        return self.env.company.currency_id.id

    x_aa_av_currency_id = fields.Many2one('res.currency', default=_get_default_currency_id)

    x_aa_av_sale_order_id = fields.Many2one('sale.order', string='Sale order')

    x_aa_av_sequence = fields.Integer(string='Sequence')
    x_aa_av_vormgroep = fields.Selection(
        [('1', 'Vormgroep 1'), ('2', 'Vormgroep 2'), ('3', 'Vormgroep 3'), ('Specials', 'Specials')],
        string='Vormgroep')
    x_aa_av_price = fields.Monetary(string='Extra per m2', currency_field='x_aa_av_currency_id')
    x_aa_av_vormgroep_surface = fields.Integer(string='m2')
    x_aa_av_vormgroep_price_total = fields.Monetary(string='Total vormgroep price',
                                                    currency_field='x_aa_av_currency_id',
                                                    compute='_compute_total_vormgroep_price')

    @api.depends('x_aa_av_vormgroep', 'x_aa_av_price', 'x_aa_av_vormgroep_surface')
    def _compute_total_vormgroep_price(self):
        for rec in self:
            if rec.x_aa_av_price and rec.x_aa_av_vormgroep_surface:
                rec.x_aa_av_vormgroep_price_total = rec.x_aa_av_price * rec.x_aa_av_vormgroep_surface
            else:
                rec.x_aa_av_vormgroep_price_total = 0.0

    @api.onchange('x_aa_av_vormgroep')
    def _onchange_x_aa_av_vormgroep(self):
        if self.x_aa_av_vormgroep:
            if self.x_aa_av_vormgroep == '1':
                self.x_aa_av_price = 0.0
            elif self.x_aa_av_vormgroep == '2':
                self.x_aa_av_price = 1.75
            elif self.x_aa_av_vormgroep == '3':
                self.x_aa_av_price = 2.25
