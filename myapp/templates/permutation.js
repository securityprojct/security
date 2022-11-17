var PERMUTATION = PERMUTATION || (function(){
 return {
  init : function(id, name) {
   this._div = $('#'+id).addClass('permutation');
   this._name = name;
   this._size = 0;
   this._key = '';
  },
  
  permutation : function(options) {
   if (options === undefined) options = {};
   if (options.default_value !== undefined) this._key = options.default_value;
   this.draw();
  },
  
  draw : function() {
   this._div.empty();
   this._div.append(this.draw_permutation());
   this._div.append(this.draw_hidden_values());
   this.update_values();
  },

  draw_permutation : function() {
   var this_permutation = this;
   this._input = $('<input>').val(this._key);
   this._input.on('click keyup paste', function(e) {
    this_permutation.update_values();
   });
   this._text = $('<span>').addClass('label');
   return [this._input, this._text];
  },
  
  draw_hidden_values : function() {
   var this_permutation = this;
   this._output = $('<input>').attr('name',this._name).attr('type','hidden').attr('autocomplete','off').attr('data-reload',true);
   this._output.on('reload',function(event, json_data) {
    var permutation = {};
    try { permutation = JSON.parse(json_data || '{}'); } catch (e) { }
    this_permutation._key = permutation.key;
    this_permutation.draw();
   });
   return this._output;
  },

  update_values : function() {
   var value = this._input.val().toUpperCase();
   value = value.replace(/([A-Z])/g,' $1 ');
   var permutation = [];
   var values = value.split(/[^A-Z0-9]/).filter(function(n){ return n.length > 0 });
   if (values.length == 1) values = values.join('').split('');
   var is_permutation = true;
   for (var i = 1; i <= values.length; i++) {
    if ( $.inArray( i.toString(), values ) == -1) { is_permutation = false; break; }
   }
   if (!is_permutation) {
    var array = [];
    for (var k in values) {
     array.push([k, values[k]]);
    }
    array.sort(function(a, b) {
     a = (+a[1]==a[1] ? +a[1] : 1000000000+a[1].charCodeAt(0) );
     b = (+b[1]==b[1] ? +b[1] : 1000000000+b[1].charCodeAt(0) );
     return a > b ? 1 : a < b ? -1 : 0;
    });
    $(array).each(function(key,val) {
     permutation.push(val[0]*1+1);
    });
   }
   else {
    permutation = values;
   }
   this._text.html('');
   var permutation_inverse = this.inverse(permutation);
   if (permutation.length) this._text.html(permutation_inverse.join(','));
   this._key = value;
   var json_data = JSON.stringify({'permutation':permutation, 'key':this._key});
   this._output.val(json_data);
  },
  
  inverse : function(perm) {
   var array = [];
   for (var k in perm) {
    array.push([k, parseInt(perm[k])]);
   }
   array.sort(function(a, b) {
    return a[1] > b[1] ? 1 : a[1] < b[1] ? -1 : 0;
   });
   var permutation_inverse = [];
   $(array).each(function(key,val) {
    permutation_inverse.push(val[0]*1+1);
   });
   return permutation_inverse;
  },
  

 };
}());
