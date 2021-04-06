window.onload = fetchData();

function fetchData() {
  fetchFromBackend();
  var interval = setInterval(fetchFromBackend, 1000);
}

function fetchFromBackend() {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        console.log(xhr.responseText);
        data = JSON.parse(xhr.responseText);
        document.getElementById("mask-alert-text").textContent =
          data.mask.maskAlarmStatus;

        if (data.mask.maskAlarm === true) {
          document.getElementById("mask-alert-text").style.color = "#eb3434";
        } else {
          document.getElementById("mask-alert-text").style.color = "#33ff00";
        }

        document.getElementById("occupancy-alert-text").textContent =
          data.occupancy.occupancyAlarmStatus;

        if (data.occupancy.occupancyAlarm === true) {
          document.getElementById("occupancy-alert-text").style.color =
            "#eb3434";
        } else {
          document.getElementById("occupancy-alert-text").style.color =
            "#33ff00";
        }

        document.getElementById("room-id").textContent = data.roomID;

        document.getElementById("room-max-occupancy").textContent =
          data.occupancy.maxOccupancy;

        document.getElementById("room-current-occupancy").textContent =
          data.occupancy.occupancyCount;

        document.getElementById("footer-text").textContent = Date();
      }
    }
  };
  xhr.open("GET", "http://localhost:5000/api/v1/roomInfo");
  xhr.send();
}

function clearAlerts() {
  document.getElementById("mask-alert-text").textContent = "No mask alert";
  document.getElementById("mask-alert-text").style.color = "#33ff00";

  document.getElementById("occupancy-alert-text").textContent =
    "No occupancy alert";
  document.getElementById("occupancy-alert-text").style.color = "#33ff00";
}
