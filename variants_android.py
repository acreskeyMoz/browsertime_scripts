# Define the apps to test
#  The last parameter can be a firefox pref string (e.g '--firefox.preference network.http.rcwn.enabled:false ')

# customize these apk locations:
fenix_beta = '~/dev/experiments/fennec_gve_fenix/binaries/fenix.beta.2020.11.30.apk'
fennec68 = '~/dev/experiments/fennec_gve_fenix/binaries/fennec-68.3.0.multi.android-aarch64.apk'
fenix_nightly = '~/dev/experiments/fennec_gve_fenix/binaries/fenix.nightly.2020.12.16_aarch64.apk'

# the last parameter can be used to pass through a firefox preference. eg. ('--firefox.preference network.preload:false ')
variants = [ ('fenix', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly, '' ),
             ('fenix_beta', 'fenix.sh', 'org.mozilla.firefox_beta', fenix_beta, ' ' ),
             ('fennec68', 'fennec.sh', 'org.mozilla.firefox', fennec68, '')]
