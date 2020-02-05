
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

    const localStorage = window.localStorage;

    // now check if new user, then add session id into local storage
    if(!localStorage.getItem('id')){
        
        localStorage.setItem('id', currentId)
    }

    console.log('expe is finished ? ', expeFinished)
    console.log('expe ', expeName)
    console.log('expe ', sceneName)

    if(expeFinished.toLowerCase() == 'true'){

        console.log('Update of user data...')
        // update storage data
        var user_expes = JSON.parse(localStorage.getItem('user_expes'))

        // set scene of expe has done for current user
        user_expes[expeName][sceneName]['done'] = true

        // update data into request.session object and local storage
        localStorage.setItem('user_expes', JSON.stringify(user_expes))
        updateSession('update_session_user_expes', JSON.stringify(user_expes))
    }
}

window.addEventListener('DOMContentLoaded', () => {
    updateData()
})