function capitalize(word) {
  return word.replace(/^\w/, (c) => c.toUpperCase());
}

function displayExpenses() {
  $.ajax({
    type: 'GET',
    url: '/accounts/displayExpenses',
    success: function (response) {
      let platforms = Object.keys(response);
      let dataset = [];
      for (var i = 0, len = platforms.length; i < len; i++) {
        dataset.push(response[platforms[i]]);
        $(`.${platforms[i]}`).text(`$${response[platforms[i]]}`);
        platforms[i] = capitalize(platforms[i]);
      }
      new Chart(document.getElementById('chartjs-dashboard-pie'), {
        type: 'pie',
        data: {
          labels: platforms,
          datasets: [
            {
              data: dataset,
              borderWidth: 5,
            },
          ],
        },
        options: {
          responsive: !window.MSInputMethodContext,
          maintainAspectRatio: false,
          legend: {
            display: true,
          },
          cutoutPercentage: 75,
          plugins: {
            colorschemes: {
              scheme: 'tableau.ClassicMedium10'
            }
          }
        },
      });
    },
  });
}

function displayDeliveries() {
  $.ajax({
    type: "GET",
    url: "/accounts/displayDeliveries",
    success: function (response) {
      var rows = $(".data");
      var columns;
      for (var i = 0; i < rows.length; i++) {
        columns = $(rows[i]).find("td");
        state = response["response"][i]["delivery_status"];
        if (state == "delivered") {
          $(columns[3]).children("span").addClass("badge bg-success");
          $(columns[3]).children("span").html(state);
        } else if (state == "transit" || state == "pickup") {
          $(columns[3]).children("span").addClass("badge bg-warning");
          $(columns[3]).children("span").html(state);
        } else if (state == "pendding") {
          $(columns[3]).children("span").addClass("badge bg-secondary");
          $(columns[3]).children("span").html("pending");
        } else {
          $(columns[3]).children("span").addClass("badge bg-danger");
          $(columns[3]).children("span").html(state);
        }
        t = response["response"][i]["lastest_checkpoint_time"]
          ? response["response"][i]["lastest_checkpoint_time"].split("T")
          : "";
        tt = t == "" ? "" : t[1].split("+");
        $(columns[4]).html(tt == "" ? "---" : t[0] + " " + tt[0]);
      }
    },
  });
}

// Display deliveries
$(document).ready(function () {
  displayExpenses();
  displayDeliveries();
});

function redirect(group_name) {
  location.href = "/accounts/ship/" + group_name;
}

function redirect_locked(group_name) {
  location.href = "/accounts/ship/" + group_name + "/locked";
}
