odoo.define('task_advance.aa_task_kanban_progressbar', function (require) {
'use strict';

    var aa_utils = require('web.utils');
    var KanbanColumnProgressBar = require('web.KanbanColumnProgressBar');

    KanbanColumnProgressBar.include({
        init: function (parent, options, columnState) {
            this._super.apply(this, arguments);
            // this._super(parent, options, columnState);
            this.progessBarPercentage = 0;
            console.log(this, this.progessBarPercentage);
        },

        _render: function () {
            var self = this;
            if (this.columnState.model === 'project.task' &&
                this.columnState.progressBarValues.sum_field === 'aa_production_time_count'){
                this._super();
                // Display and animate the progress bars
                var aa_machineCapacity = 0;
                var aa_barNumber = 0;
                var aa_barMinWidth = 0; // In %

                _.each(self.columnState.data, function (record) {
                    var aa_recordData = record.data;
                    if (aa_recordData.aa_capacity_machine_id) {
                        self._rpc({
                            model: aa_recordData.aa_capacity_machine_id.model,
                            method: 'search_read',
                            fields: ['aa_capacity'],
                            domain: [['id', '=', aa_recordData.aa_capacity_machine_id.res_id]]
                        }).then(function (values) {
                            aa_machineCapacity = values[0].aa_capacity;
                            _.each(self.colors, function (val, key) {
                                var aa_$bar = self.$bars[val];
                                var aa_count = self.subgroupCounts && self.subgroupCounts[key] || 0;

                                if (!aa_$bar) {
                                return;
                            }

                            // Adapt tooltip
                            aa_$bar.attr('data-original-title', aa_count + ' ' + key);
                            aa_$bar.tooltip({
                                delay: 0,
                                trigger: 'hover',
                            });

                            // Adapt active state
                            aa_$bar.toggleClass('active progress-bar-striped', key === self.activeFilter);

                            // Adapt width
                            aa_$bar.removeClass('o_bar_has_records transition-off');
                            window.getComputedStyle(aa_$bar[0]).getPropertyValue('width'); // Force reflow so that animations work
                            if (aa_count > 0) {
                                aa_$bar.addClass('o_bar_has_records');
                                // Make sure every bar that has records has some space
                                // and that everything adds up to 100%
                                var aa_maxWidth = 100 - aa_barMinWidth * aa_barNumber;
                                self.$('.progress-bar.o_bar_has_records').css('max-width', aa_maxWidth + '%');
                                aa_count = self.totalCounterValue;
                                if (aa_machineCapacity > 0){
                                    aa_$bar.css('width', (aa_count * 100 / aa_machineCapacity) + '%');
                                    self.progessBarPercentage = (aa_count * 100 / aa_machineCapacity).toFixed(2);
                                    aa_barNumber++;
                                    aa_$bar.attr('aria-valuemin', 0);
                                    aa_$bar.attr('aria-valuemax', aa_machineCapacity);
                                    aa_$bar.attr('aria-valuenow', aa_count);
                                }
                                else {
                                    aa_$bar.css('width', '');
                                }
                            } else {
                                aa_$bar.css('width', '');
                            }
                        });
                        self.$('.progress-bar.o_bar_has_records').css('min-width', aa_barMinWidth + '%');
                        });
                    }
                });
            }
            else {
                this._super();
            }
        },
    });

});