(function($) {
  'use strict'; // Start of use strict

  $(document).ready(function() {

    // Add burger icon to navigation
    $('#portal-globalnav').prepend('<li id=\"portaltab-burger-menu\"><i class=\"glyphicon glyphicon-menu-hamburger\" /></li>');

    // Mouse
    $('body').on('mousemove', function(event) {
      if (event.pageX < 20) {
        $('body').attr('data-with-sidebar', 'true');
      }
    });

    // Burger

    $('#portaltab-burger-menu').click(function(e) {
      e.preventDefault();
      $('body').attr('data-with-sidebar', 'true');
    });

    // Sidebar Cover

    $('#portal-navigation-cover').click(function(e) {
      e.preventDefault();
      $('body').attr('data-with-sidebar', '');
    });

    // Sidebar Collapse

    $('#portal-navigation #menu-collapse').click(function(e) {
      $('.menu .menu-section').fadeOut(150, function() {
        $('#portal-navigation').toggleClass('collapsed').one('transitionend', function() {
          $('.menu .menu-section').fadeIn(150);
        });
      });
    });

  });

})(jQuery); // End of use strict
