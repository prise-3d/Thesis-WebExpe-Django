// implement `key` events
document.addEventListener('keydown', checkKey)

urlParams = new URLSearchParams(window.location.search);

// Utils informations
const KEYCODE_Q           = '81'
const KEYCODE_ENTER       = '13'
const KEYCODE_LEFT_ARROW  = '37'
const KEYCODE_RIGHT_ARROW = '39'

// get params if exists
if (urlParams.has('scene')) {
   var scene = urlParams.get('scene')
   var expe  = urlParams.get('expe')
}

const checkKey = e => {
   e = e || window.event

   if (e.keyCode === '81') {
      // `q` to quit expe
      console.log('`q` key is pressed')
      window.location = baseUrl
   }
   else if (e.keyCode === '13') {
      console.log("Here")
      // check if experience is begin
      if (!BEGIN_EXPE) {
         console.log("And Here")
         // right arrow
         window.location = window.location.href + '&begin=true'
      } 
   }
   else if (e.keyCode === '37' || e.keyCode === '39') {
      // only do something is experience is begin
      if (BEGIN_EXPE) {
         let answer

         // left arrow key
         if (e.keyCode === '37') {
            console.log('left arrow is pressed')
            answer = '1'
         }

         // right arrow key
         if (e.keyCode === '39') {
            console.log('right arrow is pressed')
            answer = '0'
         }

         let iteration = 0

         // update of iteration if exists
         if (urlParams.has('iteration')) {
            iteration = urlParams.get('iteration')

            // increment step
            iteration++
         }
         
         // construct url with params for experience
         const params = `?scene=${scene}&expe=${expe}&iteration${iteration}&answer=${answer}`
         window.location = baseExpeUrl + params
      }
   }
}
