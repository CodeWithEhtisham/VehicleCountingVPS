const sio = io('http://' + document.domain + ':' + location.port);

sio.on('connect', () => {
  console.log('connected clint main html');
  //   sio.emit('sum', {numbers: [1, 2]});
});

sio.on('disconnect', () => {
  console.log('disconnected');
});

sio.on("frame", (data) => {
  console.log("frame received")
//   document.getElementById("frames").src = "data:image/png;base64," + data;
document.getElementById('card1').style.backgroundImage ="data:image/png;base64," + data['image'] ;

});