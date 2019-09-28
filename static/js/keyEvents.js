// Utils informations
const KEYCODE_Q           = 81
const KEYCODE_ENTER       = 13
const KEYCODE_LEFT_ARROW  = 37
const KEYCODE_RIGHT_ARROW = 39

urlParams = new URLSearchParams(window.location.search)

const scene = urlParams.get('scene')
const expe  = urlParams.get('expe')

const checkKey = e => {
   if (e.keyCode === KEYCODE_Q) {
      // `q` to quit expe
      console.log('`q` key is pressed')
      window.location = baseUrl
   }
   else if (e.keyCode === KEYCODE_ENTER) {
      // check if experience is begin
      if (!BEGIN_EXPE) {
         // right arrow
         window.location = window.location.href + '&begin=true'
      } 
   }
   else if (e.keyCode === KEYCODE_LEFT_ARROW || e.keyCode === KEYCODE_RIGHT_ARROW) {
      // only do something is experience has begun
      if (BEGIN_EXPE) {
         let answer

         // left arrow key
         if (e.keyCode === KEYCODE_LEFT_ARROW) {
            console.log('left arrow is pressed')
            answer = '1'
         }

         // right arrow key
         if (e.keyCode === KEYCODE_RIGHT_ARROW) {
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
         window.location = expeUrl + params
      }
   }
}

// implement `key` events
document.addEventListener('keydown', checkKey)
