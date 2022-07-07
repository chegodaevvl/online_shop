var amountFld = document.querySelector(".Amount-input");
console.log(amountFld.value);
var cart_link = document.querySelector(".cart_link");
cart_link.addEventListener("click", function() {
  cart_link.href = cart_link.href + amountFld.value
})


//
//
//
//
//input.oninput = function() {
//  console.log(input.value)
//}


//
//document.querySelector(".Amount-input").forEach(item => {
//  item.addEventListener("onchange", function() {
//    let btn = this;
//      if (btn.classList.contains("Sort-sortBy_dec")) {
//        btn.classList.remove("Sort-sortBy_dec")
//        btn.classList.add("Sort-sortBy_inc")
//        btn.href = btn.dataset.order + '&direction=up'
//      } else if (btn.classList.contains("Sort-sortBy_inc")) {
//        btn.classList.remove("Sort-sortBy_inc")
//        btn.classList.add("Sort-sortBy_dec")
//        btn.href = btn.dataset.order + '&direction=down'
//      } else{
//        btn.classList.add("Sort-sortBy_dec")
//        btn.href = btn.dataset.order + '&direction=down'
//      }
//  })
//})
