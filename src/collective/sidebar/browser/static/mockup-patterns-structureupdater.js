if (require === undefined) {
  require = function(reqs, torun) {
    'use strict';
    return torun(window.jQuery);
  }
}

require([
  'jquery',
  'pat-base',
  'mockup-patterns-moment',
  'mockup-patterns-structure-url/pattern-structureupdater',
], function($, Base, patMoment) {
  'use strict';
  var Pattern = Base.extend({
    name: 'sidebar-structureupdater',
    trigger: '.template-folder_contents',
    parser: 'mockup',
    init: function() {
      $('body').on('context-info-loaded', function(e, data) {

        var request = $.ajax({
          type: "post",
          url: data.object.getURL + '/navData',
          data: 'render=' + 1,
          success: function(data) {
            return data;
          }
        });

        request.done(function(data) {
          var elid = '#sidebar-modified';
          var mod_date = $(data).find(elid);
          self.moment = new patMoment(mod_date, {format: 'relative'});
          $('#portal-navigation').html(data);
          $(elid).replaceWith(self.moment.$el[0]);
        });

      }.bind(this));
    }
  });
  return Pattern;
});
