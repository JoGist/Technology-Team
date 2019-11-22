'use strict';

var controllerName = 'Imu',
	StructResultClient = require('../../responseClient/controllers/StructResultClientController.js')();
var PythonShell = require('python-shell');



var optionsData = {
  mode: 'text',
  scriptPath: '/home/pi/development/raspstudy/Server/central/',
  args: ['value1', 'value2', 'value3']
};

//AUTO posizionamento verso nord
// var pyshell = new PythonShell('azimut_zero.py',optionsData);


//Va avanti fino ad quando non trova un ostacolo
// var pyshell = new PythonShell('auto_guidance.py',optionsData);


//INVIO solo di dati
var pyshell = new PythonShell('complete_data.py',optionsData);
//
// pyshell.send('OK').end(function(err){
//     if (err) handleError(err);
//     else console.log('erro');
// });


var optionsMotors = {
  mode: 'text',
  pythonOptions: ['-u'],
  scriptPath: '/home/pi/development/raspstudy/Server/central/',
  args: ['value1', 'value2', 'value3']
};
// var options2 = {
//   mode: 'text',
//   pythonOptions: ['-u'],
//   scriptPath: '/home/pi/development/raspstudy/Server/distance_sensor/',
//   args: ['value1', 'value2', 'value3']
// };
//
var pyshell2 = new PythonShell('guidance.py',optionsMotors);



// pyshell.stdout.on('data', function(data) {
//     // if (data == 'data'){
//     //     pyshell.send('go').end(fucntion(err){
//     //         if (err) console.error(err);
//     //         // ...
//     //     });
// 	// } else if (data == 'data2') {
//     //     pyshell.send('OK').end(function(err){
//     //         if (err) console.error(err);
//     //         // ...
//     //     });
// 	// }
//     console.log(data);
//  });

   // pyshell.on('message', function (data) {
   //  // received a message sent from the Python script (a simple "print" statement)
   //  console.log(data);
   // });
 //   var net = require('net');
 //
 //   var client = new net.Socket();
 //   client.connect(10000, '127.0.0.1', function() {
 //   	console.log('Connected');
 //   	client.write('Hello, server! Love, Client.');
 //   });
 //
 //   client.on('data', function(data) {
 //   	console.log('Received: ' + data);
 // //   	client.destroy(); // kill client after server's response
 //   });
 //
 //   client.on('close', function() {
 //   	console.log('Connection closed');
 //   });
 //
 //
 //



var flag = true;
var ImuController = function init(modules) {
  var router = modules.router;
  console.log('IMU CONTROLLER');
  var request_data = true;
  modules.io.on('connection', function (socket) {
	//
	// setInterval(function(str1, str2) {
	// 	PythonShell.run('imuData.py',options, function (err, results) {
    // 		// console.log(err, results);
    // 		if (!err && results && results.length === 1) {
    // 			var values = results[0];
    // 			var obj = JSON.parse(values);
	//
 //  			socket.emit('news', obj);
	//
    // 		} else {
    // 			console.log('problem');
    // 		}
    // 	});
 //  	}, 1200);
//  var time = 0,
//  	timeprec = 0,
// 	intervalTime = 0;
// var vx0 = 0,
//  	vy0 = 0,
// 	vx = 0,
// 	vy = 0;
console.log('ciao_init');
	if (request_data) {
		// setTimeout(function() {
			pyshell.on('message', function (data) {
		 	   // received a message sent from the Python script (a simple "print" statement)

				var obj = JSON.parse(data);
				//    console.log(obj);
				   //console.log(obj.accel);
				//    time = process.hrtime()
				//    intervalTime = (time[0]- timeprec[0]);
				//    if (intervalTime === 1) {
				// 	   //console.log(obj.accel);

				// var val = 0.1;
				// var ax = obj.accel[0];
				// var ay = obj.accel[1];
				// if (ax > val || ay > val) {
				// 	console.log('ax:',ax);
				// 	console.log('ay:',ay);
				// 	// vx = vx0 + obj.accel[0]*9.81*0.008;
				// 	// vx0 = vx;
				// 	// vy = vy0 + obj.accel[1]*9.81*0.008;
				// 	// vy0 = vy;
				// 	// console.log(vx,vy);
				// }
				//

				//    }
				//    //console.log(time);
				//    //console.log(intervalTime);
				//    timeprec = time;
				//console.log(obj);
				socket.emit('news', obj);
		    });
			pyshell.end(function (err) {
			  if (err) throw err;
			  console.log('finished');
			});
			// pyshell.send('hello world!');
			// pyshell.end(function(){
			// 	console.log('ciao');
			// });
		// }, 1000);




		// console.log('ciao');
		// pyshell.send(JSON.stringify([1,2,3,4,5]));
		//
		// pyshell.on('message', function (message) {
		//     // received a message sent from the Python script (a simple "print" statement)
		//     // console.log(message);
		//
		// });
		//
		// // end the input stream and allow the process to exit
		// pyshell.end(function (err) {
		//     if (err){
		//         throw err;
		//     };
		//
		//     console.log('finished');
		// });

	};

	socket.on('info_imu', function (data) {
		console.log(data);
		optionsMotors.args = [data.send]
		PythonShell.run('guidance.py', optionsMotors, function (err, results) {
		  if (err) throw err;
		  // results is an array consisting of messages collected during execution
		  console.log('results: %j', results);
		});
	});
  });

  router.route('/' + controllerName)
    .get(function(req, res) {
		console.log('GET');
    	var sRC = new StructResultClient();
        var query = req.query;
		//console.log(options);
		PythonShell.run('imuData.py',options, function (err, results) {
			// console.log(err, results);
			if (!err && results && results.length === 1) {
				var values = results[0];
				var obj = JSON.parse(values);
				// console.log(obj);
				sRC.jsonStruct.result = obj;
				sRC.jsonSendToClient(res);

			} else {
				res.sendStatus(500);
			}
		});

    })
}


module.exports = ImuController;
