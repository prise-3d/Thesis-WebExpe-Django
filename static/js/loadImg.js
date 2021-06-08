const delay = ms => new Promise(res => setTimeout(res, ms))
var startAnswerTime = undefined;

window.addEventListener('DOMContentLoaded', async () => {
    console.log('End expe ' + END_EXPE)
    
    // only if not end of expe
    if (!END_EXPE) {
        var imgBlock = document.getElementById('expeImg')
        
        if (imgBlock !== null) {
            imgBlock.onload = function() {
                document.getElementById('expeImg').style.display = 'inline'

                // Once image is loaded, the stimulus is then available we can measure the answer time
                startAnswerTime = Date.now();
            }
        }
    }
    // redirect after 5s if end of expe
    /*else if (END_EXPE) {
        for (let i = 0; i <= 5; i++) {
            document.getElementById('refreshTime').textContent = 5 - i
            if (i <= 4) await delay(1000)
        }
        window.location = baseUrl
    }*/
})
