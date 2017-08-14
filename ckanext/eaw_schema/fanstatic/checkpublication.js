// add check-button to form
// check whether dora-id or dora-link was given
// if yes, find record in dora
// return result

ckan.module('eaw_schema_checkpublication', function ($) {
  return {
    initialize: function() {
      var module = this;
      // add check-button
      (function(element) {
	var checkbutton = $('<button>', {type: 'button', text: 'Check',
					 id: 'pubcheckbutton',
					 class: 'btn btn-primary pull-right',
					 width: '80px'});
	element.after(checkbutton);
	checkbutton.click(module.main.bind(module));
      } )(this.el);
      this.el.after($(this.modal_html));
      $('#pubmodal_button_right').click(this.prefill.bind(this));
    },

    spinner: '<i class="icon-spinner icon-spin"></i>',

    pubdata: {},

    prefill: function() {
      console.log('pubdata:');
      if (! this.pubdata) {return;}
      var metadata = {title: '', authors: [], doi: '',
		      year: '', abstract: '', keywords: [] };
      if (this.pubdata[0]['source'] === 'xref') {
	metadata = this.pubdata[0];
	metadata.title = 'Data for: ' + metadata.title;
	metadata.authors = metadata.aunames;
	metadata.abstract = '';
	metadata.keywords = [];
      } else {
	var mods = $(this.pubdata[0]).find('mods');
	metadata['title'] = 'Data for: '
	  + mods.children('titleinfo').children('title').text();
	metadata.title = metadata.title.replace(/<\/?[^>]+(?:>|$)/g, "");
	var namelist = mods.find('name');
	$.each(namelist, function(idx, obj) {
	    metadata['authors'][idx] = {
	      given: $(obj).children('namepart[type="given"]').text()
	    };
	    metadata['authors'][idx]['family'] =
	    $(obj).children('namepart[type="family"]').text();
	});
	var subject = mods.find('subject').children('topic');
	$.each(subject, (idx, obj) => {
	  if ($(obj).text() !== '') {
	    metadata['keywords'].push($(obj).text());
	  }
	});
	metadata['doi'] = mods.find('identifier[type="doi"]').text();
	metadata['year'] = mods.find('originInfo dateIssued').text();
	metadata['abstract'] = mods.find('abstract').text();
	metadata.abstract = metadata.abstract.replace(/<\/?[^>]+(?:>|$)/g, "");
      }
      $('#field-title').val(metadata.title);
      this.sandbox.publish('slug-target-changed', metadata.title);
      $('#field-notes').val(metadata.abstract);
      $('input#field-tag_string').val(metadata.keywords).trigger('change');
      // collect all author fieldsiterate over all author fields
      let authorfields = $('input[id^=field-author-]');
      authorfields.each(function(idx) {
	let val = metadata.authors.length > idx
	      ? metadata.authors[idx]['family']
		+ ', ' + metadata.authors[idx]['given']
	      : '';
	this.value = val;
      });
      // add new authors if necessary
      let iter = metadata.authors.slice(authorfields.length).entries();
      let appendto = authorfields.last().parents('div.control-repeating').parent();
      for (let au of iter) {
	let aunum = au[0] + 1;
	let val = au[1]['family'] + ', ' + au[1]['given'];
	let el = `
        <div class="control-repeating">
          <div class="control-group control-medium">
	    <label class="control-label" for="field-author-${aunum}">Author ${aunum}</label>
            <div class="controls ">
              <input id="field-author-${aunum}" type="text" name="author-${aunum}" value="${val}" placeholder="" class="medinput">
	    </div>
          </div>
        </div>`;
	appendto.append(el);
      }
    },
    
    normalize_doraid: function(id) {
      return(id.replace('%3A', ':'));
    },

    identpub : function(value) {
      var regdora = /.*(eawag:\d+$|.*eawag%3A\d+$)/;
      var regdoi = /.*(10.\d{4,9}\/.+$)/;
      var ids = {};
      console.log('in identpub');
      console.log('this', this);
      console.log('value:', value);
      var res = value.match(regdora);
      if (res) {
	ids['dora_id'] = this.normalize_doraid(res[1]);
      } else {
	ids['dora_id'] = null;
	res = value.match(regdoi);
	if (res) {
	  ids['doi'] = res[1];
	} else {
	  ids['doi'] = null;
	}
      }
      return(ids);
    },

    mkdoralinks: function(id) {
      return({'oai': 'https://www.dora.lib4ri.ch/eawag/oai2?'+
	      'verb=GetRecord&metadataPrefix=mods&identifier='+id,
	      'citation': 'https://www.dora.lib4ri.ch/eawag/'+
	      'islandora/object/'+id+'/islandora_scholar_citation/'+
	      '?citation_style=APA'
	     });
    },

    get_dora_id_from_doi: function(doi) {
      var module = this;
      var popelre = /<a\s+href="\/eawag\/islandora\/object\/(eawag(?:%3A|:)\d+)">Detailed\s+Record<\/a>/;
      var doradoi = doi.replace('/', '~slsh~');
      var link = 'https://www.dora.lib4ri.ch/eawag/islandora/search/'
		   + 'mods_identifier_doi_mt%3A%28' + doradoi + '%29';
      var doraid = $.ajax({
	url: link,
	dataType: 'html',
	beforeSend: function() {
	  $('#pubcheckbutton').html(module.spinner);
	},
	complete: function(data, status) {
	  $('#pubcheckbutton').html('Check');
	  return(data);
	}})
	.then(
	  data => {
	    let id = data.match(popelre);
	    id = id === null ? null : this.normalize_doraid(id[1]);
	    return(id);
	  },
	  data => {
	    console.log('request to '+link+' failed');
	    return(null);
	  });
      return(doraid);
    },

    get_crossref_info: function(doi) {
      let link = 'https://data.crossref.org/'+doi;
      let params = {url: link, dataType: 'json'};
      return($.ajax(params));
    },

    get_dora_info: function(doralinks) {
      let params = [
	{url: doralinks.oai, dataType: 'xml'},
	{url: doralinks.citation, dataType: 'json'}];
      return(Promise.all([$.ajax(params[0]), $.ajax(params[1])]));
    },

    pubmodal: function(modalinfo) {
      var maintext;
      if (modalinfo.type === 'error') {
	maintext = '<p><b>Could not retrieve record for:</b></p>'
	  + '<p>' + modalinfo.url + '</p>'
	  + '<p>Reason: ' + modalinfo.status + '</p>'
	  + '<div class="alert-info"> Just continue after checking for typos.</div>';
	$('#pubmodal_header').addClass('alert');
	$('#pubmodal_title').html('error');
	$('#pubmodal_main').html(maintext);
	$('#pubmodal_button_left').hide();
	$('#pubmodal_button_right').html('OK').show();
      } else {
	maintext = '<p><b>Found publication:</b></p>'
	  + '<div>' + modalinfo.citation + '</div><p></p>'
	  + '<div class="alert-info">'
	  + 'If that is not the right one, just click "Wrong" and continue.</div>';
	$('#pubmodal_header').addClass('alert-success');
	$('#pubmodal_title').html('success');
	$('#pubmodal_main').html(maintext);
	$('#pubmodal_button_left').html('Wrong').addClass('btn-warning').show();
	$('#pubmodal_button_right').html('OK').addClass('btn-success').show();
	
      }
      $('#pubmodal').modal('show');
  
    },

    modal_html:
`<div id="pubmodal" class="modal hide fade">
  <div id="pubmodal_header" class="modal-header">
    <button style="right:-5px;" type="button" class="close" data-dismiss="modal" aria-hidden="true">&times</button>
    <h3 id="pubmodal_title"></h3>
  </div>
  <div class="modal-body" id="pubmodal_main">
  </div>
  <div class="modal-footer">
    <a id="pubmodal_button_left" href="#" class="btn pull-left" data-dismiss="modal"></a>
    <a id="pubmodal_button_right" href="#" class="btn pull-right" data-dismiss="modal"></a>
  </div>
</div>`,

    xref_extract: function(data) {
      let metadata = {};
      metadata.aunames = data.author.map(el => {
	return(el.family + ', ' + el.given);});
      metadata.authors = metadata.aunames.join(', ');
      metadata.title = data.title;
      metadata.year = data.created['date-parts'][0][0];
      metadata.journal = '<i>' + data['container-title'] + '</i>';
      metadata.page = data.page;
      metadata.volume = data.volume;
      metadata.issue = data.issue;
      metadata.doi = `https://doi.org/${data.DOI}`;
      let citation = `${metadata.authors} (${metadata.year}). `
	    + `${metadata.title}. ${metadata.journal}, `
	    + `${metadata.volume}(${metadata.issue}), ${metadata.page}. `
	    + `${metadata.doi}`;
      metadata.source = 'xref';
      this.pubdata = [metadata, {'citation': citation}];
      return(citation);
    },
    
    main: function () {
      // identify id-type
      // if dora, get dora-record
      // if doi, search dora-record
      // if not found, get crossref-record
      // return: attributes, citationtext, error
      var value = this.el.val();
      var doralinks;
      console.log('in main');
      console.log('value:', value);
      idtyp = this.identpub.call(this, value);
      console.log('idtyp', idtyp);
      if (idtyp.dora_id !== null) {
	// get the dora record and citation
	doralinks = this.mkdoralinks(idtyp.dora_id);
	this.get_dora_info(doralinks)
	  .then(data => {  //We got OAI-record and citation
	    //check if record was found via OAI-PMH
	    let error = $(data[0]).find('error');
	    if (error.length > 0) {
	      this.pubmodal(
		{type: 'error',
		 status: error.text(),
		 url: doralinks.oai});
	    } else {     // both record found
	      this.pubdata = data;
	      this.pubmodal(
		{type: 'success',
		 citation: data[1].citation});
	    }},
	    data => {    // failed request
	      this.pubmodal(
		{type: 'error',
		 status: data.statusText + '(' + data.status + ')',
		 url: doralinks.oai});
	    });

      } else if (idtyp.doi != null) {
	// check whether that is in DORA
	this.get_dora_id_from_doi.call(this, idtyp.doi)
	  .then(
	    data => {
	      if (data === null) {
		console.log('Not in DORA');
		this.get_crossref_info(idtyp.doi)
		  .then(
		    data => {
		      this.pubdata = [data];
		      this.pubmodal(
			{type: 'success',
			 source: 'xref',
			 citation: this.xref_extract(data)});
		    },
		    data => {
		      this.pubdata = false;
		      this.pubmodal(
			{type: 'error',
			 status: data.responseText,
			 url: 'https://data.crossref.org/' + idtyp.doi});
		    });
	      } else {
		console.log('DORA-ID: '+data);
	      }
	    },
	    data => {
	      console.log('FAIL');
	    });
      } else {
	this.pubdata = false;
	  this.pubmodal(
	    {type: 'error',
	     status: 'not recoginzed as identifyer.',
	     url: '"'+value+'"'});
      }
    }
  };
});
    

      
 //      function report_result(metadata) {
// 	print_test(JSON.stringify(metadata));
//       }
      
//       function print_test(res) {
// 	$( 'div#test ').append(res);
//       }
      
//       function makelinks(dora_id_nr) {
// 	doraread.dora_oai_id = 'eawag:' + dora_id_nr;
// 	doraread.doralink = ('https://www.dora.lib4ri.ch/eawag/islandora/object/'
// 			     + doraread.dora_oai_id);
// 	doraread.dora_oailink = ('https://www.dora.lib4ri.ch/eawag/oai2?' +
// 				 'verb=GetRecord&metadataPrefix=mods&identifier=' +
// 				 doraread.dora_oai_id);
// 	doraread.dora_citationlink = ('https://www.dora.lib4ri.ch/eawag/islandora/object/' +
// 				      doraread.dora_oai_id + '/islandora_scholar_citation/' +
// 				      '?citation_style=APA');
//       }

//       function getcitation(metadata, citationlink) {
// 	$.ajax(citationlink, {
// 	  dataType: 'json',
// 	  success: function(data, code, jqXHR) {
// 	    metadata['citation'] = $(data['citation']).children( 'div.csl-entry' ).text();
// 	    metadata['citation'] = 'Data for: ' + metadata['citation'];
// 	    metadata['citation'] = metadata['citation'].replace(doraread.re_removedoi, '');
// 	  },
// 	  beforeSend: function() {
// 	    $( '#checkbutton' ).append('<img src="loading-spinner.gif" id="spinner" />');
// 	  },
// 	  complete: function() {
// 	    $( '#spinner' ).remove();
// 	    report_result(metadata);
// 	  }
// 	});
//       }
      
//       function getmetadata (metadata, oailink) {
// 	$.ajax(oailink, {
// 	  dataType: 'xml',
// 	  success: function(data, code, jqXHR) {
// 	    metadata = modsextract($( data ));
// 	    if (metadata['error']) {
// 	    report_result(metadata);
// 	    } else {
// 	      getcitation(metadata, doraread.dora_citationlink);
// 	    }
// 	  },
// 	  beforeSend: function() {
// 	    $( '#checkbutton' ).append('<img src="loading-spinner.gif" id="spinner" />');
// 	  },
// 	  complete: function() {
// 	    $( '#spinner' ).remove();
// 	  }
// 	});
//       }
 
//       function modsextract(d) {
// 	var metadata = {title: '', authors: [], doi: '', year: ''
// 			, abstract: '', citation: '', error: ''};
// 	var mods;
// 	var namelist;
// 	var error;
// 	error = d.find( 'error' );
// 	if (error.length > 0) {
// 	  return({error: error.attr('code')});
// 	}
// 	mods = d.find( 'mods' );
// 	metadata['title'] = mods.children('titleinfo').children('title').text();
// 	namelist = mods.find( 'name' );
// 	$.each(namelist, function(idx, obj) {
// 	  metadata['authors'][idx] = {
// 	    given:$(obj).children( 'namepart[type="given"]' ).text()
// 	  };
// 	  metadata['authors'][idx]['family'] =
// 	    $(obj).children( 'namepart[type="family"]' ).text();
// 	});
// 	metadata['doi'] = mods.find( 'identifier[type="doi"]' ).text();
// 	metadata['year'] = mods.find( 'originInfo dateIssued' ).text();
// 	metadata['abstract'] = mods.find( 'abstract' ).text();
// 	return(metadata);
//       }


//     }
//   };
// });

      
  



