# Define the apps to test
#  The last parameter can be a firefox pref string (e.g '--firefox.preference dom.prefetch_dns_for_anchor:false ')
# variants = [('baseline', 'desktop.sh', '--firefox.preference dom.prefetch_dns_for_anchor:false ' ),
#             ('dns_prefetch', 'desktop.sh', '--firefox.preference dom.prefetch_dns_for_anchor:false  --firefox.preference network.dns.disablePrefetchFromHTTPS:true '),
#             ('baseline_run2', 'desktop.sh', '--firefox.preference dom.prefetch_dns_for_anchor:false ' ),
#             ('dns_prefetch_run2', 'desktop.sh', '--firefox.preference dom.prefetch_dns_for_anchor:false  --firefox.preference network.dns.disablePrefetchFromHTTPS:true ' )]

variants = [('cira', 'desktop.sh', ' --firefox.preference network.trr.mode:3 --firefox.preference network.trr.uri:https://private.canadianshield.cira.ca/dns-query ' ),
            ('cloudflare', 'desktop.sh', '--firefox.preference network.trr.mode:3 --firefox.preference network.trr.uri:https://mozilla.cloudflare-dns.com/dns-query  ' ),
            ('native', 'desktop.sh', ' --firefox.preference network.trr.mode:0 ' ),
            ('cira_run2', 'desktop.sh', ' --firefox.preference network.trr.mode:3 --firefox.preference network.trr.uri:https://private.canadianshield.cira.ca/dns-query ' ),
            ('cloudflare_run2', 'desktop.sh', '--firefox.preference network.trr.mode:3 --firefox.preference network.trr.uri:https://mozilla.cloudflare-dns.com/dns-query  ' ),
            ('native_run2', 'desktop.sh', ' --firefox.preference network.trr.mode:0 ' )]

# variants = [('chrome', 'chrome_desktop.sh', ' '),
#             ('baseline', 'desktop.sh', '--firefox.preference dom.prefetch_dns_for_anchor:false ' )]
