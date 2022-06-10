window.addEventListener('DOMContentLoaded', function() {

  var bannersSwiper = new Swiper(".banners-swiper", {
      loop: true,

      pagination: {
        el: '.banners-pagination',
      },

      navigation: {
        nextEl: '.banner-next',
        prevEl: '.banner-prev',
      },

  });

  var goodsSwiper = new Swiper(".goods-swiper", {
      slidesPerView: 3,
      spaceBetween: 50,

      pagination: {
        el: '.goods-pagination',
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
    document.querySelector(".menu__cats").classList.toggle("menu-active");
  });

  document.addEventListener("click", function(e) {
    let target = e.target;
    if (!target.closest(".header__btn")) {
      document.querySelector(".menu__cats").classList.remove("menu-active");
    }
  });

});