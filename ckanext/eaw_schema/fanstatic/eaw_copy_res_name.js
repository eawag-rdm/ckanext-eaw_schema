// Auto-fill of the "Name" field for resource-upload
// derived from upload-filename or link-URL

"use strict";

ckan.module('eaw_copy_res_name', function($) {
  return {
    initialize: function () {
      $.proxyAll(this, /_on/);
      var el = this.el;
      var source_context = $('div[data-module="image-upload"]');
      var source_input_file = $('input[name="upload"]', source_context);
      var source_input_url = $('input[name="url"]', source_context);

      source_input_file.change(function () {
	var fn = this.value.split(/^C:\\fakepath\\/).pop();
	el.val(fn);
      });
      source_input_url.change(function () {
	var name = this.value.split('/').pop();
	el.val(name);
      });
    }
  };
});
