// Enable JavaScript's strict mode. Strict mode catches some common
// programming errors and throws exceptions, prevents some unsafe actions from
// being taken, and disables some confusing and bad JavaScript features.
"use strict";

ckan.module('eaw_schema_publication', function ($) {
  return {
    initialize: function () {
      var module = this;
      var $el = this.el;
      var publink = $( 'div.publicationcheck_wrap' ).nextAll('div').first();
      $el.change(function() {
	if ($el.prop("checked")) {
	  publink.css("display", "block").css("visibility", "visible")
	  .css("background", "#C4EBEA").css("border-radius", "10px");
	} else {
	  publink.css("visibility", "hidden").css("display", "block");
	}
      });
    },
    onChange: function() {
      console.log("CHANGED");
    }
  };
});
    
  
