// implement `key` events
document.onkeydown = checkKey;

// Utils informations
var KEYCODE_Q           = '81'
var KEYCODE_ENTER       = '13'

urlParams = new URLSearchParams(window.location.search);

var scene = urlParams.get('scene')
var expe  = urlParams.get('expe')

console.log(expeUrl)

function checkKey(e) {

   e = e || window.event;

   if (e.keyCode == KEYCODE_Q) {
        // `q` for quit expe
        console.log('`q` key is pressed')
        window.location = ''
   }
   else if (e.keyCode == KEYCODE_ENTER) {

        // right arrow
        var params = "?scene=" + scene + "&expe=" + expe + "&iteration=0"
        console.log(expeUrl + params)
        window.location = expeUrl + params
   }
}