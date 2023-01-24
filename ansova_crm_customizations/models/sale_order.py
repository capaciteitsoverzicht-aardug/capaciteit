# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################
from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_aa_av_mu_id = fields.Many2one('ansova.mu', string='Tickness in MU', tracking=True)
    x_aa_av_system = fields.Selection([('no_primer', 'No Primer'),
                                       ('with_primer', 'With Primer')], string='System', tracking=True)
    x_aa_av_uv_resistant = fields.Boolean(string='UV Resistant', tracking=True)

    x_aa_av_total_kilos = fields.Float(string='Amount of steel (kilo)', compute='_compute_kilos_steel')
    x_aa_av_parts = fields.Integer(string='Amount of parts per ton', default=0, tracking=True)
    x_aa_av_connected_parts = fields.Boolean(string='Connected parts', tracking=True)
    x_aa_av_grams_amount = fields.Float(string='Product amount (gram)', compute='_compute_product_amount')
    x_aa_av_product_kilo_amount = fields.Float(string='Product amount (kilo)', compute='_compute_product_amount')

    @api.depends('x_aa_av_mu_id', 'x_aa_av_mu_id.x_aa_av_mu_m2', 'x_aa_av_mu_id.x_aa_av_grams',
                 'x_aa_av_surface')
    def _compute_product_amount(self):
        for rec in self:
            if not rec.x_aa_av_mu_id:
                rec.x_aa_av_grams_amount = 0.0
                rec.x_aa_av_product_kilo_amount = 0.0
            else:
                rec.x_aa_av_grams_amount = rec.x_aa_av_surface * rec.x_aa_av_mu_id.x_aa_av_grams
                rec.x_aa_av_product_kilo_amount = (rec.x_aa_av_surface * rec.x_aa_av_mu_id.x_aa_av_grams) / 1000

    @api.depends('x_aa_av_tonnage')
    def _compute_kilos_steel(self):
        for rec in self:
            rec.x_aa_av_total_kilos = rec.x_aa_av_tonnage * 1000

    @api.onchange('x_aa_av_color_layer_1_id')
    def _onchange_color_product_id(self):
        if self.x_aa_av_color_layer_1_id:
            if self.x_aa_av_color_layer_1_id.x_aa_av_mu_ids and self.x_aa_av_mu_id:
                if self.x_aa_av_mu_id.id in self.x_aa_av_color_layer_1_id.x_aa_av_mu_ids.ids:
                    return
        self.x_aa_av_mu_id = False

    @api.onchange('x_aa_av_mu_id')
    def _onchange_mu_id(self):
        if not self.x_aa_av_mu_id:
            self.x_aa_av_layer1_thickness = 0
        else:
            self.x_aa_av_layer1_thickness = self.x_aa_av_mu_id.x_aa_av_mu_m2
