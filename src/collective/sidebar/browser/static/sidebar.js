(function($) {
  'use strict'; // Start of use strict

  $(document).ready(function() {

    // Burger

    $('#portal-navigation-handle').click(function(e) {
      e.preventDefault();
      $('body').toggleClass('with-sidebar');
    });

  });

})(jQuery); // End of use strict
