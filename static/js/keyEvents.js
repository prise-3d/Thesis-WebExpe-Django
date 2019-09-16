// implement `key` events
document.onkeydown = checkKey;

function checkKey(e) {

    e = e || window.event;

    if (e.keyCode == '81') {
        // `q` for quit expe
       console.log('`q` key is pressed');
       window.location = ''
    }
    else if (e.keyCode == '37') {
       // left arrow
       console.log('left arrow is pressed');
    }
    else if (e.keyCode == '39') {
       // right arrow
       console.log('right arrow is pressed');
    }

}