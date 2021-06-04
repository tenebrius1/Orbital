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
        if (state == "delivered")  {
          $(columns[3]).children("span").addClass("badge bg-success");
          $(columns[3]).children("span").html(state);
        } else if (state == "transit" || state == "pickup" || state == "pendding") {
          $(columns[3]).children("span").addClass("badge bg-warning");
          $(columns[3]).children("span").html(state);
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
$(document).ready(displayDeliveries());


// Delete button AJAX Request
$(document).on("click", ".delete", function () {
  $(this).parents("tr").remove();
  $.ajax({
    type: 'POST',
    url: "/accounts/deleteDelivery",
    data: {
      "name": $(this).parent().parent().siblings().closest(".name").text(),
      "tkg_number": $(this).parent().parent().siblings().closest(".tkg_number").text(),
      "courier": $(this).parent().parent().siblings().closest(".courier").text(),
      "status": $(this).parent().parent().siblings().closest(".status").text(),
      "time_updated": $(this).parent().parent().siblings().closest(".time_updated").text(),
      csrfmiddlewaretoken: getCookie('csrftoken'),
    },
    success: function (response) {
      displayDeliveries();
    }
  })
});


$(document).ready(function () {

});
