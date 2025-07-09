/* eaw_schema_datepicker.js
 * 
 * Attaches bootstrap-datepicker.
   (
 */

"use strict";

this.ckan.module('datepicker', function ($) {
  return {
    initialize: function () {
      var picker_opts = {   
	'format': 'yyyy-mm-dd',
	'autoclose': true,
	'startDate': this.options.today,
	'endDate': this.options.maxdate
      };
      var inputGroup = this.el.parent('.input-group');
      var picker = inputGroup.datepicker(picker_opts);
      
      picker.on('show', () => {
	picker.datepicker('setDate', this.el.val());
      });
      picker.on('changeDate', e => {
	this.el.val(e.format());
      });
    }
  };
});

  
// this.ckan.module('datepicker', function (jQuery, _) {
//   return {
//     initialize: function () {
//       jQuery.proxyAll(this, /_on/);
//       this.el.ready(this._onReady);
//     },

//     _onReady: function() {
//       var dp = $(this.el).datepicker({
// 	'format': 'yyyy-mm-dd',
// 	'startDate': '1969-11-26'
//       });
//     }
//   };
// });
