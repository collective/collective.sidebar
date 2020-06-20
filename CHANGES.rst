Changelog
=========


1.3.0 (2020-06-20)
------------------

Added:

- Added dynamic navigation inside sidebar #27
  [santonelli]

- Add option for Bootstrap icons. #74
  [santonelli]

Changed:

- Changed to use npm scripts to compile SCSS and JS.
  [santonelli]

- Reduced font size and margings.
  [santonelli]

- Changed to activate all features (collapsible secitons) by default.
  [santonelli]

- Code cleanup to respekt flake8.
  [santonelli]

- Improved icon handling.
  [santonelli]

Bugfixes:

- Hide upgrade steps from installer.
  [santonelli]
  

1.2.0 (2019-12-04)
------------------

Added:

- Added checks to respect global navigation settings #71
  [santonelli]


1.1.0b2 (2019-08-30)
--------------------

Added:

- Added option to trigger the sidebar from left and right side of screen. #30
  [netroxen]


1.0.0b1 (2019-08-14)
--------------------

Changed:

- Crop utility functionality improved. #65
  [sarnold]

- Font pack now selectable in the sidebar settings. #69
  [sarnold]

- Plone toolbar removed from rendered DOM.
  [netroxen]


1.0.0a10 (2019-08-01)
---------------------

Added:

- Added back button to empty folders. #58
  [sarnold]


1.0.0a9 (2019-05-24)
--------------------

Added:

- Added collapsible sections to the sidebar template. #3
  [netroxen]

- Added conditional to static-links section. #54
  [goschtl]

Changed:

- Removed main_template override from package. #52
  [netroxen]


1.0.0a8 (2019-05-09)
--------------------

Added:

- Added a link to select_default_view. #33
  [sarnold]

- Added object_buttons actions like cut,copy,paste. #46
  [sarnold]


1.0.0a7 (2019-02-05)
--------------------

Changed:

- Back button not visible when root level navigation enabled.
  [netroxen, sarnold]


1.0.0a6 (2019-02-04)
--------------------

Bugfixes

- Add default to get registry record in the get_items method.
  [netroxen]


1.0.0a5 (2019-02-04)
--------------------

Added:

- Added a controlpanel for sidebar configuration. #41
  [netroxen]

- Added setting to pin the root level navigation to the sidebar. #41
  [netroxen]

Changed:

- Removed the "root" parameter from the get_items method of the sidebar. #41
  [netroxen]


1.0.0a4 (2019-02-01)
--------------------

Changed:

- Moved the profile URL from the template to Python class.
  [jstippel]


1.0.0a3 (2019-01-31)
--------------------

Added:

- Added a profile section to the top of the sidebar panel. #5
  [netroxen]

- Sidebar links are now configurable through the portal_actions menu. #22
  [netroxen]


1.0.0a2 (2018-12-04)
--------------------

Added:

- Added structureupdater functionality to the sidebar. #11
  [netroxen, sarnold]


1.0.0a1 (2018-11-10)
--------------------

Added:

- Add workflow section to sidebar. #7
  [santonelli]

- Initial release.
  [santonelli]

Changed:

- Refactor add section. #24
  [santonelli]

- Improved sidebar styling and introduced a site-cover. #1
  [jstippel]
