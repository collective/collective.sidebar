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

    // Collapse

    $('.userrole-authenticated .menu .menu-section-title').click(function() {
      var parent = $(this).parent();
      parent.toggleClass('collapsed');
      if (parent.attr('data-state') == 'show') {
        parent.attr('data-state', 'hide');
      } else {
        parent.attr('data-state', 'show');
      }
    });

  });

})(jQuery); // End of use strict
