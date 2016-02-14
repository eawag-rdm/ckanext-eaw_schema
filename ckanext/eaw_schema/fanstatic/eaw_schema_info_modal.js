/* eaw_schema_info_modal.js
 * 
 * Provides  help-modals for the eaw_schema fields.
 * To be used in search- and new-package forms
 */

"use strict";

ckan.module('eaw_schema_info_modal', function ($, _) {
    return {
	initialize: function () {
	    var target = this.options.target;
	    var modal = this.sandbox.jQuery( target );
	    modal.modal({show: false});
	    this.el.click(function (){modal.modal('toggle')});
	}
    };
});
