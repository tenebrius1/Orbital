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

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

$(document).on("click", ".delete", function () {
  $.ajax({
    type: 'POST',
    url: "/accounts/deleteTransaction",
    data: {
      "name": $(this).parent().parent().siblings().closest(".name").text(),
      "price": $(this).parent().parent().siblings().closest(".price").text(),
      "date": $(this).parent().parent().siblings().closest(".date").text(),
      "company": $(this).parent().parent().siblings().closest(".company").text(),
      csrfmiddlewaretoken: getCookie('csrftoken'),
    },
  })
});

$(document).on("click", ".btnSave", function () {
  $.ajax({
    type: 'POST',
    url: "/accounts/editTransaction",
    data: {
      "name": $(this).parent().parent().siblings().closest(".name").text(),
      "price": $(this).parent().parent().siblings().closest(".price").text(),
      "date": $(this).parent().parent().siblings().closest(".date").text(),
      "company": $(this).parent().parent().siblings().closest(".company").text(),
      csrfmiddlewaretoken: getCookie('csrftoken'),
    },
  })
});

// Delete row on delete button click
$(document).on("click", ".delete", function () {
  $(this).parents("tr").remove();
});

$(document).ready(function () {
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
            display: false
          },
          cutoutPercentage: 75
        }
      });

      $(".amazon").text("$" + (response["amazon"] ? response["amazon"] : "0.00"));
      $(".lazada").text("$" + (response["lazada"] ? response["lazada"] : "0.00"));
      $(".shopee").text("$" + (response["shopee"] ? response["shopee"] : "0.00"));
      $(".others").text("$" + (response["others"] ? response["others"] : "0.00"));
    },
  })
});