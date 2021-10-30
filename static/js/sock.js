// var speedCanvas = document.getElementById("speedChart");

// // Chart.defaults.global.defaultFontFamily = "Lato";
// // Chart.defaults.global.defaultFontSize = 18;

// var dataFirst = {
//     label: "Car A - Speed (mph)",
//     data: [0, 59, 75, 20, 20, 55, 40],
//     lineTension: 0,
//     fill: false,
//     borderColor: 'red'
//   };

// var dataSecond = {
//     label: "Car B - Speed (mph)",
//     data: [20, 15, 60, 60, 65, 30, 70],
//     lineTension: 0,
//     fill: false,
//   borderColor: 'blue'
//   };
// var speedData = {
//   labels: ["0s", "10s", "20s", "30s", "40s", "50s", "60s"],
//   datasets: [dataFirst, dataSecond]
// };

// var chartOptions = {
//   legend: {
//     display: true,
//     position: 'top',
//     labels: {
//       boxWidth: 80,
//       fontColor: 'black'
//     }
//   }
// };

// var lineChart = new Chart(speedCanvas, {
//   type: 'line',
//   data: speedData,
//   options: chartOptions
// });


const multiline = document.getElementById('multipleLineChart').getContext('2d');

const chart = new Chart(multiline, {
  type: 'line',
  data: {
    labels: [
      moment(new Date(2020, 2, 1)).format('YYYY-MM-DD'),
      moment(new Date(2020, 2, 2)).format('YYYY-MM-DD'),
      moment(new Date(2020, 2, 3)).format('YYYY-MM-DD')
    ],
    datasets: [{
        label: '# of Red Votes',
        data: [12, 18, 22],
        borderWidth: 1,
        fill: false,
        borderColor: 'red'
      },
      {
        label: '# of Green Votes',
        data: [12, 2, 13],
        borderWidth: 1,
        fill: false,
        borderColor: 'green'
      }
    ]
  },
  options: {
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: true
        }
      }]
    }
  }
});








const sio = io('http://' + document.domain + ':' + location.port);

sio.on('connect', () => {
  console.log('connected clint js');
  //   sio.emit('sum', {numbers: [1, 2]});
});

sio.on('disconnect', () => {
  console.log('disconnected');
});

sio.on("frame", (data) => {
  console.log("frame recieved")
  document.getElementById("frames").src = "data:image/png;base64," + data;

});