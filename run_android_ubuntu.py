import os
import time
import sys

# A script for generating performance results from browsertime
#  For each site in sites.txt
#     For each app (name, script, package name, apk location, custom prefs)
#        Measure pageload on the given site, n iterations

iterations = 40
arm64=True

base = '/home/jesup/src/mozilla/browsertime_on_android_scripts/'
host_ip = '192.168.86.21'  # for WebPageReplay
if (arm64):
    android_serial='9B121FFBA0031R'
else:
    android_serial='ZY322LH8WX'
geckodriver_path = base + 'geckodriver'
#browsertime_bin='/home/jesup/src/mozilla/browsertime/bin/browsertime.js'
browsertime_bin='/home/jesup/src/mozilla/geckoview/tools/browsertime/node_modules/browsertime/bin/browsertime.js'
adb_bin='~/.mozbuild/android-sdk-linux/platform-tools/adb'

# apk locations
if (arm64):
    fennec68_location = base + 'fennec-68.3.0.multi.android-aarch64.apk'
    gve_location = base + 'geckoview_example_02_03_aarch64.apk'
    fenix_02_08_location = base + 'fenix_02_08_fennec-aarch64.apk'
    fenix_beta_location = base + 'fenix_02_28-aarch64.apk'
#    fenix_beta_location = base + 'fenix_andrew.apk'    
#    fenix_performance_location = base + 'fenix_taskcluster_2_6_aarch64.apk'
    fenix_performancetest_location = base + 'performancetest.apk'
    fenix_no_settings_location = base + 'performancetest_delay.apk'
else:
    fennec68_location = base + 'fennec-68.3.0.multi.android-arm.apk'
    gve_location = base + 'geckoview_example_02_03_arm32.apk'
    fenix_beta_location = base + 'fenix_andrew_arm32.apk'

# Define the apps to test
# name, script location, appname, apk location, preload js location, options
# 'name' should not have any spaces in it
#  The last parameter can be a firefox pref string (e.g '--firefox.preference network.http.rcwn.enabled:false ')
variants = [
#    ('fennec68_condprof', base + 'fennec_condprof.sh', 'org.mozilla.firefox', fennec68_location, base + 'preload_slim.js', '--firefox.disableBrowsertimeExtension ')
#    ,('fennec68_preload', base + 'fennec.sh', 'org.mozilla.firefox', fennec68_location, base + 'preload.js', '')
#    ,('gve', base + 'gve.sh','org.mozilla.geckoview_example', gve_location,  base + 'preload.js', '')
#    ,('fenix_beta', base + 'fenix_beta.sh', 'org.mozilla.fenix', fenix_beta_location,  base + 'preload.js', '' )
#    ,('fenix_02_28_condprof', base + 'fenix_release_condprof.sh', 'org.mozilla.firefox', fenix_beta_location,  base + 'preload_slim.js', '' )
#    ,('fenix_02_28_condprof_no_extension', base + 'fenix_release_condprof.sh', 'org.mozilla.firefox', fenix_beta_location,  base + 'preload_slim.js', '--firefox.disableBrowsertimeExtension ' )
    ('fenix_02_28_preload', base + 'fenix_release.sh', 'org.mozilla.firefox', fenix_beta_location,  base + 'preload.js', '' )

    #    ,('fenix_condprof', base + 'fenix_performancetest_condprof.sh', 'org.mozilla.fenix.performancetest', fenix_performancetest_location,  base + 'preload_slim.js', '' )
#    ,('fenix_condprof_no_settings', base + 'fenix_performancetest_condprof.sh', 'org.mozilla.fenix.performancetest', fenix_no_settings_location,  base + 'preload_slim.js', '' )

    ,('fenix_02_28_rel=preload', base + 'fenix_release.sh', 'org.mozilla.firefox', fenix_beta_location,  base + 'preload.js',
#      '----firefox.preference javascript.options.mem.gc_low_frequency_heap_growth:5 --firefox.preference javascript.options.mem.gc_allocation_threshold_mb:100000000 ')
      '--firefox.preference network.preload:true --firefox.preference network.preload-experimental:true ')

#    ('fenix_performancetest', base + 'fenix_performancetest.sh', 'org.mozilla.fenix.performancetest', fenix_performance_location,  base + 'preload.js', '' )
#    ('fenix_beta', base + 'fenix_beta.sh', 'org.mozilla.fenix.beta', fenix_beta_location,  base + 'preload.js', '' )
]
#variants = [('fenix_beta', base + 'fenix_beta.sh', 'org.mozilla.fenix.beta', fenix_beta_location, '' )]

common_options = ' '

# Restore the speculative connection pool that marionette disables
common_options += '--firefox.preference network.http.speculative-parallel-limit:6 '

# Disable WebRender
common_options += '--firefox.preference gfx.webrender.force-disabled:true '

# Disable extension
#common_options += '--firefox.disableBrowsertimeExtension '

# enable rel=preload
#common_options += '--firefox.preference network.preload:true '
#common_options += '--firefox.preference network.preload-experimental:true '

# Use WebPageReplay?
#common_options += '--firefox.preference network.dns.forceResolve:' + host_ip + ' --firefox.acceptInsecureCerts true '

# Gecko profiling?
#common_options += '--firefox.geckoProfiler true --firefox.geckoProfilerParams.interval 5  --firefox.geckoProfilerParams.features "js,stackwalk,leaf" --firefox.geckoProfilerParams.threads "GeckoMain,socket,url,ava,cert,html" '

def main():

    print('Running...')
    env = 'env ANDROID_SERIAL=%s GECKODRIVER_PATH=%s BROWSERTIME_BIN=%s ' %(android_serial, geckodriver_path, browsertime_bin)
    
    common_args = common_options + '--pageCompleteWaitTime 5000 '

    common_args += '-n %d ' % iterations 
    common_args += '--visualMetrics true --video true --firefox.windowRecorder false '
    common_args += '--videoParams.addTimer false --videoParams.createFilmstrip false --videoParams.keepOriginalVideo true '

    file = open(base + 'sites.txt', 'r')
    for line in file:
        url = line.strip()

        print('Loading url: ' + url + ' with browsertime')
        url_arg = '--browsertime.url \"' + url + '\" '
        result_arg = '--resultDir "browsertime-results/' + cleanUrl(url) + '/'

        for variant in variants:
            name = variant[0]
            script = variant[1]
            package_name = variant[2]
            apk_location = variant[3]
            preload = variant[4]
            options = variant[5]
            
            print('Starting ' + name + ', ' + package_name + ', from ' + apk_location + ' with arguments ' + options)
            os.system(adb_bin + ' uninstall ' + package_name)

            install_cmd = adb_bin + ' install -d -r ' + apk_location
            print(install_cmd)
            os.system(install_cmd)

            completeCommand = env + ' bash ' + script + ' ' + common_args + preload + ' ' + options + url_arg + result_arg + name +'" '
            print( "\ncommand " + completeCommand)
            os.system(completeCommand)


def cleanUrl(url):
    cleanUrl = url.replace("http://", '')
    cleanUrl = cleanUrl.replace("https://", '')
    cleanUrl = cleanUrl.replace("/", "_")
    cleanUrl = cleanUrl.replace("?", "_")
    cleanUrl = cleanUrl.replace("&", "_")
    cleanUrl = cleanUrl.replace(":", ";")
    cleanUrl = cleanUrl.replace('\n', ' ').replace('\r', '')
    return cleanUrl

if __name__=="__main__":
   main()
