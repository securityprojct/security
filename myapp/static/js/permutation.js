class permutations {
    inverse = (perm) => {
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
    }
    treans = (text) => {
        var value = text.toUpperCase();
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
            for (var k in values) array.push([k, values[k]]);
            array.sort(function(a, b) {
                a = (+a[1]==a[1] ? +a[1] : 1000000000+a[1].charCodeAt(0) );
                b = (+b[1]==b[1] ? +b[1] : 1000000000+b[1].charCodeAt(0) );
                return a > b ? 1 : a < b ? -1 : 0;
            });
            $(array).each(function(key,val) {permutation.push(val[0]*1+1);});
        }
        else {
            permutation = values;
        }
        var permutation_inverse = this.inverse(permutation);
            console.log(permutation_inverse);
        //if (permutation.length) this._text.html(permutation_inverse.join(','));
        let thekey = value;
        var json_data = JSON.stringify({'permutation':permutation, 'key':thekey});
        return json_data
    }
}
document.getElementById("key").addEventListener("input", e => {
    console.log(JSON.parse(new permutations().treans(e.currentTarget.value)).permutation.join(","));
    document.getElementById("pkey").attributes.value.value = JSON.parse(new permutations().treans(e.currentTarget.value)).permutation.join(",");
})