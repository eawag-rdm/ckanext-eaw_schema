// Enable JavaScript's strict mode. Strict mode catches some common
// programming errors and throws exceptions, prevents some unsafe actions from
// being taken, and disables some confusing and bad JavaScript features.
"use strict";

ckan.module('eaw_schema_conditional_multicheck', function ($, _) {
  return {
    pyobstr2json: function (pyostr) {
      var fixedstring =	this.options.choices
	    .replace(/\(/g, "[").replace(/\)/g, "]")
	    .replace(/u(\'.+?\')/g, function (match, p1) {return p1;})
	    .replace(/\'/g, "\"").replace("False", "false");
      return(JSON.parse(fixedstring));
    },
    initialize: function () {
      // console.log("I've been initialized for element: ", this.el);
      // console.log(this.options.choices);
      // console.log(this.options.fieldprefix);
      
      var choices = this.pyobstr2json(this.options.choices);
      var fieldprefix = this.options.fieldprefix;
      var trigtars = [];
      choices.forEach(function (f) {
      	var trig = f.pop();
      	if (trig) {
	  trig.split(" ").forEach( function (t) {
	    // console.log($(fieldprefix+t));
	    $('#'+fieldprefix+t).on('change', function() {
	      $('#'+fieldprefix+f[0]).prop('checked', this.checked);
	    });
	  });
      	}
      });
      // console.log(trigtars);
    }
  };
});
