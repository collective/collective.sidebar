(function ($) {
  'use strict'; // Start of use strict

  function nearTo($element, distance, side, event) {
    var left = $element.offset().left;
    var loffset = left + distance;
    var right = left + $element.width();
    var roffset = right - distance;
    var x = event.pageX;
    if (side == 'left') {
      return x < loffset;
    };
    if (side == 'right') {
      return x > roffset;
    };
  };

  $(document).ready(function () {

    // Burger Icon
    $('#portal-globalnav').prepend('<li id=\"portaltab-burger-menu\"><i class=\"glyphicon glyphicon-menu-hamburger\" /></li>');

    // Mouse
    $('body').mousemove(function (event) {
      var nav = $('#portal-navigation');
      var offset = 10;
      if (nav.hasClass('sidebar-left')) {
        var nearby = nearTo(nav, offset, 'left', event);
        if (nearby) {
          $('body').attr('data-with-sidebar', 'true');
        };
      } else {
        var nearby = nearTo(nav, offset, 'right', event);
        if (nearby) {
          $('body').attr('data-with-sidebar', 'true');
        };
      };
    });

    // Burger

    $('#portaltab-burger-menu').click(function (e) {
      e.preventDefault();
      $('body').attr('data-with-sidebar', 'true');
    });

    // Sidebar Cover

    $('#portal-navigation-cover').click(function (e) {
      e.preventDefault();
      $('body').attr('data-with-sidebar', '');
    });

  });

})(jQuery); // End of use strict
