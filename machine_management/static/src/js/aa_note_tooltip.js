odoo.define('task_advance.aa_note_tooltip', function (require){
    "use strict";

    var fieldRegistry = require('web.field_registry');
    var WebBasic = require('web.basic_fields');
    var dom = require('web.dom');
    var core = require('web.core');
    var qweb = core.qweb;
    var _t = core._t;

var CustomFieldChar = WebBasic.InputField.extend(WebBasic.TranslatableFieldMixin, {
    className: 'o_field_text',
    supportedFieldTypes: ['text'],
    tagName: 'span',

    events: _.extend({}, WebBasic.DebouncedField.prototype.events, {
        'mouseover':'_OnHover',
        'input': '_onInput',
        'change': '_onChange',
    }),

    /**
     * @constructor
     */
    init: function () {
        this._super.apply(this, arguments);

        if (this.mode === 'edit') {
            this.tagName = 'textarea';
        }
    },
    /**
     * As it it done in the start function, the autoresize is done only once.
     *
     * @override
     */
    start: function () {
        if (this.mode === 'edit') {
            dom.autoresize(this.$el, {parent: this});

            this.$el = this.$el.add(this._renderTranslateButton());
        }
        return this._super();
    },
    _OnHover: function(events){
        var aa_note=String(this.value);
        if(aa_note == 'false'){
            $(event.currentTarget).tooltip({
                title: 'note',
            }).tooltip('show');
        }
        else{
                $(event.currentTarget).tooltip({
                    title:aa_note,
                }).tooltip('show');
            }
    },
    /**
     * Override to force a resize of the textarea when its value has changed
     *
     * @override
     */
    reset: function () {
        var self = this;
        return $.when(this._super.apply(this, arguments)).then(function () {
            if (self.mode === 'edit') {
                self.$input.trigger('change');
            }
        });
    },
    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * Stops the enter navigation in a text area.
     *
     * @private
     * @param {OdooEvent} ev
     */
    _onKeydown: function (ev) {
        if (ev.which === $.ui.keyCode.ENTER) {
            return;
        }
        this._super.apply(this, arguments);
    },
});

fieldRegistry.add('tooltip_widget', CustomFieldChar);
});

