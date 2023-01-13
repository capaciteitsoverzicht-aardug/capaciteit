odoo.define('task_advance.all_machine_kanban', function (require) {
"use strict";
    var Widget = require('web.Widget');

    var ShowAllMachine = Widget.include({
        events: {
                    'click .o_column_go_normal': '_onShowMachine',
                    'click .o_column_go_zero': '_onHideMachine',
                },
        _onShowMachine: function(event)
            {   var self = this;
                // var recordDate = $('input[name="record_date"]').val()
                this._rpc({
                        model: 'project.task',
                        method: 'aa_action_normal_machines',
                        args: [event.currentTarget.innerHTML, ],
                    })
                    .then(function (action) {
                        self.do_action(action);
                    });
            },
        _onHideMachine: function()
        {
            var self = this;
            history.back();
        }
    });
    return  ShowAllMachine;
});