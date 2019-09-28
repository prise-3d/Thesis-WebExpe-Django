// Utils informations
const KEYCODE_Q     = 81
const KEYCODE_ENTER = 13

urlParams = new URLSearchParams(window.location.search)

const scene = urlParams.get('scene')
const expe  = urlParams.get('expe')

const checkKey = e => {
     if (e.keyCode === KEYCODE_Q) {
          // `q` to quit expe
          console.log('`q` key is pressed')
          window.location = ''
     }
     else if (e.keyCode === KEYCODE_ENTER) {
          // right arrow
          const params = `?scene=${scene}&expe=${expe}&iteration=0`
          console.log(expeUrl + params)
          window.location = expeUrl + params
     }
}

// implement `key` events
document.addEventListener('keydown', checkKey)
