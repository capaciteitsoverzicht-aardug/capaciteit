# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################
from odoo import api, models, fields


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    x_aa_av_color_product_id = fields.Many2one('product.product', string='Color')
    x_aa_av_color_product_template_id = fields.Many2one(related='x_aa_av_color_product_id.product_tmpl_id')
    x_aa_av_mu_id = fields.Many2one('ansova.mu', string='Tickness in MU')
    x_aa_av_system = fields.Selection([('no_primer', 'No Primer'),
                                       ('with_primer', 'With Primer')], string='System')
    x_aa_av_uv_resistant = fields.Boolean(string='UV Resistant')

    x_aa_av_order_name = fields.Char(string='Customer Order name')
    x_aa_av_project_description = fields.Char(string='Order Description')
    x_aa_av_total_kilos = fields.Integer(string='Amount of steel (kilo)', compute='_compute_kilos_steel')
    x_aa_av_tons_steel = fields.Integer(string='Tonnage', default=0)
    x_aa_av_parts = fields.Integer(string='Amount of parts per ton', default=0)
    x_aa_av_connected_parts = fields.Boolean(string='Connected parts')
    x_aa_av_surface_estimate = fields.Float(string='Surface estimate (m2)')
    x_aa_av_mu_amount = fields.Integer(string='Amount of MU', compute='_compute_product_amount')
    x_aa_av_grams_amount = fields.Float(string='Product amount (gram)', compute='_compute_product_amount')
    x_aa_av_product_kilo_amount = fields.Float(string='Product amount (kilo)', compute='_compute_product_amount')

    x_aa_av_transport = fields.Selection([('client', 'Client'),
                                          ('ansova', 'Ansova')], string='Transport')
    x_aa_av_location_id = fields.Many2one('ansova.location', string='Location')
    x_aa_av_street = fields.Char(related='x_aa_av_location_id.x_aa_av_street')
    x_aa_av_zip = fields.Char(related='x_aa_av_location_id.x_aa_av_zip')
    x_aa_av_city = fields.Char(related='x_aa_av_location_id.x_aa_av_city')
    x_aa_av_state_id = fields.Many2one(related='x_aa_av_location_id.x_aa_av_state_id')
    x_aa_av_country_id = fields.Many2one(related='x_aa_av_location_id.x_aa_av_country_id')

    @api.depends('x_aa_av_mu_id', 'x_aa_av_mu_id.x_aa_av_mu_m2', 'x_aa_av_mu_id.x_aa_av_grams',
                 'x_aa_av_surface_estimate')
    def _compute_product_amount(self):
        for rec in self:
            if not rec.x_aa_av_mu_id:
                rec.x_aa_av_mu_amount = 0
                rec.x_aa_av_grams_amount = 0.0
                rec.x_aa_av_product_kilo_amount = 0.0
            else:
                rec.x_aa_av_mu_amount = rec.x_aa_av_mu_id.x_aa_av_mu_m2
                rec.x_aa_av_grams_amount = rec.x_aa_av_surface_estimate * rec.x_aa_av_mu_id.x_aa_av_grams
                rec.x_aa_av_product_kilo_amount = (rec.x_aa_av_surface_estimate * rec.x_aa_av_mu_id.x_aa_av_grams) / 1000

    @api.depends('x_aa_av_tons_steel')
    def _compute_kilos_steel(self):
        for rec in self:
            rec.x_aa_av_total_kilos = rec.x_aa_av_tons_steel * 1000

    @api.onchange('x_aa_av_color_product_id')
    def _onchange_color_product_id(self):
        self.x_aa_av_mu_id = False

    def _prepare_opportunity_quotation_context(self):
        context = super(CrmLead, self)._prepare_opportunity_quotation_context()
        context.update({
            'default_x_aa_av_color_layer_1_id': self.x_aa_av_color_product_id.id,
            'default_x_aa_av_mu_id': self.x_aa_av_mu_id.id,
            'default_x_aa_av_layer1_thickness': self.x_aa_av_mu_amount,
            'default_x_aa_av_system': self.x_aa_av_system,
            'default_x_aa_av_uv_resistant': self.x_aa_av_uv_resistant,
            'default_x_aa_av_tonnage': self.x_aa_av_tons_steel,
            'default_x_aa_av_order_name': self.x_aa_av_order_name,
            'default_x_aa_av_project_description': self.x_aa_av_project_description,
            'default_x_aa_av_parts': self.x_aa_av_parts,
            'default_x_aa_av_connected_parts': self.x_aa_av_connected_parts,
            'default_x_aa_av_surface': self.x_aa_av_surface_estimate,
            'default_x_aa_av_location_id': self.x_aa_av_location_id.id,
            'default_x_aa_av_transport': self.x_aa_av_transport,
        })
        return context
