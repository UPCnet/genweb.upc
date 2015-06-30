Introduction
============

UPC feature package for Genweb.

Resource build
--------------

The Genweb UPC package has its own set of SCSS resources that builds into an
unique set of CSS stylesheets. This stylesheets can be accessed through the URL:
`++genwebupc++stylesheets/genwebupc.css` ... and so on.

In order to build the CSS you should install the grunt-based builder::

    $ cd <the_root_directory_of_genweb.upc>
    $ npm -g install grunt-cli
    $ npm install

And then, run the watcher::

    $ grunt watch

Any change on the SCSS resources with trigger the build of the CSS.


How default genweb.theme override works
---------------------------------------

The default resources of genweb.theme are still in place, but they are intended
to be overriden if needed, in case of the genweb.upc flavours. The plans are to
make those "base styles" more thinner and only contain those that are really
needed as "frame" and "base" to other more complex themes.

The default CSS lives in the URLs `++genweb++stylesheets/genwebupc.css` and so
on.

The `main_template.pt` is overriden via z3c.jbot in the `templates` folder to
enable the load of the `++genwebupc++stylesheets` resources.
