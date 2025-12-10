/* eaw_schema_info_modal.js
 * 
 * Provides  help-modals for the eaw_schema fields.
 * To be used in search- and new-package forms
 */

"use strict";

ckan.module('eaw_schema_info_modal', function () {
    return {
	initialize: function () {
	    var target = this.options.target;
	    var modalEl = document.querySelector(target);
	    var bsModal = new bootstrap.Modal(modalEl, {show: false});
	    this.el.click(function () {bsModal.toggle();});
	}
    };
});
