(function () {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })
})()

// Delete row on delete button click
$(document).on("click", ".delete", function(){
  $(this).parents("tr").remove();
});

document.addEventListener("DOMContentLoaded", function () {
  // Pie chart
  new Chart(document.getElementById("chartjs-dashboard-pie"), {
    type: "pie",
    data: {
      labels: ["Lazada", "Shopee", "Others"],
      datasets: [{
        data: [4306, 3801, 1689],
        backgroundColor: [
          window.theme.primary,
          window.theme.warning,
          window.theme.danger
        ],
        borderWidth: 5
      }]
    },
    options: {
      responsive: !window.MSInputMethodContext,
      maintainAspectRatio: false,
      legend: {
        display: false
      },
      cutoutPercentage: 75
    }
  });
});