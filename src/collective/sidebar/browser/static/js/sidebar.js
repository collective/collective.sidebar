(function ($) {
  'use strict'; // Start of use strict

  // Cookie Methods

  function createCookie(name, value, days) {
    if (days) {
      var date = new Date();
      date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
      var expires = '; expires=' + date.toGMTString();
    } else var expires = '';
    document.cookie = name + '=' + value + expires + '; path=/';
  }

  function readCookie(name) {
    var nameEQ = name + '=';
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') c = c.substring(1, c.length);
      if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
  }

  function deleteCookie(name) {
    createCookie(name, '', -1);
  }

  $(window).bind('load', function() {

    var state_name = 'collapsed';

    $('.menu-section-title').on('click', function() {

      var parent = $(this).parent();
      var parent_id = parent.attr('id');
      var cookie = readCookie('sections');

      if (cookie) {
        var sections = cookie.split(',');
      } else {
        var sections = [];
      }

      parent.toggleClass(state_name);

      if (parent.hasClass(state_name)) {
        sections.push(parent_id);
      } else {
        var sections = sections.filter(function(e) {
          return e !== parent_id
        });
      }

      createCookie('sections', sections.join(','));

    });

  });

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

    if($('.navigation-dynamic').length){

      $(document).on('click', '.link-folder', function(e){
        e.preventDefault();
        var target = $(this).attr('href')+'/@@navigation .menu-section-content';
        $('#navigation-wrapper').load(target);
      });  
    
    }
  
  });

})(jQuery); // End of use strict
