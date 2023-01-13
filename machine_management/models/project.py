# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models


class MachineProject(models.Model):
    _inherit = 'project.project'

    aa_project_type = fields.Selection(
        [('production', 'Production'), ('purchasing', 'Purchasing'),
         ('studio', 'Studio'), ('pre_process', 'Pre Process')],
        string='Project Type')

    # def _compute_task_count(self):
    #     res = super(MachineProject, self)._compute_task_count()
    #     fields = ['project_id', 'display_project_id:count']
    #     groupby = ['project_id']
    #     for project in self:
    #         if project.id == self.env.ref('machine_management.production_project').id:
    #             domain = [('project_id', '=', project.id), ('aa_startup', '=', False),
    #             '|',('stage_id.fold', '=', False), ('stage_id', '=', False)]
    #             task_data = self.env['project.task']._read_group(domain, fields, groupby)
    #             if task_data:
    #                 project.task_count = task_data[0]['project_id_count']
    #             else:
    #                 project.task_count = 0
    #     return res
