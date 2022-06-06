window.addEventListener('DOMContentLoaded', function() {

    var swiper = new Swiper(".goodsSwiper", {
        direction: 'horizontal',
        slidesPerView: 3,
        spaceBetween: 50,

        pagination: {
          el: '.swiper-pagination',
        },

        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev',
        },

    });

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
