# Define the apps to test
#  The last parameter can be a firefox pref string (e.g '--firefox.preference network.http.rcwn.enabled:false ')

# customize these apk locations:
#fenix_nightly = '/Users/acreskey/tools/browsertime_tests/binaries/fenix_nightly.2024.04.23.arm64-v8a.apk'
fenix_nightly = '/Users/acreskey/tools/browsertime_tests/binaries/fenix_nightly.2024.05.16.arm64-v8a.apk'

fenix_beta = '/Users/acreskey/tools/browsertime_tests/binaries/fenix-beta.2024.02.23.arm64-v8a.apk'
fenix_release = '/Users/acreskey/tools/browsertime_tests/binaries/fenix-release.2024.02.13.arm64-v8a.apk'

geckoview_example = '/Users/acreskey/tools/browsertime_tests/binaries/geckoview_example.2024.05.13.apk'

#org.mozilla.geckoview_example
#org.mozilla.fenix

variants = [('fenix_nightly_05_16_https_rr_off', 'fenix.sh', 'org.mozilla.fenix', '', '--firefox.preference network.dns.native_https_query:false '),
            ('fenix_nightly_05_16', 'fenix.sh', 'org.mozilla.fenix', '', ' '),
            ('fenix_nightly_05_16_reduce_deprioritization_rr_off', 'fenix.sh', 'org.mozilla.fenix', '', '--firefox.preference page_load.deprioritization_period:2500 --firefox.preference network.dns.native_https_query:false '),
            ('Chrome_122', 'chrome.sh', 'com.android.chrome', '', '--browser chrome '),
            ('fenix_nightly_05_16_https_rr_off_run2', 'fenix.sh', 'org.mozilla.fenix', '', '--firefox.preference network.dns.native_https_query:false '),
            ('fenix_nightly_05_16_run2', 'fenix.sh', 'org.mozilla.fenix', '', ' '),
            ('fenix_nightly_05_16_reduce_deprioritization_rr_off_run2', 'fenix.sh', 'org.mozilla.fenix', '', '--firefox.preference page_load.deprioritization_period:2500 --firefox.preference network.dns.native_https_query:false '),
            ('Chrome_122_run2', 'chrome.sh', 'com.android.chrome', '', '--browser chrome ')]


# variants = [ ('geckoview_example', 'gve.sh', 'org.mozilla.geckoview_example', '', ''),
#               ('geckoview_example_native_rr_off', 'gve.sh', 'org.mozilla.geckoview_example', '', '--firefox.preference network.dns.native_https_query:false '),
#               ('Chrome_122', 'chrome.sh', 'com.android.chrome', '', '--browser chrome ')]

# variants = [ ('geckoview_example', 'gve.sh', 'org.mozilla.geckoview_example', '', ''),
#              ('Chrome_122', 'chrome.sh', 'com.android.chrome', '', '--browser chrome ')]

# variants = [ ('geckoview_example', 'gve.sh', 'org.mozilla.geckoview_example', '', ''),
#             ('Chrome_122', 'chrome.sh', 'com.android.chrome', '', '--browser chrome ')]

#variants = [ ('fenix_nightly', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly, '') ]

#variants = [ ('fenix_beta_02_23_24', 'fenix.sh', 'org.mozilla.firefox_beta', '', '')]

#variants = [ ('fenix_nightly', 'fenix.sh', 'org.mozilla.fenix', '', '') ]

#variants = [ ('Chrome_122', 'chrome.sh', 'com.android.chrome', '', '--browser chrome ') ]

# variants = [ ('fenix_nightly', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly, ''),
#              ('Chrome_122', 'chrome.sh', 'com.android.chrome', '', '--browser chrome '),
#               ('fenix_nightly_run2', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly, ''),
#              ('Chrome_122_run2', 'chrome.sh', 'com.android.chrome', '', '--browser chrome ') ]


# variants = [ ('fenix_beta_02_23_24', 'fenix.sh', 'org.mozilla.firefox_beta', fenix_beta, ''),
#              ('Chrome_122', 'chrome.sh', 'com.android.chrome', '', '--browser chrome '),
#              ('fenix_beta_reduce_deprioritization', 'fenix.sh', 'org.mozilla.firefox_beta', fenix_beta, '--firefox.preference page_load.deprioritization_period:2500 '),
#              ('fenix_beta_disable_lower_priority_refresh', 'fenix.sh', 'org.mozilla.firefox_beta', fenix_beta, '--firefox.preference layout.lower_priority_refresh_driver_during_load:false '),
#              ('fenix_beta_02_23_24_run2', 'fenix.sh', 'org.mozilla.firefox_beta', fenix_beta, ''),
#              ('Chrome_122_run2', 'chrome.sh', 'com.android.chrome', '', '--browser chrome '),
#              ('fenix_beta_reduce_deprioritization_run2', 'fenix.sh', 'org.mozilla.firefox_beta', fenix_beta, '--firefox.preference page_load.deprioritization_period:2500 '),
#              ('fenix_beta_disable_lower_priority_refresh', 'fenix.sh', 'org.mozilla.firefox_beta', fenix_beta, '--firefox.preference layout.lower_priority_refresh_driver_during_load:false ') ]

# variants = [ ('fenix_nightly', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly, ' '),
#              ('fenix_nightly_https_rr_off', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly, '--firefox.preference network.dns.native_https_query:false '),
#              ('Chrome_122', 'chrome.sh', 'com.android.chrome', '', '--browser chrome '),
#              ('fenix_nightly_run2', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly, ' '),
#              ('fenix_nightly_https_rr_off_run2', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly, '--firefox.preference network.dns.native_https_query:false '),
#              ('Chrome_122_run2', 'chrome.sh', 'com.android.chrome', '', '--browser chrome ')]

# variants = [ ('fenix_nightly', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly, ' '),
#              ('fenix_nightly_https_rr_off', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly, '--firefox.preference network.dns.native_https_query:false '),
#              ('fenix_reduce_deprioritization', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly, '--firefox.preference page_load.deprioritization_period:2500 '),
#              ('fenix_disable_lower_priority_refresh', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly, '--firefox.preference layout.lower_priority_refresh_driver_during_load:false '),
#              ('fenix_parent_controlled_load', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly, '--firefox.preference browser.tabs.documentchannel.parent-controlled:true '),
#              ('Chrome_122', 'chrome.sh', 'com.android.chrome', '', '--browser chrome '),
#              ('fenix_nightly_run2', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly, ' '),
#              ('fenix_nightly_https_rr_off_run2', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly, '--firefox.preference network.dns.native_https_query:false '),
#              ('fenix_reduce_deprioritization_run2', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly, '--firefox.preference page_load.deprioritization_period:2500 '),
#              ('fenix_disable_lower_priority_refresh_run2', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly, '--firefox.preference layout.lower_priority_refresh_driver_during_load:false '),
#              ('fenix_parent_controlled_load_run2', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly, '--firefox.preference browser.tabs.documentchannel.parent-controlled:true '),
#              ('Chrome_122_run2', 'chrome.sh', 'com.android.chrome', '', '--browser chrome ') ]

# variants = [ ('fenix_nightly', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly, ''),
#             ('Chrome_122', 'chrome.sh', 'com.android.chrome', '', '--browser chrome ') ]




# variants = [ ('fenix_beta_02_23_24', 'fenix.sh', 'org.mozilla.firefox_beta', fenix_beta, ''),
#              ('Chrome_122', 'chrome.sh', 'com.android.chrome', '', '--browser chrome '),
#              ('fenix_beta_reduce_deprioritization', 'fenix.sh', 'org.mozilla.firefox_beta', fenix_beta, '--firefox.preference page_load.deprioritization_period:2500 '),
#              ('fenix_beta_disable_lower_priority_refresh', 'fenix.sh', 'org.mozilla.firefox_beta', fenix_beta, '--firefox.preference layout.lower_priority_refresh_driver_during_load:false '),
#              ('fenix_beta_02_23_24_run2', 'fenix.sh', 'org.mozilla.firefox_beta', fenix_beta, ''),
#              ('Chrome_122_run2', 'chrome.sh', 'com.android.chrome', '', '--browser chrome '),
#              ('fenix_beta_reduce_deprioritization_run2', 'fenix.sh', 'org.mozilla.firefox_beta', fenix_beta, '--firefox.preference page_load.deprioritization_period:2500 '),
#              ('fenix_beta_disable_lower_priority_refresh', 'fenix.sh', 'org.mozilla.firefox_beta', fenix_beta, '--firefox.preference layout.lower_priority_refresh_driver_during_load:false ') ]


#variants = [ ('fenix_nightly', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly, '') ]
#variants = [ ('fenix_release', 'fenix.sh', 'org.mozilla.firefox', fenix_release, '')]

#variants = [ ('fenix_beta', 'fenix.sh', 'org.mozilla.firefox_beta', fenix_beta, '')]



#variants = [ ('Chrome', 'chrome.sh', 'com.android.chrome', '', '--browser chrome ') ]

#variants = [ ('fenix_nightly', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly, '') ]
#              ('chrome', 'fenix.sh', 'org.mozilla.firefox_beta', fenix_beta, ' ' ),
#              ('fennec68_run2', 'fennec.sh', 'org.mozilla.firefox', fennec68, ''),
#              ('fenix_beta_12_18_run2', 'fenix.sh', 'org.mozilla.firefox_beta', fenix_beta, ' ' )]


# the last parameter can be used to pass through a firefox preference. eg. ('--firefox.preference network.preload:false ')
# variants = [ ('fennec68', 'fennec.sh', 'org.mozilla.firefox', fennec68, ''),
#              ('fenix_beta_12_18', 'fenix.sh', 'org.mozilla.firefox_beta', fenix_beta, ' ' ),
#              ('fennec68_run2', 'fennec.sh', 'org.mozilla.firefox', fennec68, ''),
#              ('fenix_beta_12_18_run2', 'fenix.sh', 'org.mozilla.firefox_beta', fenix_beta, ' ' )]
