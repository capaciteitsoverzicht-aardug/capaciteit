odoo.define('task_advance.lock_status', function (require) {
'use strict';

var AbstractField = require('web.AbstractField');
var core = require('web.core');
var registry = require('web.field_registry');

var _t = core._t;

var lock_status = AbstractField.extend({
    events: _.extend({}, AbstractField.prototype.events, {
        'click': '_onClick',
    }),
    description: "",

    isSet: function () {
        return true;
    },

   _render: function () {
        var className = '';
        var title;
        if (this.recordData.aa_lock == true) {
            className = 'red_color_btn';
            title = _t('Produciton Locked');
        }
        else {
            className = 'aa_green_color';
            title = _t('Produciton Unlocked');
        }
        var $button = $('<button/>', {
            type: 'button',
            title: title,
        }).addClass('btn btn-lg fa fa-lock margin ' + className);
        this.$el.html($button);
    },

    _onClick: function (event) {
        event.stopPropagation();
        var aa_self = this
        if (this.record.data.aa_lock == false){
            var lock = true
        }
        else{
            var lock = false
        }
        aa_self._rpc({
            model: 'project.task',
            method: 'write',
            args: [[this.record.data.id], {'aa_lock': lock}],
        }).then(function (aa_tasks){
            $('.o_cp_switch_buttons button.active').trigger('click');
        })
    },
});

registry.add("lock_status", lock_status);

});
