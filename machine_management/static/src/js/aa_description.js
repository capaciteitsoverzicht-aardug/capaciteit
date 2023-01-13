odoo.define('task_advance.aa_description', function (require) {
'use strict';

    var KanbanRecord = require('web.KanbanRecord');
    var KanbanController = require('web.KanbanController');

    KanbanRecord.include({
        init: function(parent, options) {
            this.events["click .aa_customerName"] = "aa_hideRecords";
            // this.events["dblclick .aa_customerName"] = "aa_showRecords";
            this.events["click .find_same_so"] = "aa_decorateRecords";
            // this.events["dblclick .aa_kanbanTag"] = "aa_removeDecorationRecords";
            this.events["click .fa-scissors"] = "aa_split_task";
            this._super.apply(this, arguments);
        },

        aa_split_task: function (event) {
            var aa_self = this;
            this.do_action('task_advance.aa_action_split_task',{
                additional_context: {
                    default_aa_task_id: this.id,
                }
            });
        },
        aa_hideRecords: function (event) {
            var aa_self = this;
            aa_self._rpc({
                model: 'project.task',
                method: 'aa_checkTaskDescription',
                args: [[], event.currentTarget.innerHTML],
            }).then(function (aa_tasks){
                var aa_templateTag = document.getElementsByClassName('oe_kanban_content');
                for (var aa_t in aa_templateTag){
                    if (aa_templateTag[aa_t].dataset){
                        for (var aa_task in aa_tasks){
                            if (aa_templateTag[aa_t].dataset.id == aa_tasks[aa_task]){
                                if (aa_templateTag[aa_t].style.opacity == '1'){
                                    aa_templateTag[aa_t].style.opacity = 0.1;
                                }
                                else{
                                     aa_templateTag[aa_t].style.opacity = 1;
                                }
                            }
                        }
                    }
                }
            });
        },
        aa_decorateRecords: function (event) {
            var aa_self = this;
            aa_self._rpc({
                model: 'project.task',
                method: 'aa_find_SameSOTasks',
                args: [[], event.currentTarget.innerHTML],
            }).then(function (aa_tasks){
                var aa_templateTag = document.getElementsByClassName('oe_kanban_content');
                for (var aa_t in aa_templateTag){
                    if (aa_templateTag[aa_t].dataset){
                        for (var aa_task in aa_tasks){
                            if (aa_templateTag[aa_t].dataset.id.replace(/,/g, '').trim() == aa_tasks[aa_task]){
                                if (aa_templateTag[aa_t].style.background == 'white'){
                                    aa_templateTag[aa_t].style.background = '#f8ff93'
                                }
                                else{
                                    aa_templateTag[aa_t].style.background = 'white'
                                }
                            }
                        }
                    }
                }
            });
        },
    });

    // KanbanController.include({
    //     renderButtons: function ($node) {
    //         this._super.apply(this, arguments);
    //         var self = this;
    //         if(this.modelName === "project.task"
    //         && this.model.defaultGroupedBy[0] === "aa_capacity_machine_id"){
    //             this.$buttons.css("width","550px");
    //             this.$buttons.append($('<input type="text" name="FindTags" id="tag_taxt"\
    //                 style="margin-left:200px; width:300px; float: right;margin-right: 1%;" />\
    //                 <button type="button" class="btn btn-primary btn-sm"\
    //                 style="float: right; margin-left:500px;" id="btm_click_me">Click Me</button>'
    //             ));
    //             this.$buttons.on('click', 'button#btm_click_me', function(ev){
    //                 var aa_taxt = document.getElementById("tag_taxt").value;
    //                 console.log("aa_taxt:",aa_taxt);
    //                 if (aa_taxt){
    //                     self._rpc({
    //                         model: 'project.task',
    //                         method: 'aa_checkTaskTags',
    //                         args: [[], aa_taxt],
    //                     }).then(function (tasks){
    //                         var templateTag = document.getElementsByClassName('oe_kanban_content');
    //                         for (var t in templateTag){
    //                             if (templateTag[t].dataset){
    //                                 for (var task in tasks){
    //                                     if (templateTag[t].dataset.id == tasks[task]){
    //                                         templateTag[t].style.background = '#C0D4C3'
    //                                     }
    //                                 }
    //                             }
    //                         }
    //                     });
    //                 }
    //             });
    //         }
    //     },
    // });
});