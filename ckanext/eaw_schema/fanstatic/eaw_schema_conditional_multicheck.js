// Enable JavaScript's strict mode. Strict mode catches some common
// programming errors and throws exceptions, prevents some unsafe actions from
// being taken, and disables some confusing and bad JavaScript features.
"use strict";

// To be used in a checkbox fieldset, e.g. in eaw_multiple_checkbox.html:
// <fieldset class="checkboxes" data-module="eaw_schema_conditional_multicheck",
// 	    data-module-choices="{{choices}}",
// 	    data-module-fieldprefix="field-{{ field.field_name }}-">
//
// Handles the "autocheckif" - property in the corresponding choices object.
//
// autockeckif != false makes a checkbox a "target-checkbox".
//
// The corresponding "trigger-checkboxes" are those with the labels denoted by
// the values of the autocheckif property.
//
// When a trigger-checkbox is checked, the target-checkbox is force-checked.
//
// As long as at least one triggert-checkbox is checked, the target-checkbox
// can not be unchecked.

ckan.module('eaw_schema_conditional_multicheck', function ($, _) {
  return {
    pyobstr2json: function (pyostr) {
      // convert a python-style object to json. Tuples to lists,
      // get rid of utf - marker, fix quotation marks.
      var fixedstring =	this.options.choices
	    .replace(/\(/g, "[").replace(/\)/g, "]")
	    .replace(/u(\'.+?\')/g, function (match, p1) {return p1;})
	    .replace(/\'/g, "\"").replace(/False/g, "false");
      return(JSON.parse(fixedstring));
    },
    initialize: function () {      
      var choices = this.pyobstr2json(this.options.choices);
      var fieldprefix = this.options.fieldprefix;
      var trigtars = [];
      choices.forEach(function (f) {
      	var trig = f.pop();
      	if (trig) {
	  trig.split(" ").forEach(function (t) {
	    $('#'+fieldprefix+t).on('change', function() {
	      $('#'+fieldprefix+f[0]).prop('checked', this.checked
					   || $('#'+fieldprefix+f[0]).checked);
	    });
	  });
	  $('#'+fieldprefix+f[0]).on('change', function () {
	    var check = trig.split(" ").map(function (x) {
		return($('#'+fieldprefix+x).is(':checked'));
	      }).concat(this.checked).reduce(function (x, y) {
		return(x || y);
	      });
	    $('#'+fieldprefix+f[0]).prop('checked', check);
	  });
	}
      });
    }
  };
});
