// https://stackoverflow.com/questions/20756042/javascript-how-to-display-image-from-byte-array-using-javascript-or-servlet

window.onload = function () {
    console.log('Load img here...');


    /*img_data = document.getElementById('expeImg').getAttribute('data-img');
    img_data = JSON.parse(img_data);

    var p = new PNGlib(800, 800, 256); // construcor takes height, weight and color-depth
    var background = p.color(0, 0, 0, 0); // set the background transparent

    for (var i = 0; i < 800; i++){
        for (var j = 0; j < 800; j++){

            let r = img_data[i][j][0]
            let g = img_data[i][j][1]
            let b = img_data[i][j][2]

            p.buffer[i, j] = p.color(r, g, b)
        }
    }
    console.log('done')

    document.getElementById('expeImg').src = "data:image/png;base64,"+p.getBase64();*/
}
