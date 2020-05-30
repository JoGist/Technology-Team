export function connetti(ip, porta){
  let address = "http://" + ip + ":" + porta;
  return io(address); 
}

export function sendData(data, toRover, socket){

  let messaggio = {
    data: data,
    toRover: toRover
  };

  socket.emit("dataToRover", JSON.stringify(messaggio));
}

export function disconnetti(socket){
  return socket.disconnect();
}
