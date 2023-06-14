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
	  element.keypress(function(e) {
		if (e.which === 13) {
		  module.main.call(module);
		}
	  });
		} )(this.el);
		this.el.after($(this.modal_html));
		$('#pubmodal_button_right').click(this.prefill.bind(this));
	  },
  
	  spinner: '<i class="icon-spinner icon-spin"></i>',
  
	  pubdata: {},
  
	  prefill: function() {
		if ($.isEmptyObject(this.pubdata)) {return;}
		var metadata = {title: '', authors: [], doi: '',
				year: '', abstract: '', keywords: [] };
		if (this.pubdata[0]['source'] === 'xref') {
	  metadata = this.pubdata[0];
	  metadata.title = 'Data for: ' + metadata.title;
	  metadata.keywords = [];
		} else {
	  var mods = $(this.pubdata[0]).find('mods');
	  metadata['title'] = 'Data for: '
		+ mods.children('titleinfo').children('title').text();
	  metadata.title = metadata.title.replace(/<\/?[^>]+(?:>|$)/g, "");
	  var namelist = mods.children('name[type="personal"]');
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
		// collect all author fields and iterate over all author fields
		var authorfields = $('input[id^=field-author-]');
		let appendto = authorfields.last().parents('div.control-repeating').parent();
		for (const au of metadata.authors.entries()) {
	  let val = au[1]['family'] + ', ' + au[1]['given'];
	  if (authorfields.length === 0) {
		let aunum = au[0] + 1;
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
	  } else {
		authorfields.first().val(val);
		authorfields = authorfields.slice(1);
	  }
		}
		authorfields.parent().parent().parent().remove();
	  },
	  
	  normalize_doraid: function(id) {
		return(id.replace('%3A', ':'));
	  },
  
	  identpub : function(value) {
		var regdora = /.*(eawag:\d+$|.*eawag%3A\d+$)/;
		var regdoi = /.*(10.\d{4,9}\/.+$)/;
		var ids = {};
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
		var slashreplace = /\//g;
		var doradoi = doi.replace(slashreplace, '%5C~slsh~');
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
		+ 'If that is not the right one, just click "Discard" and continue.'
			+ '<br />Clicking "OK, Fill in metadata!" will overwrite any ' 
		+ 'preexisting entries.</div>';
	  $('#pubmodal_header').addClass('alert-success');
	  $('#pubmodal_title').html('success');
	  $('#pubmodal_main').html(maintext);
	  $('#pubmodal_button_left').html('Discard').addClass('btn-warning').show();
	  $('#pubmodal_button_right').html('OK, Fill in metadata!').addClass('btn-success').show();
	  
		}
		$('#pubmodal').modal('show');
	
	  },
  
	  modal_html:
  `<div id="pubmodal" class="modal fade" role="dialog">
	<div class="modal-dialog" role="document">
	<div class="modal-content">
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
	</div>
	</div>
   </div>`,
  
	  xref_extract: function(data) {
		let metadata = {};
		metadata.authors = data.author;
		metadata.aunames = data.author.map(el => {
	  return(el.family + ', ' + el.given);});
		metadata.citauthors = metadata.aunames.join(', ');
		metadata.title = data.title;
		metadata.abstract = data.abstract || '';
		metadata.year = data.created['date-parts'][0][0];
		metadata.journal = '<i>' + data['container-title'] + '</i>';
		metadata.page = data.page;
		metadata.volume = data.volume;
		metadata.issue = data.issue;
		metadata.doi = `https://doi.org/${data.DOI}`;
		let citation = `${metadata.citauthors} (${metadata.year}). `
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
		var idtyp = this.identpub.call(this, value);
		if (idtyp.dora_id !== null) {
	  // get the dora record and citation
	  doralinks = this.mkdoralinks(idtyp.dora_id);
	  this.get_dora_info(doralinks)
		.then(
		  data => {
		  //OAI-record and citation request both did not fail.
		  //check if OAI-PMH record contains error
			let error = $(data[0]).find('error');
			if (error.length > 0) {
		  this.pubdata = {};
		  this.pubmodal(
			{type: 'error',
			status: error.text(),
			url: doralinks.oai});
			} else {
			// if no OAI - error we believe citation went also well.
		  this.pubdata = data;
		  this.pubmodal(
			{type: 'success',
			citation: data[1].citation});
			}
		  },
		  // Either OAI- or citation request failed
		  data => {
			this.pubdata = {};
			this.pubmodal(
		  {type: 'error',
		   status: data.statusText + '(' + data.status + ')',
		   url: doralinks.oai});
		  }
		);
		} else if (idtyp.doi != null) {
	  // A DOI was enterd as identifyer
	  // check whether that is in DORA
	  this.get_dora_id_from_doi.call(this, idtyp.doi)
		.then(
		  data => {
			if (data === null) {
			// The DOI is not in DORA
		  this.get_crossref_info(idtyp.doi)
			.then(
			  data => {
				// Crossref request returns successful
				this.pubdata = [data];
				this.pubmodal(
			  {type: 'success',
			   source: 'xref',
			   citation: this.xref_extract(data)});
			  },
			  data => {
			  // Crossref request failed
				this.pubdata = {};
				this.pubmodal(
			  {type: 'error',
			   status: data.responseText,
			   url: 'https://data.crossref.org/' + idtyp.doi});
			  }
			);
			} else {
			// The DOI was found in DORA
		  this.el.val(data);
		  this.main();
			}
		  },
		  data => {
		  // Calling get_dora_id_from_doi failed
			console.log('Calling get_dora_id_from_doi failed');
			console.log('data:\n' + data);
		  }
		);  // end of then
		} else {
		// Input is no identifyer
	  this.pubdata = {};
		this.pubmodal(
		  {type: 'error',
		   status: 'not recoginzed as identifyer.',
		   url: '"'+value+'"'});
		}
	  } // end of main()
	};  // end of module
  });   // end of module definition
  