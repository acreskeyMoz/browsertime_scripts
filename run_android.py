import os
import time
import sys

# A script for generating performance results from browsertime
#  For each site in sites.txt
#     For each app (name, script, package name, apk location, custom prefs)
#        Measure pageload on the given site, n iterations

host_ip = '192.168.86.21'  # for WebPageReplay
android_serial='9C091FFBA000BP'
geckodriver_path='/Users/acreskey/dev/gecko-driver/0.26/geckodriver'
browsertime_bin='/Users/acreskey/tools/mozilla_browsertime/browsertime/bin/browsertime.js'

iterations = 1

# apk locations
fennec68_location = '~/dev/experiments/fennec_gve_fenix/binaries/fennec-68.3.0.multi.android-aarch64.apk'
gve_location = '~/dev/experiments/fennec_gve_fenix/binaries/geckoview_example_01_09_aarch64.apk'
fenix_location = '~/dev/experiments/fennec_gve_fenix/binaries/fenix_02_12_aarch64.apk'
# fenix source:
# https://firefox-ci-tc.services.mozilla.com/api/index/v1/task/project.mobile.fenix.v2.fennec-production.2020.02.12.latest/artifacts/public/build/arm64-v8a/geckoBeta/target.apk

# Define the apps to test
#  The last parameter can be a firefox pref string (e.g '--firefox.preference network.http.rcwn.enabled:false ')
variants = [('fennec68', 'fennec.sh', 'org.mozilla.firefox', fennec68_location, ''),
            ('gve', 'gve.sh', 'org.mozilla.geckoview_example', gve_location, ''),
            ('fenix', 'fenix.sh', 'org.mozilla.firefox', fenix_location, '' )]

common_options = ' '

# Restore the speculative connection pool that marionette disables
common_options += '--firefox.preference network.http.speculative-parallel-limit:6 '

# Disable WebRender
common_options += '--firefox.preference gfx.webrender.force-disabled:true '

# Use WebPageReplay?
#common_options += '--firefox.preference network.dns.forceResolve:' + host_ip + ' --firefox.acceptInsecureCerts true '

# Gecko profiling?
#common_options += '--firefox.geckoProfiler true --firefox.geckoProfilerParams.interval 10  --firefox.geckoProfilerParams.features "js,stackwalk,leaf" --firefox.geckoProfilerParams.threads "GeckoMain,Compositor,ssl,socket,url,cert,js" '

def main():

    common_args = common_options + '--pageCompleteWaitTime 10000 '
    common_args += ' preload.js '

    common_args += '-n %d ' % iterations 
    common_args += '--visualMetrics true --video true --firefox.windowRecorder false '
    common_args += '--videoParams.addTimer false --videoParams.createFilmstrip false --videoParams.keepOriginalVideo true '

    file = open('sites.txt', 'r')
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

            env = 'env ANDROID_SERIAL=%s PACKAGE=%s GECKODRIVER_PATH=%s BROWSERTIME_BIN=%s ' %(android_serial, package_name, geckodriver_path, browsertime_bin)
    
            print('Starting ' + name + ', ' + package_name + ', from ' + apk_location + ' with arguments ' + options)
            os.system('adb uninstall ' + package_name)

            install_cmd = 'adb install ' + apk_location
            print(install_cmd)
            os.system(install_cmd)

            completeCommand = env + ' bash ' + script + ' ' + common_args + options + url_arg + result_arg + name +'" '
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
