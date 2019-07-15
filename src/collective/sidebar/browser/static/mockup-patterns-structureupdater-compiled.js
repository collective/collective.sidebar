(function ($, Base) {
  'use strict';
  var Pattern = Base.extend({
    name: 'sidebar-structureupdater',
    trigger: '.template-folder_contents',
    parser: 'mockup',
    init: function () {
      $('body').on('context-info-loaded', function (e, data) {
        $.ajax({
          type: "post",
          url: data.object.getURL + '/navData',
          data: 'render=' + 1,
          success: function (nav) {
            $('#portal-navigation').html(nav);
          }
        });
      }.bind(this));
    }
  });
  return Pattern;
})
;
define("/home/jesse/Development/repos/collective/collective.sidebar/src/collective/sidebar/browser/static/mockup-patterns-structureupdater.js", function(){});

