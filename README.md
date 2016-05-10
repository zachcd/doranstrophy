# doranstrophy
http://www.lol-at-pitt.com/dorans/

This is all written in python with django and cassiopeia, included here is the app as an independent and implementable part of any django project.

The only setting necessary is that Session Serialization must be set to pickling instead of json due to the sessions variable storing most champion data.

Overall, everything works, and its all live on the site, one thing to be worked on and improved is the number of times the request calls can stack on top of each other, luckily cassiopeia prevents them from going all the way to the riot api, but internally it can cause a hypothetical slowdown.

A couple other features we were thinking about implementing never got worked on because College Finals took over. RIP.  More documentation might follow tomorrow.
