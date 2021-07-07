function displayExpenses() {
  $.ajax({
    type: "GET",
    url: "/accounts/displayExpenses",
    success: function (response) {
      new Chart(document.getElementById("chartjs-dashboard-pie"), {
        type: "pie",
        data: {
          labels: ["Lazada", "Shopee", "Amazon", "Others"],
          datasets: [
            {
              data: [
                response["lazada"],
                response["shopee"],
                response["amazon"],
                response["others"],
              ],
              backgroundColor: [
                window.theme.primary,
                window.theme.warning,
                window.theme.danger,
              ],
              borderWidth: 5,
            },
          ],
        },
        options: {
          responsive: !window.MSInputMethodContext,
          maintainAspectRatio: false,
          legend: {
            display: false,
          },
          cutoutPercentage: 75,
        },
      });

      $(".amazon").text(
        "$" + (response["amazon"] ? response["amazon"] : "0.00")
      );
      $(".lazada").text(
        "$" + (response["lazada"] ? response["lazada"] : "0.00")
      );
      $(".shopee").text(
        "$" + (response["shopee"] ? response["shopee"] : "0.00")
      );
      $(".others").text(
        "$" + (response["others"] ? response["others"] : "0.00")
      );
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
