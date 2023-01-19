# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

import datetime
from odoo import models, fields


class aa_procedures(models.TransientModel):
    _name = 'aa.procedure'

    def aa_create_capacity_machine(self):
        '''create capcitis for 300 days for resources which resource type
           is material and active true'''
        capacity_obj = self.env['aa.capacity.machine']
        startDay = fields.date.today() - datetime.timedelta(days=7)
        lastDate = startDay + datetime.timedelta(days=29)
        resources = self.env['resource.resource'].search(
            [('active', '=', True), ('resource_type', '=', 'material')],
            order='aa_zero desc')
        parentCapacityList = []
        for resource in resources:
            # check direct last day capacity to reduce process time
            lastCapacity = capacity_obj.search(
                [('aa_resource_id', '=', resource.id), ('aa_date', '>=', startDay),
                ('aa_date', '<=', lastDate)], order='id desc', limit=1)
            if lastCapacity:
                remainDays = (lastDate - lastCapacity.aa_date).days
                nextDay = lastCapacity.aa_date + datetime.timedelta(days=1)
            else:
                remainDays = 30
                nextDay = startDay
            for day in range(remainDays):
                parentCapacity = False
                if resource.aa_parent_resource:
                    parentCapacity = capacity_obj.search([
                        ('aa_resource_id', '=', resource.aa_parent_resource.id),
                        ('aa_date', '=', nextDay)], limit=1)
                    parentCapacityList.append(parentCapacity)
                capacity_obj.create({
                    'aa_resource_id': resource.id,
                    'aa_plan_only': False,
                    'aa_date': nextDay,
                    'aa_parent_capacity': parentCapacity and parentCapacity.id})
                nextDay = nextDay + datetime.timedelta(days=1)
        for parentCap in parentCapacityList:
            parentCap.update_zero_capacities()

        #should not be necessary TODO
        #self.env.cr.execute(""" DELETE FROM aa_capacity_machine 
        #                            WHERE aa_resource_id IS NULL;
        #                    """)

        #should not be necessary TODO
        #self.env.cr.execute(""" DELETE FROM project_task 
        #                            WHERE aa_capacity_machine_id IS NULL; 
        #                    """)
        
        #should not be necessary TODO this is not correct for tasks without aa_capacity_machine!!
        #self.env.cr.execute("""
        #                    DELETE FROM aa_capacity_machine where aa_date < '2019-08-01';
        #                    DELETE FROM project_task WHERE date_start < '2019-08-01';
        #                    """)
        self.env.cr.execute("""  UPDATE aa_capacity_machine
                                    SET aa_plan_only = False
                            """)

        self.env.cr.execute("""
                                UPDATE aa_capacity_machine
                                    SET aa_plan_only = True WHERE EXTRACT(DOW FROM aa_date) = 0;
                            """)

        self.env.cr.execute("""
                                UPDATE aa_capacity_machine
                                    SET aa_name = CONCAT(resource_resource.aa_code,'|', TO_CHAR( aa_date, 'DD-MM-YYYY (IW|DY)'))
                                    FROM resource_resource
                                    WHERE aa_plan_only = FALSE AND  resource_resource.id = aa_capacity_machine.aa_resource_id;

                                UPDATE aa_capacity_machine
                                    SET aa_name = CONCAT(resource_resource.aa_code,'|', TO_CHAR( aa_date, 'DD-MM-YYYY'), ' ', '(PLAN)')
                                    FROM resource_resource
                                    WHERE aa_plan_only = TRUE AND  resource_resource.id = aa_capacity_machine.aa_resource_id;
                                    
                                UPDATE aa_capacity_machine
                                    SET aa_prod_time_norm = resource_resource.aa_prod_time_norm 
                                    FROM resource_resource
                                    WHERE resource_resource.id = aa_capacity_machine.aa_resource_id;
                            """)

        # Sunday
        self.env.cr.execute("""
                                UPDATE aa_capacity_machine 
                                    SET aa_html = CONCAT('<div style="width: 110px; background-color : #7c7bad; color: white; padding-left: 4px">PLAN ONLY (SUN)</div>')
                                    WHERE aa_plan_only = True;
                            """)
                            
        # DELETED aa_html updates here, has to be done at tak move only (Alexander)
