function toggle(elem) {
    if (elem.style.display === "none") {
        elem.style.display = "block";
      } else {
        elem.style.display = "none";
      }
}

function toggleClass(elem, class1, class2) {
    if (elem.className === class1) {
        elem.className = class2;
      } else {
        elem.className = class1;
      }
}

// use for call route to dowload content (as post request)
function downloadContent(path){

    const csrfToken = document.querySelectorAll('[name=csrfmiddlewaretoken]')[0].value

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/admin/download", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.setRequestHeader("X-CSRFToken", csrfToken);

    xhttp.onreadystatechange = function (){
        if (xhttp.readyState == 4 && xhttp.status == 200) {

            // Try to find out the filename from the content disposition `filename` value
            var disposition = xhttp.getResponseHeader('content-disposition');

            // expe is find from django
            var filename = expe_name + "_" + disposition.split('=')[1]
      
            var blob = new Blob([xhttp.response], {type: "octet/stream"});
            saveAs(blob, filename);
        }
    };
    xhttp.responseType = "arraybuffer";
    xhttp.send("path=" + path); 
}


window.onload = function () {

    // Display list of files from day folder
    elems = document.getElementsByClassName('date-folder-list')
    
    for (let item of elems) {

        item.onclick = function(event){
            event.preventDefault()
            currentElem = event.currentTarget

            // get list element
            list = currentElem.parentElement.nextElementSibling
            
            // display or hide list elements
            toggle(list)

            // toggle arrow class for display effect
            iconElem = currentElem.children[0]
            toggleClass(iconElem, 'fas fa-arrow-circle-right', 'fas fa-arrow-circle-down')
        }
    }


    elems = document.getElementsByClassName('download-list')

    for (let downloadElem of elems) {

        downloadElem.onclick = function(event){
            event.preventDefault()

            currentElem = event.currentTarget
            pathDownload = currentElem.getAttribute('data-download-path')

            downloadContent(pathDownload)
        }
    }
}