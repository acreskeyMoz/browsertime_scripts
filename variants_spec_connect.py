# Define the apps to test
#  The last parameter can be a firefox pref string (e.g '--firefox.preference dom.prefetch_dns_for_anchor:false ')
variants = [('baseline', 'desktop.sh', ' ' ),
            ('spec_connect_0_sockets', 'desktop.sh', '--firefox.preference network.http.speculative-parallel-limit:0 '),
            ('spec_connect_20_sockets', 'desktop.sh', '--firefox.preference network.http.speculative-parallel-limit:20 '),
            ('spec_connect_30_sockets', 'desktop.sh', '--firefox.preference network.http.speculative-parallel-limit:30 '),
            ('baseline_run2', 'desktop.sh', ' ' ),
            ('spec_connect_0_sockets_run2', 'desktop.sh', '--firefox.preference network.http.speculative-parallel-limit:0 '),
            ('spec_connect_20_sockets_run2', 'desktop.sh', '--firefox.preference network.http.speculative-parallel-limit:20 '),
            ('spec_connect_30_sockets_run2', 'desktop.sh', '--firefox.preference network.http.speculative-parallel-limit:30 ')]
