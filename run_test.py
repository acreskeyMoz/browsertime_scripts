import os
import time
import sys
import argparse

# A script for generating performance results from browsertime
#  For each site in sites.txt
#     For each app (name, script, package name, apk location, custom prefs)
#        Measure pageload on the given site, n iterations

global options

parser = argparse.ArgumentParser(
    description="",
    prog="run_linux",
)
parser.add_argument(
    "--debug",
    action="store_true",
    default=False,
    help="pass debugging flags to browsertime (-vvv)",
)
parser.add_argument(
    "-i",
    "--iterations",
    type=int,
    default=3,
    help="Number of iterations",
)
parser.add_argument(
    "-s",
    "--sites",
    help="File of sites",
)
parser.add_argument(
    "--url",
    help="specific site",
)
parser.add_argument(
    "--desktop",
    action="store_true",
    default=True,
    help="Desktop or mobile",
)
parser.add_argument(
    "--serial",
    help="Android serial #",
)
parser.add_argument(
    "--perf",
    action="store_true",
    default=False,
    help="Record a trace using perf",
)
parser.add_argument(
    "--webrender",
    action="store_true",
    default=False,
    help="Enable webrender (default: disabled)",
)
parser.add_argument(
    "--profile",
    action="store_true",
    default=False,
    help="Enable profiling",
)
parser.add_argument(
    "--remoteAddr",
    help="geckodriver target IP:port",
)
parser.add_argument(
    "--visualmetrics",
    action="store_true",
    default=False,
    help="Calculate visualmetrics (SI/CSI/PSI)",
)
parser.add_argument(
    "--hdmicap",
    action="store_true",
    default=False,
    help="HDMI capture from /dev/video0",
)
parser.add_argument(
    "--path",
    help="path to firefox on the target",
)

options = parser.parse_args()

base = os.path.dirname(os.path.realpath(__file__))

remoteAddr = options.remoteAddr
visualmetrics = options.visualmetrics
hdmicapture = options.hdmicap
iterations = options.iterations
debug = options.debug
webrender = options.webrender
profile = options.profile
if options.sites != None:
    sites = options.sites
else:
    sites = base + "sites.txt"

arm64=True
desktop=options.desktop
perf = options.perf

host_ip = '192.168.86.21'  # for WebPageReplay
if options.serial:
    android_serial = options.serial
elif arm64:
    android_serial='9B121FFBA0031R'
else:
    android_serial='ZY322LH8WX'
geckodriver_path = base + 'geckodriver'
# XXX Fix!
browsertime_bin='/home/jesup/src/mozilla/pageload/tools/browsertime/node_modules/browsertime/bin/browsertime.js'
adb_bin='~/.mozbuild/android-sdk-linux/platform-tools/adb'

# apk locations
if (arm64):
    fennec68_location = base + 'fennec-68.3.0.multi.android-aarch64.apk'
    gve_location = base + 'geckoview_example_02_03_aarch64.apk'
    fenix_02_08_location = base + 'fenix_02_08_fennec-aarch64.apk'
    fenix_beta_location = base + 'fenix_02_28-aarch64.apk'
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
if (desktop):
    if (options.path != None):
        firefox_path = options.path
    else:
        firefox_path = '/tmp/firefox/firefox'
    variants = [
        ('e10s', base + 'desktop.sh', 'org.mozilla.firefox', fennec68_location,  base + 'preload.js', '--firefox.preference fission.autostart:false ' )
        ,('fission', base + 'desktop.sh', 'org.mozilla.firefox', fennec68_location,  base + 'preload.js', '--firefox.preference fission.autostart:true ' )
    ]
else:
  variants = [
    ('fenix_02_28_preload', base + 'fenix_release.sh', 'org.mozilla.firefox', fenix_beta_location,  base + 'preload.js', '' )
    ,('fenix_02_28_rel=preload', base + 'fenix_release.sh', 'org.mozilla.firefox', fenix_beta_location,  base + 'preload.js',
      '--firefox.preference network.preload:true --firefox.preference network.preload-experimental:true ')

#    ('fennec68_condprof', base + 'fennec_condprof.sh', 'org.mozilla.firefox', fennec68_location, base + 'preload_slim.js', '--firefox.disableBrowsertimeExtension ')
#    ,('fennec68_preload', base + 'fennec.sh', 'org.mozilla.firefox', fennec68_location, base + 'preload.js', '')
#    ,('gve', base + 'gve.sh','org.mozilla.geckoview_example', gve_location,  base + 'preload.js', '')
#    ,('fenix_beta', base + 'fenix_beta.sh', 'org.mozilla.fenix', fenix_beta_location,  base + 'preload.js', '' )
#    ,('fenix_02_28_condprof', base + 'fenix_release_condprof.sh', 'org.mozilla.firefox', fenix_beta_location,  base + 'preload_slim.js', '' )
#    ,('fenix_02_28_condprof_no_extension', base + 'fenix_release_condprof.sh', 'org.mozilla.firefox', fenix_beta_location,  base + 'preload_slim.js', '--firefox.disableBrowsertimeExtension ' )
#    ,('fenix_condprof', base + 'fenix_performancetest_condprof.sh', 'org.mozilla.fenix.performancetest', fenix_performancetest_location,  base + 'preload_slim.js', '' )
#    ,('fenix_condprof_no_settings', base + 'fenix_performancetest_condprof.sh', 'org.mozilla.fenix.performancetest', fenix_no_settings_location,  base + 'preload_slim.js', '' )
#      '--firefox.preference javascript.options.mem.gc_low_frequency_heap_growth:5 --firefox.preference javascript.options.mem.gc_allocation_threshold_mb:100000000 ')
#    ('fenix_performancetest', base + 'fenix_performancetest.sh', 'org.mozilla.fenix.performancetest', fenix_performance_location,  base + 'preload.js', '' )
#    ('fenix_beta', base + 'fenix_beta.sh', 'org.mozilla.fenix.beta', fenix_beta_location,  base + 'preload.js', '' )
   ]

common_options = ' '

# Restore the speculative connection pool that marionette disables
common_options += '--firefox.preference network.http.speculative-parallel-limit:6 '

if (webrender):
    # Enable WebRender
    common_options += '--firefox.preference gfx.webrender.enabled:true '
else:
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
if (profile):
    common_options += '--firefox.geckoProfiler true --firefox.geckoProfilerParams.interval 1  --firefox.geckoProfilerParams.features "js,stackwalk,leaf" --firefox.geckoProfilerParams.threads "GeckoMain,Compositor,Socket,IO" --firefox.geckoProfilerParams.bufferSize 100000000 '

def main():

    print('Running... (path =' + firefox_path)
    env = 'env ANDROID_SERIAL=%s GECKODRIVER_PATH=%s BROWSERTIME_BIN=%s FIREFOX_BINARY_LOCATION=%s' %(android_serial, geckodriver_path, browsertime_bin, firefox_path)
    if perf:
        env += " PERF=1"

    common_args = '-n %d ' % iterations 
    common_args += common_options + '--viewPort maximize '
    common_args += common_options + '--pageCompleteWaitTime 5000 '

    if debug:
        common_args += '-vvv '

    if (remoteAddr != None):
        common_args += '--selenium.url http://' + remoteAddr + ' '
    if (visualmetrics):
        common_args += '--visualMetrics=true --video=true '
        common_args += '--videoParams.addTimer false --videoParams.createFilmstrip false --videoParams.keepOriginalVideo true '
        if desktop:
            if hdmicapture:
                common_args += '--videoParams.captureCardHostOS linux --videoParams.captureCardFilename /tmp/output.mp4 '
            else:
                common_args += '--firefox.windowRecorder=true '
        else:
            common_args += '--firefox.windowRecorder=false '
    file = open(sites, 'r')
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

            if (desktop):
                print('Starting ' + name + ' with arguments ' + options)
            else:
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
