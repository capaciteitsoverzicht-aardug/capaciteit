# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models


class Task(models.Model):
    _inherit = 'project.task'

    x_aa_av_so_stage_color = fields.Integer('Stage Color',
                                            compute='_compute_so_stage_color')

    # Planning / Order
    x_aa_av_order_name = fields.Char(string='Customer Order name') # filled automatically
    x_aa_av_project_description = fields.Char(string='Order Description') # filled automatically
    x_aa_av_tonnage = fields.Integer(string='Tonnage') # filled automatically
    x_aa_av_conservering = fields.Char(string='Conservering') # filled automatically
    x_aa_av_surface = fields.Float(string='Surface') # filled automatically
    x_aa_av_color_product_id = fields.Many2one('product.product', string='Color') # filled automatically

    # Planning / Transport
    x_aa_av_transport_stage = fields.Char(string='Transport stage')
    x_aa_av_components_transport = fields.Integer(string='Amount of components transport')
    x_aa_av_max_transport_length = fields.Float(string='Transport max length')
    x_aa_av_max_transport_width = fields.Float(string='Transport max width')
    x_aa_av_delivery_date = fields.Datetime(string='Delivery date')
    x_aa_av_pickup_date = fields.Datetime(string='Pickup date')
    x_aa_av_transport = fields.Selection([('client', 'Client'),
                                          ('ansova', 'Ansova'),
                                          ('mix', 'Mix Klant Ansova'),
                                          ('other', 'Ansova niet geregeld')], string='Transport') # filled automatically
    x_aa_av_poader = fields.Selection([('order', 'Poeder besteld'),
                                          ('inside', 'Poeder binnen'),
                                          ('other','Voorraad poeder')], string='Poeder', tracking=True)

    def _compute_so_stage_color(self):
        '''Set Blue color code for gantt view when sale order state is
        in plan stage.'''
        for task in self:
            task.x_aa_av_so_stage_color = task.project_color
            if task.sale_line_id \
                    and task.sale_line_id.order_id.state == 'plan':
                task.x_aa_av_so_stage_color = 8
