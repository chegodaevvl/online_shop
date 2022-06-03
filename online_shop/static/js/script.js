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