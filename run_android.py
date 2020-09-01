import os
import time
import sys

# A script for generating performance results from browsertime
#  For each site in sites.txt
#     For each app (name, script, package name, apk location, custom prefs)
#        Measure pageload on the given site, n iterations

arm64=True

iterations = 1
launch_url = "data:,"
testScript = "preload.js"

base = os.path.dirname(os.path.realpath(__file__))
host_ip = '192.168.86.21'  # for WebPageReplay
if (arm64):
    android_serial='9B121FFBA0031R'
else:
    android_serial='ZY322LH8WX'
geckodriver_path = base + 'geckodriver'
browsertime_bin='/home/jesup/src/mozilla/geckoview/tools/browsertime/node_modules/browsertime/bin/browsertime.js'
adb_bin='~/.mozbuild/android-sdk-linux/platform-tools/adb'

if (arm64):
    fennec68_location = base + 'fennec-68.3.0.multi.android-aarch64.apk'
    gve_location = base + 'geckoview_example_02_03_aarch64.apk'
    fenix_beta_location = base + 'fenix_02_08_fennec-aarch64.apk'
#    fenix_beta_location = base + 'fenix_andrew.apk'    
    fenix_performance_location = base + 'fenix_taskcluster_2_6_aarch64.apk'
else:
    fennec68_location = base + 'fennec-68.3.0.multi.android-arm.apk'
    gve_location = base + 'geckoview_example_02_03_arm32.apk'
    fenix_beta_location = base + 'fenix_andrew_arm32.apk'

# fenix source:
# https://firefox-ci-tc.services.mozilla.com/api/index/v1/task/project.mobile.fenix.v2.fennec-production.2020.02.12.latest/artifacts/public/build/arm64-v8a/gennckoBeta/target.apk

# Define the apps to test
#  The last parameter can be a firefox pref string (e.g '--firefox.preference network.http.rcwn.enabled:false ')
variants = [('fennec68', 'fennec.sh', 'org.mozilla.firefox', fennec68_location, ''),
            ('gve', 'gve.sh', 'org.mozilla.geckoview_example', gve_location, ''),
            ('fenix', 'fenix.sh', 'org.mozilla.firefox', fenix_beta_location, '' )]

# Chrome
# variants = [ ('chrome', 'chrome.sh', 'com.android.chrome', '', '' )]

common_options = ' '

# Restore the speculative connection pool that marionette disables
common_options += '--firefox.preference network.http.speculative-parallel-limit:6 '

# Disable WebRender
common_options += '--firefox.preference gfx.webrender.force-disabled:true '

# Use WebPageReplay?
#common_options += '--firefox.preference network.dns.forceResolve:' + host_ip + ' --firefox.acceptInsecureCerts true '

# Gecko profiling?
#common_options += '--firefox.geckoProfiler true --firefox.geckoProfilerParams.interval 5  --firefox.geckoProfilerParams.features "java,js,stackwalk,leaf" --firefox.geckoProfilerParams.threads "GeckoMain,Compositor,ssl,socket,url,cert,js" '

def main():

    common_args = common_options + '--pageCompleteWaitTime 5000 '
    common_args += ' ' +  base + 'preload.js '

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
            options = variant[4]

            # Cold start applink test? uncomment these and disable visual metrics/video
            # launch_url = url
            # testScript = "applink.js"
            # options += ' --processStartTime '

            env = 'env ANDROID_SERIAL=%s PACKAGE=%s GECKODRIVER_PATH=%s BROWSERTIME_BIN=%s LAUNCH_URL=%s' %(android_serial, package_name, geckodriver_path, browsertime_bin, launch_url)
    
            print('Starting ' + name + ', ' + package_name + ', from ' + apk_location + ' with arguments ' + options)
            if apk_location:
                        uninstall_cmd = adb_bin + ' uninstall ' + package_name
                        print(uninstall_cmd)
                        os.system(uninstall_cmd)

                        install_cmd = adb_bin + ' install ' + apk_location
                        print(install_cmd)
                        os.system(install_cmd)
            
            completeCommand = env + ' bash ' + script + ' ' + common_args + testScript +  ' ' + options + url_arg + result_arg + name +'" '
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
