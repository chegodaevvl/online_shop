document.querySelectorAll(".Sort-sortBy").forEach(item => {
  item.addEventListener("click", function() {
    let btn = this;
    document.querySelectorAll(".Sort-sortBy").forEach(el => {
      if (el != btn) {
        el.classList.remove("Sort-sortBy_dec", "Sort-sortBy_inc");
      }
      if (btn.classList.contains("Sort-sortBy_dec")) {
        btn.classList.remove("Sort-sortBy_dec")
        btn.classList.add("Sort-sortBy_inc")
        btn.href = btn.dataset.order + '&direction=up'
      } else if (btn.classList.contains("Sort-sortBy_inc")) {
        btn.classList.remove("Sort-sortBy_inc")
        btn.classList.add("Sort-sortBy_dec")
        btn.href = btn.dataset.order + '&direction=down'
      } else{
        btn.classList.add("Sort-sortBy_dec")
        btn.href = btn.dataset.order + '&direction=down'
      }
    });
  })
})
