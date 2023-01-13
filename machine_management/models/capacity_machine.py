# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

import datetime
from odoo import api, exceptions, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DFORMAT


class MachineCapacity(models.Model):
    _name = 'aa.capacity.machine'
    _rec_name = 'aa_name'
    _order = 'aa_date,aa_name'

    aa_name = fields.Char(string='Name')
    aa_resource_id = fields.Many2one('resource.resource', string='Machine')
    aa_date = fields.Date('Date')
    aa_capacity = fields.Float(string='Capacity',
        compute='capacity_from_working_time', store=True)
    aa_remain_capacity = fields.Float(string='Remain Capacity',
        compute='aa_compute_remain_capacity', store=True)
    aa_task_ids = fields.One2many(
        'project.task', 'aa_capacity_machine_id', string='Tasks')
    aa_machine_header = fields.Text('Machine Header')
    aa_machine_info = fields.Text('Machine Info')
    date_from = fields.Date(string='From', default=fields.Date.today())
    date_to = fields.Date(string='To',
        default=datetime.date.today() + datetime.timedelta(days=6))
    aa_plan_only = fields.Boolean(string='Plan Only',
        compute='check_plan_only', store=True)
    aa_progress = fields.Float(string='Progress',
        compute='_compute_progress', store=True)
    aa_html = fields.Html(default='')
    aa_active = fields.Boolean(string='Active')
    aa_prod_time_norm = fields.Float('Production Time Norm')
    aa_prod_time_total_est = fields.Float(string='Production Time Total EST',
        compute='aa_compute_total_time', store=True)
    aa_prod_time_remain = fields.Float(string='Production Time Remain')
    aa_prod_time_surplus = fields.Float(string='Production Time Surplus')

    aa_res_code = fields.Char(related='aa_resource_id.aa_code', store=True)
    aa_machine_group_code = fields.Char(related='aa_resource_id.aa_code',
        string='Machine Group Code')

    aa_parent_capacity = fields.Many2one('aa.capacity.machine',
        string='Parent Capacity')
    aa_locked = fields.Boolean(compute='_compute_progress', store=True)
    aa_zero = fields.Boolean(related="aa_resource_id.aa_zero", store=True)

    # Need to check
    def update_parent_capacities(self, record):
        totalCapacity = 0.0
        childCaps = self.search([('aa_parent_capacity', '=', record.id)])
        if childCaps:
            for childCap in childCaps:
                totalCapacity += childCap.aa_capacity
            record.aa_capacity = totalCapacity
        else:
            minDate = datetime.datetime.combine(record.aa_date, datetime.datetime.min.time())
            maxDate = datetime.datetime.combine(record.aa_date, datetime.datetime.max.time())
            record.aa_capacity = (record.aa_resource_id and
                record.aa_resource_id.calendar_id.get_work_hours_count(minDate, maxDate))

    # Need to check
    @api.depends('aa_resource_id', 'aa_parent_capacity', 'aa_resource_id.calendar_id')
    def capacity_from_working_time(self):
        '''Compute capacity of parent and child capcity machine'''
        for record in self:
            minDate = datetime.datetime.combine(record.aa_date, datetime.datetime.min.time())
            maxDate = datetime.datetime.combine(record.aa_date, datetime.datetime.max.time())
            if record.aa_parent_capacity:
                record.aa_capacity = (record.aa_resource_id and
                    record.aa_resource_id.calendar_id.get_work_hours_count(minDate, maxDate))
            else:
                self.update_parent_capacities(record)

    # Need to check
    def update_remain_parent_capacities(self, record):
        totalRemCapacity = 0.0
        calRecRemCap = 0.0
        childCaps = self.search([('aa_parent_capacity', '=', record.id)])
        if childCaps:
            for childCap in childCaps:
                if childCap.aa_remain_capacity == 0.0:
                    calRecRemCap = childCap.aa_capacity - childCap.aa_prod_time_total_est
                totalRemCapacity += childCap.aa_remain_capacity
            record.aa_remain_capacity = (totalRemCapacity + calRecRemCap) - record.aa_prod_time_total_est
        else:
            record.aa_remain_capacity = record.aa_capacity - record.aa_prod_time_total_est

    # Need to check
    @api.depends('aa_parent_capacity', 'aa_prod_time_total_est', 'aa_capacity')
    def aa_compute_remain_capacity(self):
        for record in self:
            if record.aa_parent_capacity:
                record.aa_remain_capacity = record.aa_capacity - record.aa_prod_time_total_est
            else:
                self.update_remain_parent_capacities(record)

    # Done
    @api.depends('aa_date')
    def check_plan_only(self):
        for record in self:
            if record.aa_date and record.aa_date.weekday() == 6:
                record.aa_plan_only = True
            else:
                record.aa_plan_only = False

    # Done
    @api.depends('aa_capacity', 'aa_remain_capacity', 'aa_prod_time_total_est')
    def _compute_progress(self):
        for rec in self:
            if rec.aa_capacity > 0:
                if rec.aa_prod_time_total_est > rec.aa_capacity:
                    rec.write({
                        'aa_progress':100.0,
                        'aa_locked':True
                        })
                else:
                    rec.aa_progress = round(
                        100.0 * (rec.aa_capacity - rec.aa_remain_capacity)\
                         / rec.aa_capacity, 2)
            else:
                rec.aa_progress = 0.0

    # Need to improve
    @api.onchange('date_from', 'date_to')
    def aa_onchange_dates(self):
        # res = {}
        # if (not self.date_from) or (not self.date_to):
        #     return res
        if self.date_from or self.date_to:
            aa_machines = self.search([
                ('aa_date', '>', self.date_from), ('aa_date', '<', self.date_to)])
            self.aa_machine_header = str([{'header': aa_machines.mapped('aa_name')}])
            aa_all_machine_details = {}
            for aa_machine in aa_machines:
                aa_machineId = aa_machine.id
                aa_all_machine_details.setdefault(aa_machineId, {
                    'name': aa_machine.aa_resource_id.name,
                    'id': aa_machineId,
                    # 'noOfDays': dateRange.days+1,
                    'noOfDays': len(aa_machines),
                    'progress': aa_machine.aa_progress})
            aa_all_machine_details = aa_all_machine_details.values()
            aa_sorted_all_machine_detail = sorted(
                aa_all_machine_details,
                key=lambda x: x['name'], reverse=True)
            # self.aa_machine_header = str(aa_date_header)
            self.aa_machine_info = str(aa_sorted_all_machine_detail)
        # return res

    # Done
    @api.depends('aa_task_ids', 'aa_task_ids.aa_production_time_count')
    def aa_compute_total_time(self):
        for record in self:
            record.aa_prod_time_total_est = round(
                sum(record.aa_task_ids.mapped('aa_production_time_count')), 2)

    # Done
    def aa_join_name_date(self, aa_name, date, aa_plan_only):
        aa_nameContent = aa_name[:2] + aa_name[-1:]
        aa_weekDay = ['MA', 'DI', 'WO', 'DO', 'VR', 'ZA', 'ZO']
        if aa_plan_only == True:
            return aa_nameContent.upper() + ' ' + date.strftime('%d-%m/') + 'PLAN'
        else:
            return aa_nameContent.upper() + ' ' + date.strftime('%d-%m/%W') + aa_weekDay[date.weekday()]

    # Done
    @api.model
    def create(self, vals):
        res = super(MachineCapacity, self).create(vals)
        if res.aa_date and res.aa_resource_id:
            res.aa_name = self.aa_join_name_date(
                res.aa_resource_id.name, res.aa_date, res.aa_plan_only)
        task = self.env['project.task'].create({
                'name': 'STARTUP',
                'aa_resource_id': res.aa_resource_id.id,
                'aa_capacity_machine_id': res.id,
                'project_id': self.env.ref('machine_management.production_project').id,
                'aa_freeze': True,
                'aa_startup':True})
        return res


    # Done
    def write(self, vals):
        aa_resource = self.env['resource.resource']
        aa_date = (datetime.datetime.strptime(vals.get('aa_date'), DFORMAT)
            if vals.get('aa_date') else self.aa_date)
        aa_res =  (aa_resource.browse(vals.get('aa_resource_id'))
            if vals.get('aa_resource_id') else self.aa_resource_id)
        aa_plan = (vals.get('aa_plan_only')
            if vals.get('aa_plan_only') in [True, False] else self.aa_plan_only)
        if (vals.get('aa_plan_only') in [True, False] or
            vals.get('aa_resource_id') or vals.get('aa_date')):
            self.aa_name = self.aa_join_name_date(aa_res.name, aa_date, aa_plan)
        return super(MachineCapacity, self).write(vals)
