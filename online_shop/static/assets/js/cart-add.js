var amountFld = document.querySelector(".Amount-input");
console.log(amountFld.value);
var cart_link = document.querySelector(".cart_link");
cart_link.addEventListener("click", function() {
  cart_link.href = cart_link.href + amountFld.value
})
