window.addEventListener('DOMContentLoaded', function() {

  var bannersSwiper = new Swiper(".banners-swiper", {
      loop: true,

      pagination: {
        el: '.banners-pagination',
        clickable: true,
      },

      navigation: {
        nextEl: '.banner-next',
        prevEl: '.banner-prev',
      },

  });

  var hotSwiper = new Swiper(".hot-swiper", {
      loop: true,
      slidesPerView: 3,
      spaceBetween: 20,
      slidesPerGroup: 3,

      pagination: {
        el: '.hot-pagination',
        clickable: true,
      },

      navigation: {
        nextEl: '.hot-next',
        prevEl: '.hot-prev',
      },

  });

  var goodsSwiper = new Swiper(".goods-swiper", {
      slidesPerView: 4,
      spaceBetween: 20,

      pagination: {
        el: '.goods-pagination',
        clickable: true,
      },

      navigation: {
        nextEl: '.goods-next',
        prevEl: '.goods-prev',
      },

  });

  document.querySelectorAll('.header__block-menu-button').forEach(function(element) {
        element.addEventListener('click', function(event) {
            const menu = document.querySelector('.header__nav_menu')
            if (menu.classList.contains('active')){
                document.querySelectorAll('.header__nav_menu').forEach(function(content) {
                content.classList.remove('active')
            })
            }
            else {
                document.querySelector('.header__nav_menu').classList.add('active')
            }
        })
    });

  document.querySelectorAll('.search-form-menu-btn').forEach(function(element) {
        element.addEventListener('click', function(event) {
            const menu = document.querySelector('.search-form_menu')
            if (menu.classList.contains('active-flex')){
                document.querySelectorAll('.search-form_menu').forEach(function(content) {
                content.classList.remove('active-flex')
            })
            }
            else {
                document.querySelector('.search-form_menu').classList.add('active-flex')
            }
        })
    })

  document.querySelector(".header__btn").addEventListener("click", function() {
    document.querySelector(".menu-cats").classList.toggle("menu-active");
  });

  document.addEventListener("click", function(e) {
    let target = e.target;
    if (!target.closest(".header__btn")) {
      document.querySelector(".menu-cats").classList.remove("menu-active");
    }
  });

});

var endTime = 24 * 3600000;
var x = setInterval(function() {
  var currentDate = new Date();
  startTime = ((currentDate.getHours() * 3600) + (currentDate.getMinutes() * 60) + currentDate.getSeconds()) * 1000;
  var distance = endTime - startTime;
  var hours = Math.floor(distance / 3600000);
  var minutes = Math.floor((distance % 3600000) / 60000);
  var seconds = Math.floor((distance % 60000) / 1000);
  document.getElementById("hrs").innerHTML = hours;
  document.getElementById("mins").innerHTML = minutes;
  document.getElementById("secs").innerHTML = seconds;
}, 1000);
