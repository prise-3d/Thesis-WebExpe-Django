function toggle(elem) {
    if (elem.style.display === "none") {
        elem.style.display = "block";
      } else {
        elem.style.display = "none";
      }
}


window.onload = function () {

    elems = document.getElementsByClassName('date-folder-list')
    
    for (let item of elems) {

        item.onclick = function(event){
            event.preventDefault()
            list = item.children[0].children[1]
            toggle(list)
        }
    }
}