//simuliamo che i dati ci vengano inviati dalla ground station. simuliamo questi dati con la funzione creaDati

//per quella che devo scrivere vedo se fare una classe di cui possono fare un'istanza oppure fare un modulo che possono importare
function sendData(messaggio, toRover = null){

  if (toRover == null) {
    toRover = "all";
  }

  let data = {
    toRover: toRover,
    data: messaggio
  }
  
  socket.emit("dataToRover", JSON.stringify(messaggio));
}


function creaDati(toRover){
  let data=document.getElementById("inputData").value;
  let selezione = document.getElementById("selezione").value;

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
      document.getElementById("roverList").innerHTML+= "<button style='padding:20px; font-size:20px' onclick='sendData(\""+roverArray[rover]+"\")'>"+roverArray[rover]+"</button>";
    };
  }
})
