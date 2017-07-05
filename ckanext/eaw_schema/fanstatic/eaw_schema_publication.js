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
      publink.css("display", "none");
      $el.change(function() {
	if ($el.prop("checked")) {
	  publink.css("display", "block").css("visibility", "visible")
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
    
  
