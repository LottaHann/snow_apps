
function button (){
    alert("booton");
}



    function selectedPerson(name) {
        const container = document.getElementById('main-contact');
        if (name === "Dennis Biström") {
            container.innerHTML = "";
            fetch('../template/contact/bistrom.html')
                .then(response => response.text())
                .then(html => {
                    // Once the HTML is fetched, insert it into a DOM element
                    container.innerHTML = html;
                })
                .catch(error => {
                    console.error('Error fetching HTML:', error);
                });
        }

        if (name === "Leonardo Espinosa-Leal") {
            container.innerHTML = "";
            fetch('../template/contact/Leonardo Espinosa-Leal.html')
                .then(response => response.text())
                .then(html => {
                    // Once the HTML is fetched, insert it into a DOM element
                    container.innerHTML = html;
                })
                .catch(error => {
                    console.error('Error fetching HTML:', error);
                });
        }

        if (name === "christa-name") {
            container.innerHTML = "";
            fetch('../template/contact/christa.html')
                .then(response => response.text())
                .then(html => {
                    // Once the HTML is fetched, insert it into a DOM element
                    container.innerHTML = html;
                })
                .catch(error => {
                    console.error('Error fetching HTML:', error);
                });
        }

        if (name === "Andrey Shcherbakov") {
            container.innerHTML = "";
            fetch('../template/contact/andrey.html')
                .then(response => response.text())
                .then(html => {
                    // Once the HTML is fetched, insert it into a DOM element
                    container.innerHTML = html;
                })
                .catch(error => {
                    console.error('Error fetching HTML:', error);
                });
        }

   
        
        if (name === "Magnus Westerlund") {
            container.innerHTML = "";
            fetch('../template/contact/Magnus Westerlund.html')
                .then(response => response.text())
                .then(html => {
                    // Once the HTML is fetched, insert it into a DOM element
                    container.innerHTML = html;
                })
                .catch(error => {
                    console.error('Error fetching HTML:', error);
                });
        }
        if (name === "Matteo Stocchetti") {
            container.innerHTML = "";
            fetch('../template/contact/Matteo Stocchetti.html')
                .then(response => response.text())
                .then(html => {
                    // Once the HTML is fetched, insert it into a DOM element
                    container.innerHTML = html;
                })
                .catch(error => {
                    console.error('Error fetching HTML:', error);
                });
        }

        

        if (name === "Jonas Irjala") {
            container.innerHTML = "";
            fetch('../template/contact/Jonas Irjala.html')
                .then(response => response.text())
                .then(html => {
                    // Once the HTML is fetched, insert it into a DOM element
                    container.innerHTML = html;
                })
                .catch(error => {
                    console.error('Error fetching HTML:', error);
                });
        }
        
    }

    function selectedPerson2(){
        container.innerHTML = person1HTML ;
    }



function contact(){
    fetch('../template/contact/people.html')
    .then(response => response.text())
    .then(html => {
        // Once the HTML is fetched, insert it into a DOM element
        // const container = document.getElementById('contact-people');
        const container = document.getElementById('main-contact');
        container.innerHTML = html;
    })
    .catch(error => {
        console.error('Error fetching HTML:', error);
    });
}



function arcada(){
  
    fetch('../template/arcada/arcada.html')
    .then(response => response.text())
    .then(html => {
        // Once the HTML is fetched, insert it into a DOM element
        const container = document.getElementById('content-arcada');
        container.innerHTML = html;
    })
    .catch(error => {
        console.error('Error fetching HTML:', error);
    });
}

function info(){
  
    fetch('../template/info/info.html')
    .then(response => response.text())
    .then(html => {
        // Once the HTML is fetched, insert it into a DOM element
        const container = document.getElementById('content-info');
        container.innerHTML = html;
    })
    .catch(error => {
        console.error('Error fetching HTML:', error);
    });
}

async function SendFaceName(int){
    //  url exemple = http://127.0.0.1:4000/face?name=smile
    
    if(int == "" || int>= 9){
        int = 0;
    }
    console.log(int);
    // http://localhost:5000/api/post?face=${faceInput.value}
    API_URL = "http://localhost:5100/api/post?touch="
    let default_face_name= "from robot js"
    let faces = ["smile", "neutral", "sad","hearth","wink","angry","smile3","bigsmile","suprise"];
    console.log("sendt default_face_name : "+faces[int]);

    const response = await fetch(API_URL + faces[int]);

    //const response = await fetch(`http://localhost:5000/api/post?face=${face.value}`);
    if (!response.ok) {
        console.log("Something went wrong.");
        return;
    }
    const data = await response.text();
    if (data === "OK") {
        console.log("SUCCESS");
        console.log("sendt face name : "+faces[int]);
    }
}

// SendFaceName();

document.addEventListener('DOMContentLoaded', function() {
    var clickableDiv = document.querySelector('.contact-div');
    
    if (clickableDiv) {
        clickableDiv.addEventListener('click', function() {
            // Redirect to the desired URL
            window.location.href = './contact';
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var clickableDiv = document.querySelector('.info-div');
    
    if (clickableDiv) {
        clickableDiv.addEventListener('click', function() {
            // Redirect to the desired URL
            window.location.href = './info';
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var clickableDiv = document.querySelector('.arcada-div');
    
    if (clickableDiv) {
        clickableDiv.addEventListener('click', function() {
            // Redirect to the desired URL
            window.location.href = './arcada';
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var clickableDiv = document.querySelector('.techlabs-div');
    
    if (clickableDiv) {
        clickableDiv.addEventListener('click', function() {
            // Redirect to the desired URL
            window.location.href = './techlabs';
        });
    }
});

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function myFunction(int) {
    console.log('Start'); // This message will be logged immediately
    await delay(int); // Wait for 7000 milliseconds (7 seconds)
    console.log('End'); // This message will be logged after the delay of 7 seconds
}

// snow  button clickable
var clickableImage = document.querySelector('.clickable-image-snow');
if(clickableImage){
    const audioPlayer = new Audio('../audio/Snow_talking.mp3');
    clickableImage.addEventListener('click',async function(event) {
        event.preventDefault(); // Prevent the default link behavior
        SendFaceName(8);
        audioPlayer.play();
        await myFunction(10000);
        SendFaceName(0);
    });
}


var clickableImageArcada = document.querySelector('.clickable-image-arcada');
if(clickableImageArcada){
    const audioPlayerArcada = new Audio('../audio/arcada_talking.mp3');
    clickableImageArcada.addEventListener('click', async function(event) {
        event.preventDefault(); // Prevent the default link behavior
        SendFaceName(8);
        audioPlayerArcada.play();
        await myFunction(17000);
        SendFaceName(0);
    });
}

var clickableImageBistrom = document.querySelector('.clickable-image-bistrom');
if(clickableImageBistrom){
    const audioPlayerArcada = new Audio('../audio/Bistrom.mp3');
    clickableImageArcada.addEventListener('click', function() {
        audioPlayerArcada.play();
        alert("dennis");
        //SendFaceName(6);
    });
}





// techlabs image button
var clickableImageTechlabs = document.querySelector('.clickable-image-techlabs');
if(clickableImageTechlabs){
    const audioPlayerTechlabs = new Audio('../audio/techlabs_talking.mp3');
    clickableImageTechlabs.addEventListener('click',  async function(event) {
        event.preventDefault(); 
        SendFaceName(8);
        audioPlayerTechlabs.play();
        await myFunction(17000);
        SendFaceName(0);
    });
}


//  Exit button with robot face interactions 
var clickableImageExit = document.querySelector('.clickable-image-Exit');
if(clickableImageExit){
    console.log("clickable-image-Exit");
//    clickableImageExit.addEventListener('click',  async function(event) {
//     event.preventDefault(); // Prevent the default link behavior
//        console.log("clickableImageExit");
//         SendFaceName(2);
//         await myFunction(1000);
//          SendFaceName(0);
//          await myFunction(500);
//          window.location.href = "../";
//     });
}

// SendFaceName(0);
console.log("robot ");

