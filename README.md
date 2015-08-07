# cdp.py
Python module/cli/cgi script for cdp backup creation

####CLI Usage:

    $ ./cdp.py [hostname] [ip] [os (LINUX/WINDOWS)] [scheduled hour] [frequency hours]

####HTTP Usage:

    $ curl http://hostname.tld/cdp/cdp-cgi.py?cdpserver=cdp09.solido.net&hostname=testtest01&ip=1.2.3.4&os=LINUX&schehours=2&freqhours=1

####Module information (`$ python3 >>> import cdp(); help(cdp);`):

    NAME
        cdp

    CLASSES
        builtins.object
            cdp

        class cdp(builtins.object)
         |  Methods defined here:
         |
         |  __init__(self, soap_host, soap_port, soap_user, soap_pass)
         |
         |  create_agent(self, hostname, ip, port, os)
         |
         |  create_disksafe(self, hostname)
         |
         |  create_policy(self, hostname, replsche_hours_of_day, dailyfreq_hours_of_day)
         |
         |  help(self)
         |
         |  run(self, hostname, ip, port, os, sche_hours, freq_hours)
         |
         |  set_timezone(self, area)
         |
         |  ----------------------------------------------------------------------
         |  Data descriptors defined here:
         |
         |  __dict__
         |      dictionary for instance variables (if defined)
         |
         |  __weakref__
         |      list of weak references to the object (if defined)

    FILE
        /var/www/html/cdp/cdp.py
