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
document.getElementById('card1').style.backgroundImage ="data:image/png;base64," + data ;

});
sio.on("page data detection", (data) =>{
    console.log(data)

    // document.getElementById("frames").src = "data:image/png;base64," + json['image'];
    // document.getElementById("total").textContent=json['total']
    // document.getElementById("carcount").textContent=json['cartotal']
    // document.getElementById("buscount").textContent=json['bustotal']
    // document.getElementById("truckcount").textContent=json['trucktotal']
    // document.getElementById("bikecount").textContent=json['biketotal']
    // document.getElementById("rickshawcount").textContent=json['rickshawtotal']
    // document.getElementById("vancount").textContent=json['vantotal']
});