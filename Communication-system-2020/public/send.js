function sendData(toRover){

  /*funzione chiamata dalla pressione dei bottoni sulla pagina html che prende il data dall'input della pagina e lo invia al rover toRover*/

  let data=document.getElementById("inputData").value;

  let messaggio = {
    data: data,
    toRover: toRover
  };

  socket.emit("dataToRover", JSON.stringify(messaggio));  //stringify serve per trasformare l'oggetto in formato JSON per inviarlo
}

socket.on("updateRoverList", (roverArray)=>{            /*il server comunica, tramite updateRoverList, che la lista rover online è cambiata e quindi questo script aggiorna i bottoni della pagina*/
  if(roverArray.length===0){
    document.getElementById("roverList").innerHTML="<li>Nessuno</li>";
  }else{
    document.getElementById("roverList").innerHTML="";
    for(const rover in roverArray){
      document.getElementById("roverList").innerHTML+= "<button style='padding:20px; font-size:20px' onclick='sendData("+'"'+roverArray[rover]+'"'+")'>"+roverArray[rover]+"</button>";
    };
  }
})
