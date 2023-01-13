odoo.define('task_advance.kanaban_reload', function (require) {
'use strict';

    var KanbanModel = require('web.KanbanModel');
    var rpc = require('web.rpc');
    var ActionManager = require('web.ActionManager');

    KanbanModel.include({
        save: function (recordID) {
            var self = this;
            this._super.apply(this, arguments);
            rpc.query({
                model: 'project.task',
                method: 'fire_sql',
                args: [[]],
            }).then(function (){
                $('.o_cp_switch_buttons button.active').trigger('click');
            });
        },
    });
});
