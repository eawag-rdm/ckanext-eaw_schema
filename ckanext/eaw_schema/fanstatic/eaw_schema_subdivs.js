// Enable JavaScript's strict mode. Strict mode catches some common
// programming errors and throws exceptions, prevents some unsafe actions from
// being taken, and disables some confusing and bad JavaScript features.
"use strict";

ckan.module('eaw_schema_subdivs', function ($) {
  return {
    initialize: function () {
      var outerdiv = $( 'div.' + this.options.divname_outer );
      if (this.options.divnames_inner !== undefined) {
	var innerselect = $( this.options.divnames_inner.split(/\s+/).map(
	  x => 'div.' + x).join());
      }
      if (this.options.names_clearfields !== undefined) {
	var clearselect = $( this.options.names_clearfields.split(/\s+/).map(
	  x => '#field-' + x).join());
      }
      var select2_options = {
	onText: "YES",
	onColor: "primary",
	offText: "NO",
	offColor: "default",
	size: "normal",
	animate: false
      };
      var $el = this.el;
      $el.bootstrapSwitch(select2_options);
      if (innerselect !== undefined) {
	if ($el.bootstrapSwitch('state')) {
	  innerselect.show();
	  outerdiv.css('border-radius', '10px 10px 0px 0px');
	} else {
	  innerselect.hide();
	}
	$el.on('switchChange.bootstrapSwitch', function(event, state) {
	  if (state) {
	    innerselect.show(100);
	    outerdiv.css('border-radius', '10px 10px 0px 0px');
	  } else {
	    innerselect.hide(100);
	    outerdiv.css('border-radius', '10px 10px 10px 10px');
	    if (clearselect !== undefined) {
	      clearselect.val('');
	    }
	  }
	});
      }
    }
  };
});
