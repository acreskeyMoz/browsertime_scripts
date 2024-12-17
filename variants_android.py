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

#variants = [('fenix_nightly', 'fenix.sh', 'org.mozilla.fenix', '', ' ')]
#variants = [ ('geckoview_example', 'gve.sh', 'org.mozilla.geckoview_example', '', '')]

variants = [('fenix_nightly', 'fenix.sh', 'org.mozilla.fenix', '', ' '),
            ('fenix_nightly_delay', 'fenix.sh', 'org.mozilla.fenix', '', '--firefox.preference browser.pageload.delay_change_events_by_MS:30 '),
            ('fenix_nightly_run2', 'fenix.sh', 'org.mozilla.fenix', '', ' '),
            ('fenix_nightly_delay_run2', 'fenix.sh', 'org.mozilla.fenix', '', '--firefox.preference browser.pageload.delay_change_events_by_MS:30 ')]

#variants = [('fenix_debug', 'fenix.sh', 'org.mozilla.fenix.debug', '', ' ')]


# variants = [('fenix_nightly', 'fenix.sh', 'org.mozilla.fenix', '', '--firefox.preference network.http.classifier.defer.enable:false ') ,
#             ('fenix_nightly_defer_classifier', 'fenix.sh', 'org.mozilla.fenix', '', '--firefox.preference network.http.classifier.defer.enable:true ') ,
#             ('Chrome_release', 'chrome.sh', 'com.android.chrome', '', '--browser chrome '),
#             ('fenix_nightly_run2', 'fenix.sh', 'org.mozilla.fenix', '', '--firefox.preference network.http.classifier.defer.enable:false ') ,
#             ('fenix_nightly_defer_classifier_run2', 'fenix.sh', 'org.mozilla.fenix', '', '--firefox.preference network.http.classifier.defer.enable:true '),
#             ('Chrome_release_run2', 'chrome.sh', 'com.android.chrome', '', '--browser chrome ')]

#variants = [('fenix_debug', 'fenix.sh', 'org.mozilla.fenix.debug', '', ' ')]
            
#variants = [('fenix_nightly', 'fenix.sh', 'org.mozilla.fenix', '', ' ')            ]


# variants = [('fenix_nightly', 'fenix.sh', 'org.mozilla.fenix', '', ' '),
#             ('Chrome_release', 'chrome.sh', 'com.android.chrome', '', '--browser chrome '),
#             ('fenix_nightly_run2', 'fenix.sh', 'org.mozilla.fenix', '', ' '),
#             ('Chrome_release_run2', 'chrome.sh', 'com.android.chrome', '', '--browser chrome ')
#             ]
