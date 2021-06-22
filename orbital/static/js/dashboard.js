document.addEventListener("DOMContentLoaded", function () {
  var ctx = document.getElementById("chartjs-dashboard-line").getContext("2d");
  var gradient = ctx.createLinearGradient(0, 0, 0, 225);
  gradient.addColorStop(0, "rgba(215, 227, 244, 1)");
  gradient.addColorStop(1, "rgba(215, 227, 244, 0)");
  // Line chart
  new Chart(document.getElementById("chartjs-dashboard-line"), {
    type: "line",
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
      datasets: [{
        label: "Sales ($)",
        fill: true,
        backgroundColor: gradient,
        borderColor: window.theme.primary,
        data: [
          2115,
          1562,
          1584,
          1892,
          1587,
          1923,
          2566,
          2448,
          2805,
          3438,
          2917,
          3327
        ]
      }]
    },
    options: {
      maintainAspectRatio: false,
      legend: {
        display: false
      },
      tooltips: {
        intersect: false
      },
      hover: {
        intersect: true
      },
      plugins: {
        title: {
          display: true,
          text: 'Razer Deathadder'
        },
        filler: {
          propagate: false
        }
      },
      scales: {
        xAxes: [{
          reverse: true,
          gridLines: {
            color: "rgba(0,0,0,0.0)"
          }
        }],
        yAxes: [{
          ticks: {
            stepSize: 1000
          },
          display: true,
          borderDash: [3, 3],
          gridLines: {
            color: "rgba(0,0,0,0.0)"
          }
        }]
      }
    }
  });
  new Chart(document.getElementById("chartjs-dashboard-line1"), {
    type: "line",
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
      datasets: [{
        label: "Sales ($)",
        fill: true,
        backgroundColor: gradient,
        borderColor: window.theme.primary,
        data: [
          2115,
          1562,
          1584,
          1892,
          1587,
          1923,
          2566,
          2448,
          2805,
          3438,
          2917,
          3327
        ]
      }]
    },
    options: {
      maintainAspectRatio: false,
      legend: {
        display: false
      },
      tooltips: {
        intersect: false
      },
      hover: {
        intersect: true
      },
      plugins: {
        filler: {
          propagate: false
        }
      },
      scales: {
        xAxes: [{
          reverse: true,
          gridLines: {
            color: "rgba(0,0,0,0.0)"
          }
        }],
        yAxes: [{
          ticks: {
            stepSize: 1000
          },
          display: true,
          borderDash: [3, 3],
          gridLines: {
            color: "rgba(0,0,0,0.0)"
          }
        }]
      }
    }
  });
  new Chart(document.getElementById("chartjs-dashboard-line2"), {
    type: "line",
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
      datasets: [{
        label: "Sales ($)",
        fill: true,
        backgroundColor: gradient,
        borderColor: window.theme.primary,
        data: [
          2115,
          1562,
          1584,
          1892,
          1587,
          1923,
          2566,
          2448,
          2805,
          3438,
          2917,
          3327
        ]
      }]
    },
    options: {
      maintainAspectRatio: false,
      legend: {
        display: false
      },
      tooltips: {
        intersect: false
      },
      hover: {
        intersect: true
      },
      plugins: {
        filler: {
          propagate: false
        }
      },
      scales: {
        xAxes: [{
          reverse: true,
          gridLines: {
            color: "rgba(0,0,0,0.0)"
          }
        }],
        yAxes: [{
          ticks: {
            stepSize: 1000
          },
          display: true,
          borderDash: [3, 3],
          gridLines: {
            color: "rgba(0,0,0,0.0)"
          }
        }]
      }
    }
  });
});

function displayExpenses() {
  $.ajax({
    type: 'GET',
    url: "/accounts/displayExpenses",
    success: function (response) {
      new Chart(document.getElementById("chartjs-dashboard-pie"), {
        type: "pie",
        data: {
          labels: ["Lazada", "Shopee", "Amazon", "Others"],
          datasets: [{
            data: [response["lazada"], response["shopee"], response["amazon"], response["others"]],
            backgroundColor: [
              window.theme.primary,
              window.theme.warning,
              window.theme.danger,
            ],
            borderWidth: 5
          }]
        },
        options: {
          responsive: !window.MSInputMethodContext,
          maintainAspectRatio: false,
          legend: {
            display: false,
          },
          cutoutPercentage: 75,
        }
      });

      $(".amazon").text("$" + (response["amazon"] ? response["amazon"] : "0.00"));
      $(".lazada").text("$" + (response["lazada"] ? response["lazada"] : "0.00"));
      $(".shopee").text("$" + (response["shopee"] ? response["shopee"] : "0.00"));
      $(".others").text("$" + (response["others"] ? response["others"] : "0.00"));
    },
  })
}

function displayDeliveries() {
  $.ajax({
    type: 'GET',
    url: "/accounts/displayDeliveries",
    success: function (response) {
      var rows = $('.data');
      var columns;
      for (var i = 0; i < rows.length; i++) {
        columns = $(rows[i]).find('td');
        state = response['response'][i]['delivery_status'];
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
        t = response['response'][i]['lastest_checkpoint_time'] ? response['response'][i]['lastest_checkpoint_time'].split("T") : "";
        tt = t == "" ? "" : t[1].split("+");
        $(columns[4]).html(tt == "" ? "---" : t[0] + " " + tt[0]);
      }
    },
  })
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