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
      // check if experiments is begin
      if (!BEGIN_EXPE) {
         // right arrow
         window.location = window.location.href + '&begin=true'
      } 
   }
   else if (e.keyCode === KEYCODE_LEFT_ARROW || e.keyCode === KEYCODE_RIGHT_ARROW) {
      // only do something is experiments has begun
      if (BEGIN_EXPE && !END_EXPE) {
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
         
         // check if checkbox is present
         var validation_checkbox =  document.getElementById('validation_checkbox')

         if (typeof(validation_checkbox) != 'undefined' && validation_checkbox != null)
         {
            if(validation_checkbox.checked)
            {
               // construct url with params for experiments
               const params = `?scene=${scene}&expe=${expe}&iteration=${iteration}&answer=${answer}&check=true`
               window.location = expeUrl + params
            }
            else{
               alert('You need to check the box before continuing')
            }
         }
         else
         {
            // construct url with params for experiments
            const params = `?scene=${scene}&expe=${expe}&iteration=${iteration}&answer=${answer}&check=false`
            window.location = expeUrl + params
         }
      }
   }
}

// implement `key` events
document.addEventListener('keydown', checkKey)


// avoid back button return 30 times... (Need to improve this..)
for (var i = 0; i < 30; i++){
   window.history.pushState({isBackPage: false, }, document.title, location.href)
}