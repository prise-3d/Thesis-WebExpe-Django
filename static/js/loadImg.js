window.onload = function () {

    console.log("End expe " + END_EXPE)

    // only if not end of expe
    if (END_EXPE == "False"){
        setTimeout(function(){ 
            document.getElementById("expeImg").style.display = "inline";
        }, 500);
    }

    // redirect if end of expe after 5 sec
    if (END_EXPE == "True"){
        
        for(var i=0; i<6; i++){
            ((x)=>{
                setTimeout(()=> 
                    document.getElementById("refreshTime").textContent = 5 - x
                ,1000 * i)
            })(i);
        } 

        setTimeout(function(){ 
            window.location = baseUrl
        }, 5000);
    }
}
