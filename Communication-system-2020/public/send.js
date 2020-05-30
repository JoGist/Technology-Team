import {connetti} from "./modulo.js";
import {sendData} from "./modulo.js";
import {disconnetti} from "./modulo.js";

var socket;
//avendo dichiarato questo file come module (quando lo importiamo come script nel file html),
// è necessario dichiarare con window ogni variabile o funzione dichiarata qui dentro, altrimenti il file html non li vede
window.connetti = function connettiImportata(ip, porta) {
  socket = connetti(ip, porta);
}
window.sendData = function sendDataImportata(data, toRover, socket) {
  sendData(data, toRover, socket);
}
window.disconnetti = function disconnettiImportata() {
  disconnetti(socket);
}

socket = connetti("localhost", "80");

window.bottone = function bottone(rover){
  let data = document.getElementById("inputData").value;
  sendData(data, rover, socket);
}
socket.on("dataToGS", (data)=>{           //questo viene eseguito quando la groundstation riceve i dati dal server del rover
  let realdata = JSON.parse(data);
  document.getElementById("roverData").innerHTML= "";
  for(const field in realdata){
    document.getElementById("roverData").innerHTML+= "<li>"+field+': '+realdata[field]+"</li>";
  };
});


socket.on("updateRoverList", (roverArray)=>{            /*il server comunica, tramite updateRoverList, che la lista rover online è cambiata e quindi questo script aggiorna i bottoni della pagina*/
  if(roverArray.length===0){
    document.getElementById("roverList").innerHTML="<li>Nessuno</li>";
  }else{
    document.getElementById("roverList").innerHTML="";
    for(const rover in roverArray){
      document.getElementById("roverList").innerHTML+= "<button style='padding:20px; font-size:20px' onclick='bottone("+'"'+roverArray[rover]+'"'+")'>"+roverArray[rover]+"</button>";
    };
  }
});

