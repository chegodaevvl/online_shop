var personName = document.getElementById("name");
var personPhone = document.getElementById("phone");
var personEmail = document.getElementById("mail");
var orderCity = document.getElementById("city");
var orderAddress = document.getElementById("address");
document.querySelectorAll(".Order-next").forEach(nextBtn => {
  nextBtn.addEventListener("click", function() {
    document.getElementById("order-name").innerHTML = personName.value;
    document.getElementById("order-phone").innerHTML = personPhone.value;
    document.getElementById("order-email").innerHTML = personEmail.value;
    document.getElementById("order-city").innerHTML = orderCity.value;
    document.getElementById("order-address").innerHTML = orderAddress.value;
    document.querySelectorAll(".deliveryType").forEach(radioBtn => {
      if (radioBtn.checked) {
        deliveryName = radioBtn.nextSibling.nextSibling.nextSibling.nextSibling.innerHTML
        document.getElementById("order-delivery").innerHTML = deliveryName;
      }
    })
    document.querySelectorAll(".paymentType").forEach(radioBtn => {
      if (radioBtn.checked) {
        deliveryName = radioBtn.nextSibling.nextSibling.nextSibling.nextSibling.innerHTML
        document.getElementById("order-payment").innerHTML = deliveryName;
      }
    })
  })
})
