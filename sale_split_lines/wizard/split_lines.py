# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models
from datetime import timedelta


class SaleSplitLine(models.TransientModel):
    _name = 'sale.split.line'
    _description = 'SO Split Line'

    x_aa_av_number_of_lines = fields.Integer('Number of Lines')
    x_aa_av_number_of_delivery = fields.Integer('Amount of deliveries',
                                                default=1)
    x_aa_av_delivery_date = fields.Datetime('Start Date')
    x_aa_av_surface = fields.Integer(string='Totaal Oppervlakte (m2)',
        default=lambda self: self.env['sale.order'].browse(self._context.get(
            'active_id')).x_aa_av_surface if self._context.get('active_id') else 0)
    x_aa_av_tonnage = fields.Integer(string='Totaal Tonnage',
        default=lambda self: self.env['sale.order'].browse(self._context.get(
            'active_id')).x_aa_av_tonnage if self._context.get('active_id') else 0)
    x_aa_av_order_line_ids = fields.Many2many(
        'sale.order.line',
        string='Order Lines'
    )

    def action_split_line(self):
        '''on button click split line based on date and
        delivery qty and number of lines.
        skip schedule date'''
        saleline = self.env['sale.order.line']
        if self.x_aa_av_number_of_lines > 0:
            for line in self.x_aa_av_order_line_ids:
                count = 0
                scheduled_date = self.x_aa_av_delivery_date
                for no in range(self.x_aa_av_number_of_lines):
                    saleline.create({
                        'order_id': self.env.context.get('active_id'),
                        'product_id': line.product_id.id,
                        'name': line.product_id.name + ' ' + str(no + 1),
                        'product_uom_qty': line.product_uom_qty,
                        'price_unit':
                            line.price_unit / self.x_aa_av_number_of_lines,
                        'x_aa_av_scheduled_date': scheduled_date,
                        'x_aa_av_surface': self.x_aa_av_surface / \
                        self.x_aa_av_number_of_lines if self.x_aa_av_surface else 0,
                        'x_aa_av_tonnage': self.x_aa_av_tonnage / \
                        self.x_aa_av_number_of_lines if self.x_aa_av_tonnage else 0,
                    })
                    count += 1
                    if int(count) % int(self.x_aa_av_number_of_delivery) == 0:
                        scheduled_date = \
                            (scheduled_date.weekday() == 4) \
                            and scheduled_date + timedelta(days=3) \
                            or (scheduled_date + timedelta(days=1))
                        count = 0
                line.unlink()
        return True
