(function($) {
  'use strict'; // Start of use strict

  $(document).ready(function() {

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
