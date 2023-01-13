odoo.define('task_advance.production_status', function (require) {
'use strict';

var AbstractField = require('web.AbstractField');
var core = require('web.core');
var registry = require('web.field_registry');

var _t = core._t;

var production_status = AbstractField.extend({
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
        if (this.recordData.is_production_done == true) {
            className = 'aa_green_color';
            title = _t('Produciton done');
        }
        else {
            className = 'red_color_btn';
            title = _t('Produciton not done yet');
        }
        var $button = $('<button/>', {
            type: 'button',
            title: title,
        }).addClass('btn btn-lg fa fa-download margin ' + className);
        this.$el.html($button);
    },

    _onClick: function (event) {
        event.stopPropagation();
        var aa_self = this
        if (this.record.data.is_production_done == false){
            var produciton = true
        }
        else{
            var produciton = false
        }
        aa_self._rpc({
            model: 'project.task',
            method: 'write',
            args: [[this.record.data.id], {'is_production_done': produciton}],
        }).then(function (aa_tasks){
            $('.o_cp_switch_buttons button.active').trigger('click');
        })
    },
});

registry.add("production_status", production_status);

});
