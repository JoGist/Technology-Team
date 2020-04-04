const io = require("socket.io-client"),
	  readLine = require("readline");

const rl = readLine.createInterface({
			input : process.stdin,
			output: process.stdout
		});

rl.question("Nome Rover: ", (roverName) => {		/*nel rover vero chiaramente questo non sarà lasciato come input all'utente ma verrà fissato univoco per ogni rover*/
	const socket = io("http://localhost:3000/?roverName="+roverName); 	/*il "rover" si collega al server tramite l'indirizzo e comunica con la query il suo nome */
	socket.on("dataToRover", (data)=>{
		rl.write(data.toString()+"\n");
	});
});
