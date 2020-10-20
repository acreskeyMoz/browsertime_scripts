import os
import time
import sys
import argparse


# A script for generating performance results from browsertime
#   
#  For each site in sites.txt
#     For each app (name, script, package name, apk location, custom prefs)
#        Measure pageload on the given site, n iterations


# Customize the app locations and the variants that you wish to compare:

# apk locations
fennec68_location = '~/dev/experiments/fennec_gve_fenix/binaries/fennec-68.3.0.multi.android-aarch64.apk'
gve_location = '~/dev/experiments/fennec_gve_fenix/binaries/geckoview_example_01_09_aarch64.apk'
fenix_location = '~/dev/experiments/fennec_gve_fenix/binaries/fenix.v2.fennec-production.2020.02.26.apk'

# Define the apps to test
#  The last parameter can be a firefox pref string (e.g '--firefox.preference network.http.rcwn.enabled:false ')
variants = [('fennec68', 'fennec.sh', 'org.mozilla.firefox', fennec68_location, ''),
            ('fenix', 'fenix.sh', 'org.mozilla.firefox', fenix_location, '' )]


global options
parser = argparse.ArgumentParser(
    description="",
    prog="run_android",
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
    "--serial",
    help="Android serial #",
)
parser.add_argument(
    "--webrender",
    action="store_false",
    help="Enable webrender (default: disabled)",
)
parser.add_argument(
    "--profile",
    action="store_true",
    default=False,
    help="Enable profiling",
)

parser.add_argument(
    "--visualmetrics",
    action="store_true",
    default=False,
    help="Calculate visualmetrics (SI/CSI/PSI)",
)
options = parser.parse_args()

base = os.path.dirname(os.path.realpath(__file__))

if options.sites != None:
    sites = options.sites
else:
    sites = os.path.join(base, "sites.txt")

if options.serial:
    android_serial = options.serial
else:
    android_serial='89PX0DD5W'

geckodriver_path='/Users/acreskey/dev/gecko-driver/0.26/geckodriver'
browsertime_bin='/Users/acreskey/tools/test_parent_process_nav_in_bt/browsertime/bin/browsertime.js'

launch_url = "data:,"
testScript = "preload.js"

common_options = ' '

# Restore the speculative connection pool that marionette disables
common_options += '--firefox.preference network.http.speculative-parallel-limit:6 '

if (options.webrender):
    common_options += '--firefox.preference gfx.webrender.enabled:true '
else:
    common_options += '--firefox.preference gfx.webrender.force-disabled:true '

# Gecko profiling?
if (options.profile):
    common_options += '--firefox.geckoProfiler true --firefox.geckoProfilerParams.interval 10  --firefox.geckoProfilerParams.features "java,js,stackwalk,leaf" --firefox.geckoProfilerParams.threads "GeckoMain,Compositor,ssl,socket,url,cert,js" '

if options.debug:
    common_options += '-vvv '

if options.visualmetrics:
    common_options += '--visualMetrics true --video true --visualMetricsContentful true --visualMetricsPerceptual true --firefox.windowRecorder false '
    common_options += '--videoParams.addTimer false --videoParams.createFilmstrip false --videoParams.keepOriginalVideo true '
else:
    common_options += '--visualMetrics false '

common_options += '-n %d ' % options.iterations 

# Use WebPageReplay?
#common_options += '--firefox.preference network.dns.forceResolve:' + host_ip + ' --firefox.acceptInsecureCerts true '

def main():

    common_args = common_options + '--pageCompleteWaitTime 10000 '

    site_count = len(open(sites).readlines())

    file = open(sites, 'r')
    for site_num, line in enumerate(file):
        url = line.strip()

        print('Loading url: ' + url + ' with browsertime')
        url_arg = '--browsertime.url \"' + url + '\" '
        result_arg = '--resultDir "browsertime-results/' + cleanUrl(url) + '/'

        for variant_num, variant in enumerate(variants):
            name = variant[0]
            script = variant[1]
            package_name = variant[2]
            apk_location = variant[3]
            variant_options = variant[4]

            env = 'env ANDROID_SERIAL=%s PACKAGE=%s GECKODRIVER_PATH=%s BROWSERTIME_BIN=%s LAUNCH_URL=%s' %(android_serial, package_name, geckodriver_path, browsertime_bin, launch_url)
    
            print('Starting ' + name + ', ' + package_name + ', from ' + apk_location + ' with arguments ' + variant_options)
            if apk_location:
                uninstall_cmd = 'adb uninstall ' + package_name
                print(uninstall_cmd)
                os.system(uninstall_cmd)

                install_cmd = 'adb install ' + apk_location
                print(install_cmd)
                os.system(install_cmd)
            
            completeCommand = env + ' bash ' + script + ' ' + common_args + testScript +  ' ' + variant_options + url_arg + result_arg + name +'" '
            print( "\ncommand " + completeCommand)

            print_progress(site_count, len(variants), site_num, variant_num)
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

def print_progress(site_count, variants, current_site, current_variant):
    total = site_count * variants    
    # sites processed so far + variants completed for current site
    current = (current_site * variants) + current_variant
    progress_percent = float(current) / float(total)

    progress_bar_length = 78
    print ('Progress')
    print ('[' +  '=' * int(progress_bar_length * progress_percent) + ' ' * int(progress_bar_length * (1.0-progress_percent)) + ']')


if __name__=="__main__":
   main()
