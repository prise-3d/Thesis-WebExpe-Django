// Download endpoint response as a file using a POST request
function updateSession(route, value){

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value
    const updateUrl = BASE === '' ? `/${route}` : `/${BASE}/${route}`

    fetch(updateUrl, {
        method: 'POST',
        body: `value=${value}`,
        headers: {
            'Content-type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        }
    }).then(async res => {
        console.log('success udpate')
    })
}

function updateData() {

    // access storage
    const localStorage = window.localStorage;

    var expes_corrected = scenes.toString('utf8').replace(/\&quot;/g, '"' )
    var expes_json = JSON.parse(expes_corrected)

    var contructed_json = {}
    // prepare default data
    for(var expe in expes_json) {

        // contruct object
        contructed_json[expe] = {}

        for(var scene in expes_json[expe]) {

            // get name and contruct object
            scene_name = expes_json[expe][scene]
            contructed_json[expe][scene_name] = {'done': false}
        }
    }

    // contruct new storage data and update session data (if new expe and scenes used)
    // contains user advancement
    var finalJson = {}

    if (localStorage.getItem('p3d-user-expes')){
        expes = JSON.parse(localStorage.getItem('p3d-user-expes'))
        
        // fusion of data
        for(var expe in contructed_json) {

            finalJson[expe] = {}

            // if experience exists
            if (expes[expe]){
                
                for(var scene in contructed_json[expe]) {

                    // check if scenes already exists
                    if (expes[expe][scene]){
                        finalJson[expe][scene] = expes[expe][scene]
                    }
                    else
                    {
                        finalJson[expe][scene] = contructed_json[expe][scene]
                    }
                }
            }
            else{
                finalJson[expe] = contructed_json[expe]
            }
        }
    }
    else{
        finalJson = contructed_json
    }
    
    // update storage data
    localStorage.setItem('p3d-user-expes', JSON.stringify(finalJson))

    // now store into session data information
    if(localStorage.getItem('p3d-user-id')){
        
        // update data into request.session object
        updateSession('update_session_user_id', localStorage.getItem('p3d-user-id'))
    }

    // update data into request.session object
    updateSession('update_session_user_expes', JSON.stringify(finalJson))
}

window.addEventListener('DOMContentLoaded', () => {
    updateData()
})