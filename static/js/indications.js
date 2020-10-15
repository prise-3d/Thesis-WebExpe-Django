// Utils informations
const KEYCODE_Q     = 81
const KEYCODE_ENTER = 13
const KEYCODE_LEFT_ARROW  = 37
const KEYCODE_RIGHT_ARROW = 39

urlParams = new URLSearchParams(window.location.search)

var scene      = urlParams.get('scene')
const expe     = urlParams.get('expe')
var example    = urlParams.get('example')

if (example == null || example == ''){
     example = 0
}

if (scene === null || scene === ''){
     scene = document.getElementsByName('scene_name')[0].value
}

const checkKey = e => {
     if (e.keyCode === KEYCODE_Q) {
          // `q` to quit expe
          console.log('`q` key is pressed')
          window.location = ''
     }
     else if (e.keyCode === KEYCODE_ENTER) {
          // enter key

          // check if form is used for this generated page
          if (document.forms.length > 0){
               e.preventDefault()
               form = document.forms['form-indications']

               // check field we want
               names = ['gender', 'birth', 'nationality']
               if (prolific == 1 || prolific == '1'){
                   names = ['gender', 'birth', 'nationality', 'experimentId']
               }
               formError = false

               for (name of names){     
                    if (form[name].value == ""){
                         formError = true
                    }
               }
               
               if (formError){
                    alert('Please fill the required fields correctly')
               }
               else{
                    form.submit()
               }
          }
          else{
               const experimentId = document.getElementsByName('experimentId')[0].value
               const params = `?scene=${scene}&expe=${expe}&experimentId=${experimentId}&iteration=0`
               console.log(expeUrl + params)
               window.location = expeUrl + params
          }
     }
     else if (e.keyCode === KEYCODE_LEFT_ARROW || e.keyCode === KEYCODE_RIGHT_ARROW) {
          // increment number of example
          example = parseInt(example) + 1
          
          // construct url with params for experiments
          const params = `?scene=${scene}&expe=${expe}&example=${example}`
          window.location = indicationsUrl + params
     }
}

// implement `key` events
document.addEventListener('keydown', checkKey)

if (document.forms.length > 0){

     form = document.forms['form-indications']

     form.addEventListener('submit', function(e){
          
          e.preventDefault()

          // check field we want
          names = ['gender', 'birth', 'nationality']
          if (prolific == 1 || prolific == '1'){
              names = ['gender', 'birth', 'nationality', 'experimentId']
          }
          formError = false

          for (name of names){     
               if (form[name] != undefined && form[name].value == ""){
                    formError = true
               }
          }
          
          if (formError){
               alert('Please fill the required fields correctly')
          }
          else{
               form.submit()
          }
     })
}

