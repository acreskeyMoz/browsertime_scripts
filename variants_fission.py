# Define the apps to test
#  The last parameter can be a firefox pref string (e.g '--firefox.preference network.http.rcwn.enabled:false ')
variants = [ ('e10s', 'desktop.sh', ' ' ),
             ('fission', 'desktop.sh', '--firefox.preference fission.autostart:true ' )]
