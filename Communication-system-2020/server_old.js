
const express= require("express"),
		appGroundStation = express(),
		appRover = express();

const socket = require('socket.io');

let roverSockets={};									/*oggetto che ha come attributi i nomi con cui si connettono i singoli rover, a cui corrispondono i valori dei socket.id*/

function updateRoverList(){								/*il server comunica alle groundstation i nomi tutti i rover attualmente online. Ovvero gli attributi dell'oggetto roverSockets*/
	groundStations.emit("updateRoverList",Object.keys(roverSockets));
}

const groundStationServer = appGroundStation.listen(80),
 ioGS = socket(groundStationServer),
 groundStations = ioGS.of("/");							/*rappresenta tutti i socket a cui sono collegate le groundstation*/


appGroundStation.use(express.static("./public"));

ioGS.on('connection', (socket) => {		//appena un rover si collega alla groundstation succede questo
	updateRoverList();
	console.log("GroundStation connection id: "+socket.id);
	socket.on("dataToRover", (data, to)=>{
		rovers.to(roverSockets[to]).emit("dataToRover",data);	//dal namespace prendo il nome della connessione e invio il messaggio solo a lei
	})															//usando solo la socket senza namespace non avrei potuto farlo, perché dato l'id della socket (preso dalla mappa)
																//devo riprendere la socket dal namespace.
																//Ma in realtà possiamo evitare tutto questo procedimento, basta mettere nella map direttamente la socket,
																//non l'id, così non devo ripescare la socket dal namespace ma ce l'ho direttamente.
																//lo vediamo nella versione modificata di questo file, sempre nella stessa cartella
	socket.on('disconnect', () => {
		console.log("GroundStation Disconnected id: "+socket.id);
	});
});

const roverServer = appRover.listen(3000),
 ioRover = socket(roverServer),
 rovers = ioRover.of("/");		//creazione di un namespace
//ioRover.of crea un namespace, ossia un pool di connessioni. Di solito l'argomento è il nome del namespace, in questo caso "/" è il default namespace 

ioRover.on('connection', (socket) => {

	let roverName = socket.handshake.query.roverName;	/*alla connessione del rover prende il suo nome dalla query e aggiunge il suo id all'oggetto roverSockets, infine lo comunica alle groundstation*/
	roverSockets[roverName]=socket.id;
	updateRoverList();

	console.log("Rover connection id: "+ socket.id+"	RoverName: "+roverName);
	socket.on('disconnect', () => {
		delete roverSockets[roverName];
		updateRoverList();
		console.log("Rover disconnected id: "+socket.id);
	});
});
