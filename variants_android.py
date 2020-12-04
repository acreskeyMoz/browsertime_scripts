# Define the apps to test
#  The last parameter can be a firefox pref string (e.g '--firefox.preference network.http.rcwn.enabled:false ')

# apk locations
fennec68_location = '~/dev/experiments/fennec_gve_fenix/binaries/fennec-68.3.0.multi.android-aarch64.apk'
fenix_nightly = '~/dev/experiments/fennec_gve_fenix/binaries/fenix_nightly_aarch74.apk'

variants = [('fennec68', 'fennec.sh', 'org.mozilla.firefox', fennec68_location, ''),
            ('fenix', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly, '' )]