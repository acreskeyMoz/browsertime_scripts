# Define the apps to test
#  The last parameter can be a firefox pref string (e.g '--firefox.preference dom.prefetch_dns_for_anchor:false ')
variants = [('baseline', 'desktop.sh', '--firefox.preference dom.prefetch_dns_for_anchor:false ' ),
            ('dns_prefetch', 'desktop.sh', '--firefox.preference dom.prefetch_dns_for_anchor:false  --firefox.preference network.dns.disablePrefetchFromHTTPS:true '),
            ('baseline_run2', 'desktop.sh', '--firefox.preference dom.prefetch_dns_for_anchor:false ' ),
            ('dns_prefetch_run2', 'desktop.sh', '--firefox.preference dom.prefetch_dns_for_anchor:false  --firefox.preference network.dns.disablePrefetchFromHTTPS:true ' )]
