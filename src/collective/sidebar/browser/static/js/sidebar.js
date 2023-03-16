(function ($) {
  'use strict'; // Start of use strict

  $(document).ready(function () {

    // Burger elements to open Sidebar

    var burger = '#burger-menu, #navigation-menu, #sidebar-menu, #sidebar-handle'
    var sidebar_element = document.getElementById('portal-sidebar');

    if (!sidebar_element) {
        return;
    }
    var sidebar = new bootstrap.Offcanvas(sidebar_element);

    var showSidebarEvent = function (event) {
      event.stopPropagation();
      sidebar.show();      
    }

    document.querySelectorAll(burger).forEach((element) => {
      element.addEventListener('click', showSidebarEvent);
    });

    // Save collapsed state in localstorage

    $(".collapse").on("shown.bs.collapse", function () {
      localStorage.setItem("coll_" + this.id, true);
    });
  
    $(".collapse").on("hidden.bs.collapse", function () {
      localStorage.removeItem("coll_" + this.id);
    });
  
    $(".collapse").each(function () {
      if (localStorage.getItem("coll_" + this.id) === "true") {
        $(this).collapse("show");
      } else {
        $(this).collapse("hide");
      }
    });

    // Mouse

    var mouse_activated = $('#portal-sidebar').data('sidebar-mouse');
    var offset = $('#portal-sidebar').data('sidebar-mouse-area');

    if (mouse_activated) {
      $('body').mousemove(function (event) {
        if (sidebar_element.classList.contains('offcanvas-start')) {
          if ( event.pageX <= offset ) {
            sidebar.show();
          }        
        } else {
          if ( event.pageX >= window.innerWidth - offset ) {
            sidebar.show();
          }
        }
        
      });
    }

    if($('.navigation-dynamic').length){

      $(document).on('click', '.link-folder', function(e){
        e.preventDefault();
        var target = $(this).attr('href')+'/@@navigation .nav';
        $('#navigation-wrapper').hide();
        $('#navigation-wrapper').load(target);
        $('#navigation-wrapper').fadeIn('500');
      });  
    
    }
  
  });

})(jQuery); // End of use strict
