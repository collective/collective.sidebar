(function($) {
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

})(jQuery); // End of use strict
