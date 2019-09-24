const delay = ms => new Promise(res => setTimeout(res, ms))

window.addEventListener('DOMContentLoaded', async () => {
    console.log('End expe ' + END_EXPE)
    
    // only if not end of expe
    if (END_EXPE === 'False') {
        await delay(500)
        document.getElementById('expeImg').style.display = 'inline'
    }
    // redirect if end of expe after 5 sec
    else if (END_EXPE === 'True') {
        for (const i = 0; i <= 5; i++) {
            document.getElementById('refreshTime').textContent = 5 - i
            if (i <= 4) await delay(1000)
        }
        window.location = baseUrl
    }
})
