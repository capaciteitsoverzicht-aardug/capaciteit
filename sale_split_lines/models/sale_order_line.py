# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    x_aa_av_scheduled_date = fields.Datetime('Schedule Date')
    x_aa_av_surface = fields.Integer(string='Oppervlakte (m2) per vracht')
    x_aa_av_tonnage = fields.Integer(string='Tonnage per vracht')

    def _timesheet_create_task(self, project):
        '''overload base method to update some task info'''
        res = super(SaleOrderLine, self)._timesheet_create_task(project)
        if self.x_aa_av_scheduled_date:
            for rec in res:
                rec.write({
                    'date_deadline': self.x_aa_av_scheduled_date.date(),
                    'date_assign': self.x_aa_av_scheduled_date.replace(
                        hour=9, minute=0, second=0),
                    'planned_date_begin': self.x_aa_av_scheduled_date.replace(
                        hour=9, minute=0, second=0),
                    'planned_date_end': self.x_aa_av_scheduled_date.replace(
                        hour=10, minute=0, second=0),
                    'working_hours_open': float(9.0),
                    'working_hours_close': float(10.0),

                    'x_aa_av_order_name': self.order_id.x_aa_av_order_name,
                    'x_aa_av_project_description': self.order_id.x_aa_av_project_description,
                    'x_aa_av_tonnage': self.x_aa_av_tonnage,
                    'x_aa_av_conservering': self.order_id.x_aa_av_layer_1,
                    'x_aa_av_surface': self.x_aa_av_surface,
                    'x_aa_av_color_product_id': self.order_id.x_aa_av_color_layer_1_id.id,
                    'x_aa_av_transport': self.order_id.x_aa_av_transport,
                    'x_aa_av_poader': self.order_id.x_aa_av_poader
                })
        return res
