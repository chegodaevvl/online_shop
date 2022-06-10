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
        el: '.goods-pagination',
        clickable: true,
      },

      navigation: {
        nextEl: '.goods-next',
        prevEl: '.goods-prev',
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