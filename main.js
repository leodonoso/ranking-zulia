// Definir arrays vacios globalmente para poder llenarlos con la informacion que queremos enviar a la base de datos

let gamertags = [];
let standings = [];
let placings = [];

// Definir la clase "placing" para poder generar los objetos que iran dentro del JSON que mandaremos a mongoDB

class placing {
    constructor(standing, gamertag) {
        this.standing = standing;
        this.gamertag = gamertag;
    }
}

// Carga un archivo HTML guardado localmente y lo inyecta a un div

function loadHtml (id, filename) {
    console.log(`div id: ${id}, filename: ${filename}`);

    let xhttp;
    let element = document.getElementById(id);
    let file = filename;

    if (file) {
        xhttp = new XMLHttpRequest();

        xhttp.onreadystatechange = function() {
            if (this.readyState == 4) {
                if (this.status == 200) {element.innerHTML = this.responseText;}
                if (this.stauts == 404) {element.innerHTML = "<h1>Page not found.</h1>";}
            }
        }
        xhttp.open("GET", `assets/${file}`, true);
        xhttp.send();
        return;
    }
}

// Llena el array vacio de Standings que declaramos al principio con la informacion correcta

function displayStandings () {
    let standingElements = document.querySelectorAll('tbody>tr');
    const regexNumeros = /\d/g;

    // Llenar Standings
    for (index in standingElements) {
        let _standingsRaw = standingElements[index].firstElementChild.firstElementChild.firstElementChild.firstElementChild.innerText;

        let _standingsArray = _standingsRaw.match(regexNumeros);
        let _standings = _standingsArray.join('')

        standings.push(parseInt(_standings));
    }
}

// Llena el array vacio de Gamertags que declaramos al principio con la informacion correcta

function displayGamertags () {
    let gamertagElements = document.querySelectorAll("[data-test='gamertag']");
    const regexLetras = /\w-?/g;

    // Llenar Gamertags
    for (index in gamertagElements) {
        let _gamertagsRaw = gamertagElements[index].innerText;

        _gamertags = _gamertagsRaw.match(regexLetras);
        gamertags.push(_gamertags.join(''));
    }
}

// Llena el array vacio de Placings con objetos construidos de la clase creada al principio, a partir de la data guardada en los 
// arrays Standings y Placings.

function populatePlacings () {
    let uniqueGamertags = [...new Set(gamertags)]

    for (index in standings) {
        let placingObject = new placing(standings[index], uniqueGamertags[index]);
        placings.push(placingObject);
    }

    let placingsJSON = JSON.stringify(placings);

    console.log(placingsJSON);
}

// Ejecuta la funcion loadHTML en todos los archivos necesarios.

function loadPages () {
    loadHtml("page1","Tomodachi_page1.html");
}

// Arreglos frontend

const fileBtn = document.getElementById("file-btn");
const realFile = document.getElementById("real-file");
const customText = document.getElementById("custom-text");

fileBtn.addEventListener("click", () => {
    preventDefault();
    console.log('pene');
    realFile.click();
})