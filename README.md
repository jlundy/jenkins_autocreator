# **DEPRECATED**


jenkins_autocreator
===================

A tool to update and create new jobs on your jenkins server.  Moves configuration from jenkins to source control.

NOTE:  Right now this does not handle jenkins authentication.  The servers I tested it on use IP authentication and do not prompt for username, passwords, etc.  If your jenkins requires auth, this will need to be extended.  I plan on eventually adding different auth types to this, but feel free to extend it yourself.  Please contribute back if you do.

Jason

(This tool was built years ago to deal with maintaing pipeline as code well before Jenkins implemented it.  It has not been maintained, and not really needed with the newer versions of Jenkins)
