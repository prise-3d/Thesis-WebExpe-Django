// implement `key` events
document.onkeydown = checkKey;

urlParams = new URLSearchParams(window.location.search);

// Utils informations
var KEYCODE_Q           = '81'
var KEYCODE_ENTER       = '13'
var KEYCODE_LEFT_ARROW  = '37'
var KEYCODE_RIGHT_ARROW = '39'

// get params if exists
if (urlParams.has('scene')){

   var scene = urlParams.get('scene')
   var expe  = urlParams.get('expe')
}

function checkKey(e) {

   e = e || window.event;

   if (e.keyCode == '81') {
      // `q` for quit expe
      console.log('`q` key is pressed')
      window.location = baseUrl
   }
   else if (e.keyCode == '13') {

      // check if experience is begin
      if (!BEGIN_EXPE){

         console.log(window.location.href + "&begin=true")
         // right arrow
         window.location = window.location.href + "&begin=true"
      } 
   }
   else if (e.keyCode == '37' || e.keyCode == '39'){

      // only do something is experience is begin
      if (BEGIN_EXPE){
         var answer;

         // left arrow key
         if (e.keyCode == '37'){
            console.log('left arrow is pressed')
            answer = '1'
         }

         // right arrow key
         if (e.keyCode == '39'){
            console.log('right arrow is pressed')
            answer = '0'
         }

         var iteration = 0;

         // update of iteration if exists
         if (urlParams.has('iteration')){
            iteration = urlParams.get('iteration')

            // increment step
            iteration++;
         }
         
         // construct url with params for experience
         var params = "?scene=" + scene + "&expe=" + expe + "&iteration=" + iteration + "&answer=" + answer
         console.log(expeUrl + params)
         window.location = expeUrl + params
      }
   }
}