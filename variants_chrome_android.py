# Define the apps to test
#  The last parameter can be a firefox pref string (e.g '--firefox.preference network.http.rcwn.enabled:false ')

# customize these apk locations:
fenix_nightly = '/Users/acreskey/tools/browsertime_tests/binaries/fenix-nightly.2024.02.24.arm64-v8a.apk'
fenix_beta = '/Users/acreskey/tools/browsertime_tests/binaries/fenix-beta.2024.02.23.arm64-v8a.apk'
fenix_release = '/Users/acreskey/tools/browsertime_tests/binaries/fenix-release.2024.02.13.arm64-v8a.apk'

#org.mozilla.geckoview_example
#org.mozilla.fenix

variants = [ ('Chrome_122', 'chrome.sh', 'com.android.chrome', '', '--browser chrome ')]

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
