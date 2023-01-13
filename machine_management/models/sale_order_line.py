# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    aa_resource_id = fields.Many2one('resource.resource', string='Machine')
    aa_capacity_machine_id = fields.Many2one('aa.capacity.machine',
        string='Uitvoering')
    aa_prod_time_total_est = fields.Float(string='PTI')
    aa_prod_time_total_norm = fields.Float(
        compute='aa_compute_total_production_time',
        string='PTB', store=True)

    @api.depends('product_uom_qty', 'product_id.aa_prod_time_est',
                 'product_id.aa_setup_time_est1', 'product_id.aa_setup_time_est2')
    def aa_compute_total_production_time(self):
        for aa_record in self:
            aa_record.aa_prod_time_total_est =\
                (((aa_record.product_uom_qty * aa_record.product_id.aa_prod_time_est) +
                  aa_record.product_id.aa_setup_time_est1) / 60) / 60
            aa_record.aa_prod_time_total_norm = \
                (((aa_record.product_uom_qty * aa_record.product_id.aa_prod_time_est) +
                  aa_record.product_id.aa_setup_time_est1) / 60) / 60

    @api.onchange('product_id')
    def onchange_product(self):
        self.aa_resource_id = self.product_id.aa_resource_id

    # aa_promised_date > check
    def _timesheet_create_task_prepare_values(self, project):
        res = super(SaleOrderLine, self)._timesheet_create_task_prepare_values(project)
        # state = False
        # if self.aa_prod_time_total_est > 0:
        #     state = 'done'
        res.update({
            'aa_production_time_count': self.aa_prod_time_total_est,
            'aa_resource_id': self.aa_resource_id.id,
            'aa_capacity_machine_id': self.aa_capacity_machine_id.id,
            'aa_production_state': 'done' if self.aa_prod_time_total_est < 0 else False,
            # 'date_deadline': self.order_id.aa_promised_date,
            'date_assign': self.aa_capacity_machine_id.aa_date,
            'aa_quantity': self.product_uom_qty
            })
        return res

    # confirmation_date > Check
    @api.depends('order_id.confirmation_date', 'product_id.aa_product_lead_time')
    def aa_compute_production_date(self):
        for aa_rec in self:
            if aa_rec.order_id.confirmation_date and aa_rec.product_id.aa_product_lead_time:
                aa_rec.aa_production_date = aa_rec.order_id.confirmation_date + datetime.timedelta(
                    minutes=aa_rec.product_id.aa_product_lead_time)

    @api.onchange('aa_capacity_machine_id', 'aa_resource_id')
    def _onchange_cap(self):
        if self._origin.task_id:
            self._origin.task_id.write({
                'aa_capacity_machine_id': self.aa_capacity_machine_id.id,
                'aa_resource_id' : self.aa_resource_id.id})
            self.product_id.write({
                'aa_resource_id' : self.aa_resource_id.id})
