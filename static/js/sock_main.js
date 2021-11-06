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
    console.log(data['carcount'])

    // document.getElementById("frames").src = "data:image/png;base64," + json['image'];
    document.getElementById("total").textContent=data['total']
    document.getElementById("carcount").textContent=data['cartotal']
    document.getElementById("buscount").textContent=data['bustotal']
    document.getElementById("truckcount").textContent=data['trucktotal']
    document.getElementById("bikecount").textContent=data['biketotal']
    document.getElementById("rickshawcount").textContent=data['rickshawtotal']
    document.getElementById("vancount").textContent=data['vantotal']
});