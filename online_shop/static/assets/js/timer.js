var endTime = 24 * 3600000;
var x = setInterval(function() {
  var currentDate = new Date();
  startTime = ((currentDate.getHours() * 3600) + (currentDate.getMinutes() * 60) + currentDate.getSeconds()) * 1000;
  var distance = endTime - startTime;
  var hours = Math.floor(distance / 3600000);
  var minutes = Math.floor((distance % 3600000) / 60000);
  var seconds = Math.floor((distance % 60000) / 1000);
  document.getElementById("hrs").innerHTML = hours;
  document.getElementById("mins").innerHTML = minutes;
  document.getElementById("secs").innerHTML = seconds;
}, 1000);
