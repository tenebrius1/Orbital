function clearNotifications() {
  $(".notifications").html(
    "<div class='dropdown-menu-header'>You're all caught up :)</div>" +
    "<div class='list-group'>" +
    "<span class='justify-content-center align-content-center d-flex'>" +
    "<img src='https://res.cloudinary.com/dgfzlpuds/image/upload/v1625811708/no-noti-icon_pptq34.jpg' alt='no notification' width=60%>" +
    "</span>" +
    "</div>"
  )
  $.ajax({
    type: "GET",
    url: "/accounts/clearNotifications",
  });
  $('.indicator').remove()
}