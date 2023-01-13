odoo.define('task_advance.machine_dashboard', function (require){
    "use strict";

    var core = require('web.core');
    var QWeb = core.qweb;
    var widgetRegistry = require('web.widget_registry');
    var Widget = require('web.Widget');
    var MachineDashboard = Widget.extend({
        template: "MachineDashboardDetails",
        events: {
            'click .search-data': '_aa_filterData',
        },

        init: function(parent, data, options) {
            this._super.apply(this, arguments);
            this.aa_machine_header = py.eval(data.data.aa_machine_header);
            this.aa_machine_info = py.eval(data.data.aa_machine_info);
        },

        _aa_filterData: function () {
            var aa_data = this.__parentedParent.state.data;
            this.aa_machine_header = py.eval(aa_data.aa_machine_header);
            this.aa_machine_info = py.eval(aa_data.aa_machine_info);
            this.renderElement();
        },

        renderElement: function() {
            var $el;
            $el = $(QWeb.render("MachineDashboardDetails", {widget: this}).trim());
            this._replaceElement($el);
        },
    });
    widgetRegistry.add('machine_dashboard', MachineDashboard);
});