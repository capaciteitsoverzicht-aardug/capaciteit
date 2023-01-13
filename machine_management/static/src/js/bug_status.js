odoo.define('task_advance.bug_status', function (require) {
'use strict';

var AbstractField = require('web.AbstractField');
var core = require('web.core');
var registry = require('web.field_registry');

var _t = core._t;

var bug_status = AbstractField.extend({
    events: _.extend({}, AbstractField.prototype.events, {
        'click': '_onClick',
    }),
    description: "",

    isSet: function () {
        return true;
    },

   _render: function () {
        var className = '';
        var bugTitle;
        if (this.recordData.aa_bug == true) {
            className = 'red_color_btn';
            bugTitle = _t('Production Issue');
        }
        else {
            className = 'aa_green_color';
            bugTitle = _t('No Issue');
        }

        var $buttonBug = $('<button/>', {
            type: 'button',
            title: bugTitle,
        }).addClass('btn btn-lg fa fa-bug margin ' + className);
        this.$el.html($buttonBug);
    },

    _onClick: function (event) {
        event.stopPropagation();
        var aa_self = this
        if (this.record.data.aa_bug == false){
            var bug = true
        }
        else{
            var bug = false
        }
        aa_self._rpc({
            model: 'project.task',
            method: 'write',
            args: [[this.record.data.id], {'aa_bug': bug}],
        }).then(function (aa_tasks){
            $('.o_cp_switch_buttons button.active').trigger('click');
        })
    },
});

registry.add("bug_status", bug_status);

});
