(function($) {
  'use strict'; // Start of use strict

  $(document).ready(function() {

    // Mouse
    $('body').on('mousemove',function(event) {
      if (event.pageX < 20) {
        $('body').attr('data-with-sidebar', 'true');
      }
    });

    // Burger

    $('#portal-navigation-handle').click(function(e) {
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
