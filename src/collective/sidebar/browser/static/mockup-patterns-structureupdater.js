if (require === undefined) {
  require = function (reqs, torun) {
    'use strict';
    return torun(window.jQuery);
  }
}

require([
  'jquery',
  'pat-base',
], function ($, Base) {
  'use strict';

  var SidebarUpdater = Base.extend({
    name: 'sidebar-structureupdater',
    trigger: '.template-folder_contents',
    parser: 'mockup',
    init: function () {
      $('body').on('context-info-loaded', function (e, data) {
        var base_url = $('body').data('base-url');
        var path = base_url + '/navData';
        if (data.object) {
          path = data.object.getURL + '/navData';
        }
        $.ajax({
          type: "post",
          url: path,
          data: 'render=' + 1,
          success: function (nav) {
            $('#portal-navigation').html(nav);
          }
        });
      }.bind(this));
    }
  });

  return SidebarUpdater;

});
