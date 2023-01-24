# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, fields, models
from odoo.tools import float_round


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_aa_av_uitvoeringsperiode = fields.Char(string='Aangeboden uitvoeringsperiode')

    # Other Info / Files
    x_aa_av_tekla_bestand_1 = fields.Binary('Tekla file 1')
    x_aa_av_tekla_bestand_2 = fields.Binary('Tekla file 2')

    # Calculation / Project Information
    x_aa_av_pro_manager_id = fields.Many2one('res.users', 'Project manager')
    x_aa_av_order_name = fields.Char(string='Customer Order name')
    x_aa_av_project_description = fields.Char(string='Order Description')
    x_aa_av_layers = fields.Selection([('1', '1'), ('2', '2')], string='Layers', default='1')
    x_aa_av_pre_treatment = fields.Char(string='Pre-treatment', default='SA 2,5')
    x_aa_av_corrosivity = fields.Selection([('c1', 'C1'), ('c2', 'C2'), ('c3', 'C3'), ('c4', 'C4'), ('c5', 'C5')],
                                           string='Corrosivity')
    x_aa_av_layer_1 = fields.Char(string='Layer 1 title', compute='_compute_layer_1_title')
    x_aa_av_layer_2 = fields.Char(string='Layer 2 title', compute='_compute_layer_2_title')
    x_aa_av_layer1_thickness = fields.Integer(string='Thickness')
    x_aa_av_layer2_thickness = fields.Integer(string='Thickness layer 2')
    x_aa_av_surface = fields.Integer(string='Surface')
    x_aa_av_tonnage = fields.Integer(string='Tonnage')

    # Calculation / Color
    x_aa_av_color_layer_1_id = fields.Many2one('product.product', string='Color layer 1', tracking=True)
    x_aa_av_color_layer_2_id = fields.Many2one('product.product', string='Color layer 2', tracking=True)
    x_aa_av_color_product_template_id = fields.Many2one(related='x_aa_av_color_layer_1_id.product_tmpl_id')
    x_aa_av_color_group = fields.Many2one(related='x_aa_av_color_layer_1_id.categ_id', string='Kleurgroep 1')
    x_aa_av_color_group_price_m2 = fields.Monetary(string='Color group price m2', currency_field='currency_id',
                                                   compute='_compute_color_group_price')
    x_aa_av_total_color_group_price = fields.Monetary(string='Total color group price', currency_field='currency_id',
                                                      compute='_compute_total_color_group_price')
    x_aa_av_color_group_layer_2 = fields.Many2one(related='x_aa_av_color_layer_2_id.categ_id', string='Kleurgroep 2')

    # Calculation / Vormgroep
    x_aa_av_vormgroep_ids = fields.One2many('ansova.vormgroep', 'x_aa_av_sale_order_id', string='Vormgroepen')
    x_aa_av_vormgroep_price_total = fields.Monetary(string='Total vormgroep price', currency_field='currency_id',
                                                    compute='_compute_total_vormgroep_price')

    x_aa_av_vormgroep_1 = fields.Many2one('ansova.vormgroep', string='Vormgroep 1', compute='_compute_vormgroep_fields', store=True)
    x_aa_av_vormgroep_1_price = fields.Monetary(related='x_aa_av_vormgroep_1.x_aa_av_price')
    x_aa_av_vormgroep_1_surface = fields.Integer(string='Vormgroep 1 surface', compute='_compute_vormgroep_fields')
    x_aa_av_vormgroep_1_total_price = fields.Monetary(related='x_aa_av_vormgroep_1.x_aa_av_vormgroep_price_total')

    x_aa_av_vormgroep_2 = fields.Many2one('ansova.vormgroep', string='Vormgroep 2', compute='_compute_vormgroep_fields', store=True)
    x_aa_av_vormgroep_2_price = fields.Monetary(related='x_aa_av_vormgroep_2.x_aa_av_price')
    x_aa_av_vormgroep_2_surface = fields.Integer(string='Vormgroep 2 surface', compute='_compute_vormgroep_fields')
    x_aa_av_vormgroep_2_total_price = fields.Monetary(related='x_aa_av_vormgroep_2.x_aa_av_vormgroep_price_total')

    x_aa_av_vormgroep_3 = fields.Many2one('ansova.vormgroep', string='Vormgroep 3', compute='_compute_vormgroep_fields', store=True)
    x_aa_av_vormgroep_3_price = fields.Monetary(related='x_aa_av_vormgroep_3.x_aa_av_price')
    x_aa_av_vormgroep_3_surface = fields.Integer(string='Vormgroep 3 surface', compute='_compute_vormgroep_fields')
    x_aa_av_vormgroep_3_total_price = fields.Monetary(related='x_aa_av_vormgroep_3.x_aa_av_vormgroep_price_total')

    x_aa_av_vormgroep_4 = fields.Many2one('ansova.vormgroep', string='Vormgroep 4', compute='_compute_vormgroep_fields', store=True)
    x_aa_av_vormgroep_4_price = fields.Monetary(related='x_aa_av_vormgroep_4.x_aa_av_price')
    x_aa_av_vormgroep_4_surface = fields.Integer(string='Vormgroep 4 surface', compute='_compute_vormgroep_fields')
    x_aa_av_vormgroep_4_total_price = fields.Monetary(related='x_aa_av_vormgroep_4.x_aa_av_vormgroep_price_total')

    # Calculation / Delengroep
    x_aa_av_delengroep_id = fields.Many2one('ansova.delengroep', string='Delengroep')
    x_aa_av_extra_per_delengroep = fields.Monetary(related='x_aa_av_delengroep_id.x_aa_av_price')
    x_aa_av_delengroep_price_total = fields.Monetary(string='Total delengroep price', currency_field='currency_id',
                                                     compute='_compute_total_delengroep_price')

    # Calculation / Kraanbanen
    x_aa_av_kraanbanen_price = fields.Monetary(string='Kraanbanen afplakken', currency_field='currency_id',
                                               default=1.25)
    x_aa_av_kraanbanen_surface = fields.Integer(string='Kraanbanen surface')
    x_aa_av_kraanbanen_price_total = fields.Monetary(string='Total kraanbanen price', currency_field='currency_id',
                                                     compute='_compute_total_kraanbanen_price')

    # Calculation / Kleurwissels
    x_aa_av_kleurwissels_price = fields.Monetary(string='Kleurwissels', currency_field='currency_id', default=225.0)
    x_aa_av_kleurwissels_amount = fields.Integer(string='Aantal kleurwissels')
    x_aa_av_kleurwissels_price_total = fields.Monetary(string='Total kleurwissels price', currency_field='currency_id',
                                                       compute='_compute_total_kleurwissels_price')

    # Calculation / Base Price
    x_aa_av_base_price = fields.Monetary(string='Base Price', currency_field='currency_id')
    x_aa_av_total_base_price = fields.Monetary(string='Total Base Price', currency_field='currency_id',
                                               compute='_compute_total_base_price')

    x_aa_av_discount = fields.Monetary(string='Discount per m2', currency_field='currency_id')
    x_aa_av_net_discount = fields.Monetary(string='Extra discount', currency_field='currency_id')

    # Calculation / Pricing
    x_aa_av_subtotal_total = fields.Monetary(string='Gross total', currency_field='currency_id',
                                             compute='_compute_x_aa_av_subtotal_total')
    x_aa_av_gross_price_per_m2 = fields.Monetary(string='Price per m2', currency_field='currency_id',
                                                 compute='_compute_x_aa_av_gross_price_per_m2')

    x_aa_av_net_price = fields.Monetary(string='Net project price per m2', currency_field='currency_id',
                                        compute='_compute_x_aa_av_net_price')
    x_aa_av_net_price_total = fields.Monetary(string='Net price total', currency_field='currency_id', compute='_compute_x_aa_av_net_price')

    # CRM
    x_aa_av_transport = fields.Selection([('client', 'Client'),
                                          ('ansova', 'Ansova')], string='Transport', tracking=True)
    x_aa_av_location_id = fields.Many2one('ansova.location', string='Location', tracking=True)
    x_aa_av_project_leader_id = fields.Many2one(related='x_aa_av_location_id.x_aa_av_project_leader_id')
    x_aa_av_project_leader_phone = fields.Char(related='x_aa_av_location_id.x_aa_av_project_leader_phone')
    x_aa_av_street = fields.Char(related='x_aa_av_location_id.x_aa_av_street')
    x_aa_av_zip = fields.Char(related='x_aa_av_location_id.x_aa_av_zip')
    x_aa_av_city = fields.Char(related='x_aa_av_location_id.x_aa_av_city')
    x_aa_av_state_id = fields.Many2one(related='x_aa_av_location_id.x_aa_av_state_id')
    x_aa_av_country_id = fields.Many2one(related='x_aa_av_location_id.x_aa_av_country_id')

    @api.onchange('x_aa_av_layers')
    def change_x_aa_av_layers(self):
        if self.x_aa_av_layers == '1':
            self.x_aa_av_layer_2 = ' '

    @api.depends('x_aa_av_layer1_thickness', 'x_aa_av_color_layer_1_id')
    def _compute_layer_1_title(self):
        for rec in self:
            if rec.x_aa_av_color_layer_1_id and rec.x_aa_av_color_layer_1_id.x_aa_av_layer_title:
                rec.x_aa_av_layer_1 = rec.x_aa_av_color_layer_1_id.x_aa_av_layer_title + ' ' + str(
                    rec.x_aa_av_layer1_thickness) + ' MU ' + rec.x_aa_av_color_layer_1_id.name
            else:
                rec.x_aa_av_layer_1 = ''

    @api.depends('x_aa_av_layer2_thickness', 'x_aa_av_color_layer_2_id')
    def _compute_layer_2_title(self):
        for rec in self:
            if rec.x_aa_av_color_layer_2_id and rec.x_aa_av_color_layer_2_id.x_aa_av_layer_title:
                rec.x_aa_av_layer_2 = rec.x_aa_av_color_layer_2_id.x_aa_av_layer_title + ' ' + str(
                    rec.x_aa_av_layer2_thickness) + ' MU ' + rec.x_aa_av_color_layer_2_id.name
            else:
                rec.x_aa_av_layer_2 = ''

    @api.depends('x_aa_av_vormgroep_ids')
    def _compute_vormgroep_fields(self):
        for rec in self:
            vormgroep_1 = False
            vormgroep_1_surface = 0.0
            vormgroep_2 = False
            vormgroep_2_surface = 0.0
            vormgroep_3 = False
            vormgroep_3_surface = 0.0
            vormgroep_4 = False
            vormgroep_4_surface = 0.0
            if rec.x_aa_av_vormgroep_ids:
                for vormgroep in rec.x_aa_av_vormgroep_ids:
                    if vormgroep.x_aa_av_vormgroep == '1':
                        vormgroep_1 = vormgroep.id
                        vormgroep_1_surface = vormgroep.x_aa_av_vormgroep_surface
                    elif vormgroep.x_aa_av_vormgroep == '2':
                        vormgroep_2 = vormgroep.id
                        vormgroep_2_surface = vormgroep.x_aa_av_vormgroep_surface
                    elif vormgroep.x_aa_av_vormgroep == '3':
                        vormgroep_3 = vormgroep.id
                        vormgroep_3_surface = vormgroep.x_aa_av_vormgroep_surface
                    elif vormgroep.x_aa_av_vormgroep == 'Specials':
                        vormgroep_4 = vormgroep.id
                        vormgroep_4_surface = vormgroep.x_aa_av_vormgroep_surface

            rec.x_aa_av_vormgroep_1 = vormgroep_1
            rec.x_aa_av_vormgroep_1_surface = vormgroep_1_surface
            rec.x_aa_av_vormgroep_2 = vormgroep_2
            rec.x_aa_av_vormgroep_2_surface = vormgroep_2_surface
            rec.x_aa_av_vormgroep_3 = vormgroep_3
            rec.x_aa_av_vormgroep_3_surface = vormgroep_3_surface
            rec.x_aa_av_vormgroep_4 = vormgroep_4
            rec.x_aa_av_vormgroep_4_surface = vormgroep_4_surface

    @api.depends('x_aa_av_base_price', 'x_aa_av_surface')
    def _compute_total_base_price(self):
        for rec in self:
            if rec.x_aa_av_base_price and rec.x_aa_av_surface:
                rec.x_aa_av_total_base_price = rec.x_aa_av_base_price * rec.x_aa_av_surface
            else:
                rec.x_aa_av_total_base_price = 0.0

    @api.depends('x_aa_av_color_group')
    def _compute_color_group_price(self):
        for rec in self:
            if rec.x_aa_av_color_group:
                rec.x_aa_av_color_group_price_m2 = rec.x_aa_av_color_group.x_aa_av_price_m2
            else:
                rec.x_aa_av_color_group_price_m2 = 0.0

    @api.depends('x_aa_av_color_group_price_m2', 'x_aa_av_surface')
    def _compute_total_color_group_price(self):
        for rec in self:
            if rec.x_aa_av_color_group_price_m2 and rec.x_aa_av_surface:
                rec.x_aa_av_total_color_group_price = rec.x_aa_av_color_group_price_m2 * rec.x_aa_av_surface
            else:
                rec.x_aa_av_total_color_group_price = 0.0

    @api.depends('x_aa_av_vormgroep_ids', 'x_aa_av_vormgroep_ids.x_aa_av_vormgroep_price_total')
    def _compute_total_vormgroep_price(self):
        for rec in self:
            vormgroep_total = 0.0
            for vormgroep in rec.x_aa_av_vormgroep_ids:
                if vormgroep.x_aa_av_vormgroep_price_total:
                    vormgroep_total += vormgroep.x_aa_av_vormgroep_price_total
            rec.x_aa_av_vormgroep_price_total = vormgroep_total

    @api.depends('x_aa_av_extra_per_delengroep', 'x_aa_av_delengroep_id')
    def _compute_total_delengroep_price(self):
        for rec in self:
            if rec.x_aa_av_extra_per_delengroep and rec.x_aa_av_surface:
                rec.x_aa_av_delengroep_price_total = rec.x_aa_av_extra_per_delengroep * rec.x_aa_av_surface
            else:
                rec.x_aa_av_delengroep_price_total = 0.0

    @api.depends('x_aa_av_kraanbanen_price', 'x_aa_av_kraanbanen_surface')
    def _compute_total_kraanbanen_price(self):
        for rec in self:
            if rec.x_aa_av_kraanbanen_price and rec.x_aa_av_kraanbanen_surface:
                rec.x_aa_av_kraanbanen_price_total = rec.x_aa_av_kraanbanen_price * rec.x_aa_av_kraanbanen_surface
            else:
                rec.x_aa_av_kraanbanen_price_total = 0.0

    @api.depends('x_aa_av_kleurwissels_price', 'x_aa_av_kleurwissels_amount')
    def _compute_total_kleurwissels_price(self):
        for rec in self:
            if rec.x_aa_av_kleurwissels_price and rec.x_aa_av_kleurwissels_amount:
                rec.x_aa_av_kleurwissels_price_total = rec.x_aa_av_kleurwissels_price * rec.x_aa_av_kleurwissels_amount
            else:
                rec.x_aa_av_kleurwissels_price_total = 0.0

    @api.depends('x_aa_av_total_base_price', 'x_aa_av_total_color_group_price', 'x_aa_av_vormgroep_price_total',
                 'x_aa_av_delengroep_price_total', 'x_aa_av_kraanbanen_price_total', 'x_aa_av_kleurwissels_price_total')
    def _compute_x_aa_av_subtotal_total(self):
        for rec in self:
            rec.x_aa_av_subtotal_total = sum(
                [rec.x_aa_av_total_base_price, rec.x_aa_av_total_color_group_price, rec.x_aa_av_vormgroep_price_total,
                 rec.x_aa_av_delengroep_price_total, rec.x_aa_av_kraanbanen_price_total,
                 rec.x_aa_av_kleurwissels_price_total])

    @api.depends('x_aa_av_subtotal_total', 'x_aa_av_surface')
    def _compute_x_aa_av_gross_price_per_m2(self):
        for rec in self:
            if rec.x_aa_av_surface:
                rec.x_aa_av_gross_price_per_m2 = float_round(rec.x_aa_av_subtotal_total / rec.x_aa_av_surface, 2)
            else:
                rec.x_aa_av_gross_price_per_m2 = 0.0

    @api.depends('x_aa_av_gross_price_per_m2', 'x_aa_av_subtotal_total', 'x_aa_av_discount', 'x_aa_av_surface', 'x_aa_av_net_discount')
    def _compute_x_aa_av_net_price(self):
        for rec in self:
            if rec.x_aa_av_gross_price_per_m2 and (rec.x_aa_av_discount or rec.x_aa_av_net_discount):
                rec.x_aa_av_net_price = rec.x_aa_av_gross_price_per_m2 - rec.x_aa_av_discount
                rec.x_aa_av_net_price_total = ((rec.x_aa_av_gross_price_per_m2 - rec.x_aa_av_discount) * rec.x_aa_av_surface) - rec.x_aa_av_net_discount
            else:
                rec.x_aa_av_net_price = rec.x_aa_av_gross_price_per_m2
                rec.x_aa_av_net_price_total = rec.x_aa_av_subtotal_total
