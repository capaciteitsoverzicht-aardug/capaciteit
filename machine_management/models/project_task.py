# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from datetime import date, datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MachineProjectTask(models.Model):
    _inherit = 'project.task'
    _order = 'aa_startup desc'

    aa_production_start_time = fields.Datetime('Production Start Time')
    aa_production_end_time = fields.Datetime('Production End Time')
    aa_production_time_count = fields.Float('Production Time')
    aa_capacity_machine_id = fields.Many2one('aa.capacity.machine',
        string='Capacity Machine')
    aa_resource_id = fields.Many2one('resource.resource', string='Machine',
        readonly=True)
    aa_production_state = fields.Selection([
        ('done', 'Done'),('blocked', 'Blocked')], string='Production State')
    aa_capacity_machine_id_old = fields.Many2one('aa.capacity.machine',
        string='Capacity Machine Old')
    aa_quantity = fields.Float(string='Quantity')
    aa_html = fields.Html()
    # aa_kanban_line = fields.Html(compute='_get_sale_order_lines')
    aa_startup = fields.Boolean(string='aa_startup', readonly=True)
    aa_freeze = fields.Boolean(string='aa_freeze')
    aa_progress_bar = fields.Float(related='aa_capacity_machine_id.aa_progress',
        string=' ', store=True)
    aa_capacity_date = fields.Date(related='aa_capacity_machine_id.aa_date', store=True)
    aa_kanban_color = fields.Char(compute='_compute_color')
    aa_related_remain_capacity = fields.Float(related='aa_capacity_machine_id.aa_remain_capacity')
    aa_task_count = fields.Integer(related='sale_order_id.tasks_count')
    x_aa_av_project_description = fields.Char(related='sale_order_id.x_aa_av_project_description')
    aa_bug = fields.Boolean(string='Is Bug')
    aa_lock = fields.Boolean(string='Is Lock')
    is_production_done = fields.Boolean(string='Is Production Done')
    # aa_default_code = fields.Char(related='sale_line_id.product_id.default_code')

    @api.model
    def aa_action_normal_machines(self, recordDate):
        view = self.env.ref('machine_management.view_task_dashboard_kanban')
        formView = self.env.ref('project.view_task_form2')
        date = recordDate.split('|')[1].split(' ')[0]
        machine = recordDate.split('|')[0][:-1]
        formetedDate = datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')
        action = {'type': 'ir.actions.act_window',
                  'name': 'Show Machine',
                  'res_model': 'project.task',
                  'views': [[view.id, 'kanban'], [formView.id, 'form']],
                  'domain':[['aa_capacity_date','=',formetedDate],
                            ['aa_capacity_machine_id.aa_machine_group_code','ilike', machine]],
                  'view_id': view.id,
                  'search_view_id': self.env.ref('machine_management.aa_view_task_dashboard_search').id,
                  'context': {'group_by':'aa_capacity_machine_id'}}
        return action

    # @api.depends('sale_order_id', 'sale_order_id.order_line')
    # def _get_sale_order_lines(self):
    #     '''planning task and group set in html field to disply in kanban'''
    #     aa_productionProject = self.env.ref('machine_management.production_project')
    #     for rec in self:
    #         if rec.sale_order_id:
    #             recordList = ''
    #             for line in rec.sale_order_id.order_line:
    #                 if line.product_id.project_id.id == aa_productionProject.id and line.task_id:
    #                     recordList +=  line.task_id.name +'<br/>'
    #             rec.aa_kanban_line = recordList
    #         else:
    #             rec.aa_kanban_line = False

    def _compute_color(self):
        for rec in self:
            if rec.aa_resource_id.aa_zero:
                rec.aa_kanban_color = 'aa_zero_machine_card_color'
            else:
                rec.aa_kanban_color = 'aa_other_machine_card_color'

    def write(self, vals):
        res = super(MachineProjectTask, self).write(vals)
        if vals.get('aa_capacity_machine_id'):
            if self.aa_freeze == True:
                raise ValidationError('\
                    Unable to move.')
            capacity = self.env['aa.capacity.machine'].browse(
                vals.get('aa_capacity_machine_id'))
            orderLine = (self.env['sale.order.line'].browse(
                vals.get('sale_line_id')) if vals.get(
                'sale_line_id') else self.sale_line_id)
            if orderLine:
                orderLine.write({'aa_capacity_machine_id':capacity.id,
                    'aa_resource_id':capacity.aa_resource_id.id})
                self.write({'aa_resource_id':capacity.aa_resource_id.id,
                    'aa_capacity_machine_id_old':self.aa_capacity_machine_id.id})
        return super(MachineProjectTask, self).write(vals)
