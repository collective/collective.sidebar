(function($) {
  'use strict'; // Start of use strict

  $(document).ready(function() {

    // Add Burger Icon

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

  });

})(jQuery); // End of use strict
