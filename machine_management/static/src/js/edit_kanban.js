/** @odoo-module */

import { kanbanView } from '@web/views/kanban/kanban_view';
import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { KanbanRecord } from '@web/views/kanban/kanban_record';
import { registry } from '@web/core/registry';

export class MachineKanbanRecord extends KanbanRecord {
    
    onGlobalClick(ev) {
        if (ev.target.closest('.oe_kanban_global_dblclick')) {
            if (ev.target.closest('.oe_kanban_global_dblclick').children[0].classList.contains('oe_update_column')){
                ev.target.closest('.oe_kanban_global_dblclick').children[0].classList.remove('oe_update_column')
            }
            else{
                ev.target.closest('.oe_kanban_global_dblclick').children[0].classList.add('oe_update_column')
            }
            return;
        }
        else{
            if (ev.target.closest('.open_kanban_machines')) {
                const action = this.props.record.model.orm.call('project.task', "aa_action_normal_machines", [], {
                    recordDate : this.props.record.data.aa_name
                });
                return this.action.doAction(action);
            }
            return super.onGlobalClick(ev);
        }
    }
}

export class MachineKanbanRenderer extends KanbanRenderer { 
    async o_column_go_zero(group){
        history.back();
    }

    async o_column_go_normal(group){
        if (group.records[0].resModel === "project.task") {
            const action = await group.model.orm.call('project.task', "aa_action_normal_machines", [], {
                recordDate : group.displayName
            });
            group.model.action.doAction(action);
        }
        return;
    }
}

MachineKanbanRenderer.components = {
    ...KanbanRenderer.components,
    KanbanRecord: MachineKanbanRecord,
};

registry.category('views').add('machine_kanban', {
    ...kanbanView,
    Renderer: MachineKanbanRenderer,
});
