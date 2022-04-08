window.addEventListener('DOMContentLoaded', function() {
  document.querySelector('.open-profile-btn').addEventListener('click', function() {

    // document.querySelector('.burger__menu').attr('tabindex', '0')

    // setTimeout(function() {
    //   document.querySelector('.burger__menu').classList.toggle('burger-menu_is-active');
    //   }, 200);

    // document.querySelector('.burger__menu').classList.toggle('menu_display-bl')

    // document.querySelector('.burger__menu').classList.add('menu_display-bl')
    document.querySelector('.burger__menu').classList.add('burger-menu_is-active')

    // document.querySelector('.burger__btn').classList.toggle('active-burger-btn')

    // document.querySelector('.burger__menu').classList.toggle('burger-menu_is-active')




  })

  document.querySelector('.close-profile-btn').addEventListener('click', function() {

    // document.querySelector('.burger__menu').classList.remove('menu_display-bl')
    document.querySelector('.burger__menu').classList.remove('burger-menu_is-active')




  })
})