"use strict";

ckan.module('eaw_copyname', function($) {
  return {
    initialize: function () {
      var el = this.el;
      var value;
      var sourceid = this.options.sourcefieldid;
      var source = document.getElementById(sourceid);

      $.proxyAll(this, /_on/);
      console.log(el[0]);
      el[0].setAttribute('value', name);
      console.log('initialized with options: ' + sourceid);
      el.focus(function () {
	console.log('got ficus!');
	var name = source.value;
	console.log("NAME: " + name);
	name = name.split('/');
	name = name[name.length - 1];
	this.setAttribute('value', name);
      });

      
    }
  };
});
