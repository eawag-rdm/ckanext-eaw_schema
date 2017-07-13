// Enable JavaScript's strict mode. Strict mode catches some common
// programming errors and throws exceptions, prevents some unsafe actions from
// being taken, and disables some confusing and bad JavaScript features.
"use strict";

ckan.module('eaw_schema_publication', function ($) {
  return {
    initialize: function () {
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
      var ispublicationdiv = $( 'div.publicationcheck');
      var publicationlink = $( 'div.publicationlink' );
      var publicationmanuscript = $('div.publicationmanuscript');
      var pubdivs = publicationlink.add(publicationmanuscript);
      $el.bootstrapSwitch('state') ? pubdivs.show() : pubdivs.hide();
      $el.on('switchChange.bootstrapSwitch', function(event, state) {
	if (state) {
	  pubdivs.show(100);
	  ispublicationdiv.css('border-radius', '10px 10px 0px 0px');
	} else {
	  pubdivs.hide(100);
	  ispublicationdiv.css('border-radius', '10px 10px 10px 10px');
	  $( 'input#field-publicationmanuscript' ).removeAttr('checked');
	  $(' input#field-publicationlink' ).val('');
	}
      });
  }};
});

      // var checkbox = $el.children( 'input.eaw_schema_checkbox' ).first();
      // 
      // 
      // publink.css("display", "none");
      // pubmanu.css("display", "none");
      // checkbox.on("select2:select", function() {
      // 	alert("CHANGED!");
	// if (checkbox.prop("checked")) {
	//   publink.css("display", "block").css("visibility", "visible");
	//   pubmanu.css("display", "block").css("visibility", "visible");
	// } else {
	//   publink.css("visibility", "hidden").css("display", "block");
	//   pubmanu.css("visibility", "hidden").css("display", "block");
	// }
