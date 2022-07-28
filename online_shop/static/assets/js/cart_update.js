document.querySelectorAll(".Amount-input").forEach(inputBlc => {
  inputBlc.addEventListener("input", function() {
    if (inputBlc.value > inputBlc.max) {
      inputBlc.value = inputBlc.max;
    }
    window.location.href = 'update/' + String(inputBlc.dataset.goodsid) + '=' + String(inputBlc.value)
  })
})

document.querySelectorAll(".form-select").forEach(shopSelect => {
  shopSelect.addEventListener("change", function() {
    window.location.href = 'update/' + String(shopSelect.dataset.goodsid) + '/' + String($(this).val())
  })
})

document.querySelectorAll(".Amount-add").forEach(addBtn => {
  addBtn.addEventListener("click", function() {
    inputBlk = this.previousElementSibling;
    if (inputBlk.value < inputBlk.max) {
      window.location.href = 'update/' + String(inputBlk.dataset.goodsid) + '=' + String(Number(inputBlk.value) + 1);
    }
  })
})

document.querySelectorAll(".Amount-remove").forEach(addBtn => {
  addBtn.addEventListener("click", function() {
    inputBlk = this.nextElementSibling;
    if (inputBlk.value > 1) {
      window.location.href = 'update/' + String(inputBlk.dataset.goodsid) + '=' + String(Number(inputBlk.value) - 1);
    }
  })
})