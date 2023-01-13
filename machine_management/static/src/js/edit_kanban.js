odoo.define('task_advance.edit_kanban', function (require) {
'use strict';

    var KanbanRecord = require('web.KanbanRecord');
    var KanbanColumn = require('web.KanbanColumn');

    KanbanRecord.include({
        _render: function () {
            this._super.apply(this, arguments);
            if (this.$el.hasClass('oe_kanban_global_dblclick')) {
                this.$el.on('dblclick', this.proxy('_onGlobalClick'));
                this.$el.on('click', this.proxy('_onFoldColumnClick'));
            }
            if (this.$el.hasClass('open_kanban_machines')) {
                this.$el.on('click', this.proxy('_openMachineRecords'));
            }
            return $.when.apply(this, this.defs);
        },
        _onFoldColumnClick: function() {
            if ($(this.$el[0].children[0]).height() === 120){
                $(this.$el[0].children[0]).css('height', '100%');
            }
            else{
                $(this.$el[0].children[0]).css('height', '120');
            }
        },
        _openMachineRecords: function() {
            var self = this;
            this._rpc({
                model: 'project.task',
                method: 'aa_action_normal_machines',
                args: [this.recordData.aa_name],
            }).then(function (action) {
                self.do_action(action);
            });
        }
	});
});
