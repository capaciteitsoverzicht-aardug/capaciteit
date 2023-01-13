odoo.define('task_advance.kanaban_disable_drag', function (require) {
'use strict';

    var KanbanRenderer = require('web.KanbanRenderer');
    var KanbanColumn = require('web.KanbanColumn');
    var rpc = require('web.rpc');

    KanbanRenderer.include({
        _setState: function (state) {
            this._super.apply(this, arguments);
            var arch = this.arch;
            var drag_drop = true;
            if (arch.attrs.disable_drag_drop) {
                if (arch.attrs.disable_drag_drop=='true') {
                    this.columnOptions.draggable = false;
                }
            }
            this.recordOptions.sortable = true;
            if (arch.attrs.disable_sort) {
                if (arch.attrs.disable_sort=='true') {
                    this.recordOptions.sortable = false;
                }
            }
            this.columnOptions.sortable = true;
            if (arch.attrs.disable_sort_column) {
                if (arch.attrs.disable_sort_column=='true') {
                    this.columnOptions.sortable = false;
                }
            }
            var aa_self = this;
            aa_self._rpc({
                model: 'aa.capacity.machine',
                method: 'aa_checkOldCapacity',
                args: [[]],
            }).then(function (aa_cap){
                var aa_templateTag = document.getElementsByClassName('oe_kanban_content');
                for (var aa_t in aa_templateTag){
                    if (aa_templateTag[aa_t].dataset){
                        for (var cap in aa_cap){
                            if (aa_templateTag[aa_t].dataset.id && aa_templateTag[aa_t].dataset.id.replace(/,/g, '').trim() == aa_cap[cap]){
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
            });
        },
        _renderGrouped: function (fragment) {
            this._super.apply(this, arguments);
            var aa_self = this;
            if (this.columnOptions.sortable==false){
                this.$el.sortable( "disable" );
            }
            aa_self._rpc({
                model: 'project.task',
                method: 'aa_checkRfq',
                args: [[]],
            }).then(function (aa_tasks){
                var aa_carts = document.getElementsByClassName('fa-cart-plus');
                _.each(aa_tasks, function(aa_task){
                    _.each(aa_carts, function(rec){
                        if ($(rec).context.dataset.id.replace(/,/g, '').trim() == aa_task){
                            $(rec).context.style.color = 'orange';
                        }
                    })
                })
            })

            aa_self._rpc({
                model: 'project.task',
                method: 'aa_checkNotDonePo',
                args: [[]],
            }).then(function (aa_tasks){
                var aa_carts = document.getElementsByClassName('fa-cart-plus');
                _.each(aa_tasks, function(aa_task){
                    _.each(aa_carts, function(rec){
                        if ($(rec).context.dataset.id.replace(/,/g, '').trim() == aa_task){
                            $(rec).context.style.color = 'red';
                        }
                    })
                })
            })

            aa_self._rpc({
                model: 'project.task',
                method: 'aa_checkDonePo',
                args: [[]],
            }).then(function (aa_tasks){
                var aa_carts = document.getElementsByClassName('fa-cart-plus');
                _.each(aa_tasks, function(aa_task){
                    _.each(aa_carts, function(rec){
                        if ($(rec).context.dataset.id.replace(/,/g, '').trim() == aa_task){
                            $(rec).context.style.color = 'green';
                        }
                    })
                })
            })

            aa_self._rpc({
                model: 'project.task',
                method: 'aa_checkDeliveryDone',
                args: [[]],
            }).then(function (aa_tasks){
                var aa_upload = document.getElementsByClassName('fa-upload');
                _.each(aa_tasks, function(aa_task){
                    _.each(aa_upload, function(rec){
                        if ($(rec).context.dataset.id.replace(/,/g, '').trim() == aa_task){
                            $(rec).context.style.color = 'green';
                        }
                    })
                })
            })

            aa_self._rpc({
                model: 'project.task',
                method: 'aa_checkDeliveryAssign',
                args: [[]],
            }).then(function (aa_tasks){
                var aa_upload = document.getElementsByClassName('fa-upload');
                _.each(aa_tasks, function(aa_task){
                    _.each(aa_upload, function(rec){
                        if ($(rec).context.dataset.id.replace(/,/g, '').trim() == aa_task){
                            $(rec).context.style.color = 'red';
                        }
                    })
                })
            })

            aa_self._rpc({
                model: 'project.task',
                method: 'aa_checkDeliveryPartial',
                args: [[]],
            }).then(function (aa_tasks){
                var aa_upload = document.getElementsByClassName('fa-upload');
                _.each(aa_tasks, function(aa_task){
                    _.each(aa_upload, function(rec){
                        if ($(rec).context.dataset.id.replace(/,/g, '').trim() == aa_task){
                            $(rec).context.style.color = 'orange';
                        }
                    })
                })
            })

            aa_self._rpc({
                model: 'project.task',
                method: 'aa_checkStudioNew',
                args: [[]],
            }).then(function (aa_tasks){
                var aa_picture = document.getElementsByClassName('fa-picture-o');
                _.each(aa_tasks, function(aa_task){
                    _.each(aa_picture, function(rec){
                        if ($(rec).context.dataset.id.replace(/,/g, '').trim() == aa_task){
                            $(rec).context.style.color = 'orange';
                        }
                    })
                })
            })

            aa_self._rpc({
                model: 'project.task',
                method: 'aa_checkStudioOnHoldCancelled',
                args: [[]],
            }).then(function (aa_tasks){
                var aa_picture = document.getElementsByClassName('fa-picture-o');
                _.each(aa_tasks, function(aa_task){
                    _.each(aa_picture, function(rec){
                        if ($(rec).context.dataset.id.replace(/,/g, '').trim() == aa_task){
                            $(rec).context.style.color = 'red';
                        }
                    })
                })
            })

            aa_self._rpc({
                model: 'project.task',
                method: 'aa_checkStudioDone',
                args: [[]],
            }).then(function (aa_tasks){
                var aa_picture = document.getElementsByClassName('fa-picture-o');
                _.each(aa_tasks, function(aa_task){
                    _.each(aa_picture, function(rec){
                        if ($(rec).context.dataset.id.replace(/,/g, '').trim() == aa_task){
                            $(rec).context.style.color = 'green';
                        }
                    })
                })
            })

            aa_self._rpc({
                model: 'project.task',
                method: 'aa_checkPreprocessNew',
                args: [[]],
            }).then(function (aa_tasks){
                var aa_picture = document.getElementsByClassName('fa-pencil-square');
                _.each(aa_tasks, function(aa_task){
                    _.each(aa_picture, function(rec){
                        if ($(rec).context.dataset.id.replace(/,/g, '').trim() == aa_task){
                            $(rec).context.style.color = 'orange';
                        }
                    })
                })
            })

            aa_self._rpc({
                model: 'project.task',
                method: 'aa_checkPreprocessOnHoldCancelled',
                args: [[]],
            }).then(function (aa_tasks){
                var aa_picture = document.getElementsByClassName('fa-pencil-square');
                _.each(aa_tasks, function(aa_task){
                    _.each(aa_picture, function(rec){
                        if ($(rec).context.dataset.id.replace(/,/g, '').trim() == aa_task){
                            $(rec).context.style.color = 'red';
                        }
                    })
                })
            })
            
            aa_self._rpc({
                model: 'project.task',
                method: 'aa_checkPreprocessDone',
                args: [[]],
            }).then(function (aa_tasks){
                var aa_picture = document.getElementsByClassName('fa-pencil-square');
                _.each(aa_tasks, function(aa_task){
                    _.each(aa_picture, function(rec){
                        if ($(rec).context.dataset.id.replace(/,/g, '').trim() == aa_task){
                            $(rec).context.style.color = 'green';
                        }
                    })
                })
            })

            aa_self._rpc({
                model: 'project.task',
                method: 'aa_ChangeDateColorRed',
                args: [[]],
            }).then(function (aa_tasks){
                var aa_dateChange = document.getElementsByClassName('datum');
                _.each(aa_tasks, function(aa_task){
                    _.each(aa_dateChange, function(rec){
                        if ($(rec).context.dataset.id.replace(/,/g, '').trim() == aa_task){
                            $(rec).context.style.color = 'red';
                        }
                    })
                })
            })

            aa_self._rpc({
                model: 'project.task',
                method: 'aa_ChangeDateColorGreen',
                args: [[]],
            }).then(function (aa_tasks){
                var aa_dateChange = document.getElementsByClassName('datum');
                _.each(aa_tasks, function(aa_task){
                    _.each(aa_dateChange, function(rec){
                        if ($(rec).context.dataset.id.replace(/,/g, '').trim() == aa_task){
                            $(rec).context.style.color = 'green';
                        }
                    })
                })
            })
            
            aa_self._rpc({
                model: 'project.task',
                method: 'aa_ChangeDateColorOrange',
                args: [[]],
            }).then(function (aa_tasks){
                var aa_dateChange = document.getElementsByClassName('datum');
                _.each(aa_tasks, function(aa_task){
                    _.each(aa_dateChange, function(rec){
                        if ($(rec).context.dataset.id.replace(/,/g, '').trim() == aa_task){
                            $(rec).context.style.color = 'orange';
                        }
                    })
                })
            })

            aa_self._rpc({
                model: 'project.task',
                method: 'aa_ChangeDateColorGray',
                args: [[]],
            }).then(function (aa_tasks){
                var aa_dateChange = document.getElementsByClassName('datum');
                _.each(aa_tasks, function(aa_task){
                    _.each(aa_dateChange, function(rec){
                        if ($(rec).context.dataset.id.replace(/,/g, '').trim() == aa_task){
                            $(rec).context.style.color = 'gray';
                        }
                    })
                })
            })

            aa_self._rpc({
                model: 'project.task',
                method: 'aa_ChangeLevelColorGreen',
                args: [[]],
            }).then(function (aa_tasks){
                var aa_levelChange = document.getElementsByClassName('fa-level-up');
                _.each(aa_tasks, function(aa_task){
                    _.each(aa_levelChange, function(rec){
                        if ($(rec).context.dataset.id.replace(/,/g, '').trim() == aa_task){
                            $(rec).context.style.color = 'green';
                        }
                    })
                })
            })

            aa_self._rpc({
                model: 'project.task',
                method: 'aa_ChangeLevelColorOrange',
                args: [[]],
            }).then(function (aa_tasks){
                var aa_levelChange = document.getElementsByClassName('fa-level-up');
                _.each(aa_tasks, function(aa_task){
                    _.each(aa_levelChange, function(rec){
                        if ($(rec).context.dataset.id.replace(/,/g, '').trim() == aa_task){
                            $(rec).context.style.color = 'orange';
                        }
                    })
                })
            })

            aa_self._rpc({
                model: 'project.task',
                method: 'aa_ChangeTruckColorGreen',
                args: [[]],
            }).then(function (aa_tasks){
                var aa_truckChange = document.getElementsByClassName('fa-truck');
                _.each(aa_tasks, function(aa_task){
                    _.each(aa_truckChange, function(rec){
                        if ($(rec).context.dataset.id.replace(/,/g, '').trim() == aa_task){
                            $(rec).context.style.color = 'green';
                        }
                    })
                })
            })

            aa_self._rpc({
                model: 'project.task',
                method: 'aa_ChangeTruckColorOrange',
                args: [[]],
            }).then(function (aa_tasks){
                var aa_truckChange = document.getElementsByClassName('fa-truck');
                _.each(aa_tasks, function(aa_task){
                    _.each(aa_truckChange, function(rec){
                        if ($(rec).context.dataset.id.replace(/,/g, '').trim() == aa_task){
                            $(rec).context.style.color = 'orange';
                        }
                    })
                })
            })

            aa_self._rpc({
                model: 'project.task',
                method: 'aa_ChangeTruckColorGray',
                args: [[]],
            }).then(function (aa_tasks){
                var aa_truckChange = document.getElementsByClassName('fa-truck');
                _.each(aa_tasks, function(aa_task){
                    _.each(aa_truckChange, function(rec){
                        if ($(rec).context.dataset.id.replace(/,/g, '').trim() == aa_task){
                            $(rec).context.style.color = 'gray';
                        }
                    })
                })
            })

            // aa_self._rpc({
            //     model: 'project.task',
            //     method: 'aa_readyToDeliver',
            //     args: [[]],
            // }).then(function (aa_tasks){
            //     var aa_dateChange = document.getElementsByClassName('datum');
            //     _.each(aa_tasks, function(aa_task){
            //         _.each(aa_dateChange, function(rec){
            //             if ($(rec).context.dataset.id.replace(/,/g, '').trim() == aa_task){
            //                 $(rec).context.style.color = 'gray';
            //             }
            //         })
            //     })
            // })
       },
    });

    KanbanColumn.include({
        start: function () {
            this._super.apply(this, arguments);
            if (this.record_options.sortable==false){
                this.$el.sortable( "disable" );
            }
        },
    });
});