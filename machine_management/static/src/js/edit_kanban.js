/** @odoo-module */

import { kanbanView } from '@web/views/kanban/kanban_view';
import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { KanbanRecord } from '@web/views/kanban/kanban_record';
import { registry } from '@web/core/registry';
export const CANCEL_GLOBAL_CLICK = ["a", ".dropdown", ".oe_kanban_action"].join(",");

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

    openGlobalClick(ev) {
        const {forceGlobalClick, openRecord, record } = this.props;
        if (ev.target.closest(CANCEL_GLOBAL_CLICK)) {
            return;
        }
        if (forceGlobalClick || ev.target.closest('.oe_kanban_global_dblclick')) {
            openRecord(record);
        }
        return;
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

    async o_column_opacity(group){
        const action = await group.model.orm.call('aa.capacity.machine', "aa_checkOldCapacity", [], {
            });
        var aa_templateTag = document.getElementsByClassName('oe_kanban_content');
        for (var aa_t in aa_templateTag){
            if (aa_templateTag[aa_t].dataset){
                for (var cap in action){
                    if (aa_templateTag[aa_t].dataset.id && aa_templateTag[aa_t].dataset.id.replace(/,/g, '').trim() == action[cap]){
                        if (aa_templateTag[aa_t].style.opacity == '1'){
                            aa_templateTag[aa_t].style.opacity = 0.3;
                        }
                        else{
                            aa_templateTag[aa_t].style.opacity = 1;
                        }
                    }
                }
            }
        }
        return action
    }

    async sortRecordDrop(dataRecordId, dataGroupId, { element, parent, previous }) {
        element.classList.remove("o_record_draggable");
        if (
            !this.props.list.isGrouped ||
            parent.classList.contains("o_kanban_hover") ||
            parent.dataset.id === element.parentElement.dataset.id
        ) {
            parent && parent.classList && parent.classList.remove("o_kanban_hover");
            while (previous && !previous.dataset.id) {
                previous = previous.previousElementSibling;
            }
            const refId = previous ? previous.dataset.id : null;
            const targetGroupId = parent && parent.dataset.id;
            await this.props.list.moveRecord(dataRecordId, dataGroupId, refId, targetGroupId);
        }
        element.classList.add("o_record_draggable");
        window.$(body).find('.o_cp_switch_buttons button.active').trigger('click');
    }

    getGroupsOrRecords() {
        var res = super.getGroupsOrRecords();
        if (res && res[0] && res[0].group && res[0].group.resModel == 'resource.resource'){
            const data = this.o_column_opacity(res[0].group)
        }
        return res
    }

    getGroupClasses(group) {
        if (group.count > 1){
            group.isFolded = false
        }
        const classes = [];
        if (this.canResequenceGroups && group.value) {
            classes.push("o_group_draggable");
        }
        if (!group.count) {
            classes.push("o_kanban_no_records");
        }
        if (!this.env.isSmall && group.isFolded) {
            classes.push("o_column_folded");
        }
        if (!group.isFolded && !group.hasActiveProgressValue) {
            classes.push("bg-100");
            // this.loadMore(group)
        }
        if (group.progressBars.length) {
            classes.push("o_kanban_has_progressbar");
            if (!group.isFolded && group.hasActiveProgressValue) {
                const progressBar = group.activeProgressBar;
                classes.push("o_kanban_group_show", `o_kanban_group_show_${progressBar.color}`);
            }
        }
        return classes.join(" ");
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
