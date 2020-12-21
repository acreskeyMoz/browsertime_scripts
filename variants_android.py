# Define the apps to test
#  The last parameter can be a firefox pref string (e.g '--firefox.preference network.http.rcwn.enabled:false ')

# customize these apk locations:
fennec68 = '~/dev/experiments/fennec_gve_fenix/binaries/fennec-68.3.0.multi.android-aarch64.apk'
fenix_beta = '~/dev/experiments/fennec_gve_fenix/binaries/fenix.beta.2020.12.18.apk'

# the last parameter can be used to pass through a firefox preference. eg. ('--firefox.preference network.preload:false ')
variants = [ ('fennec68', 'fennec.sh', 'org.mozilla.firefox', fennec68, ''),
             ('fenix_beta_12_18', 'fenix.sh', 'org.mozilla.firefox_beta', fenix_beta, ' ' ),
             ('fennec68_run2', 'fennec.sh', 'org.mozilla.firefox', fennec68, ''),
             ('fenix_beta_12_18_run2', 'fenix.sh', 'org.mozilla.firefox_beta', fenix_beta, ' ' )]
