
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


appGroundStation.use(express.static("./public"));		//restituisce il contenuto della cartella public a quelli che si connettono

ioGS.on('connection', (socket) => {		//appena un rover si collega alla groundstation succede questo
	updateRoverList();
	console.log("GroundStation connection id: "+socket.id);
	socket.on("dataToRover", (messaggio)=>{
		let msg = JSON.parse(messaggio);	//trasformiamo il JSON in oggetto javscript
		roverSockets[msg.toRover].emit("dataToRover",msg.data);		//non ho più bisogno di prendere la socket dal namespace, ce l'ho direttamente nella mappa
	})															
	socket.on('disconnect', () => {
		console.log("GroundStation Disconnected id: "+socket.id);
	});
});

const roverServer = appRover.listen(3000),
 ioRover = socket(roverServer);
 //rovers = ioRover.of("/");		il namespace non serve più

ioRover.on('connection', (socket) => {

	let roverName = socket.handshake.query.roverName;	/*alla connessione del rover prende il suo nome dalla query e aggiunge il suo id all'oggetto roverSockets, infine lo comunica alle groundstation*/
	roverSockets[roverName]=socket;		//qui c'è la modifica cruciale. Invece di mettere nella mappa socket.id metto direttamente la socket, così quando voglio
										//inviare i messaggi ai rover non devo ripescare la socket dal suo id ma ce l'ho direttamente
	updateRoverList();

	console.log("Rover connection id: "+ socket.id+"	RoverName: "+roverName);
	socket.on('disconnect', () => {
		delete roverSockets[roverName];
		updateRoverList();
		console.log("Rover disconnected id: "+socket.id);
	});
});
