import argparse
import importlib
import os
import sys
import time

# A script for larger browsertime performance experiments
#   
#  For each site in sites.txt
#     For each app (name, script, package name, apk location, custom prefs)
#        Measure pageload on the given site, n iterations

# Customize these paths, or pass by argument
#default_firefox_binary_path='/Applications/Firefox Nightly.app/Contents/MacOS/firefox'
default_firefox_binary_path='/Users/acreskey/dev/mc3/obj-ff-dbg/dist/Nightly.app/Contents/MacOS/firefox'

browsertime_bin='/Users/acreskey/tools/browsertime_tests/browsertime/bin/browsertime.js'
#geckodriver_path='/Users/acreskey/tools/browsertime_tests/geckodriver.0.34.0/geckodriver'
geckodriver_path='/Users/acreskey/tools/browsertime_tests/geckodriver_marc_fix/geckodriver'
#android_serial='89PX0DD5W'
android_serial='R5CW33A9FPA'

global options
parser = argparse.ArgumentParser(
    description="",
    prog="run_test",
)

parser.add_argument(
    "--debug",
    action="store_true",
    default=False,
    help="pass debugging flags to browsertime (-vvv)",
)

parser.add_argument(
    "-i",
    "-n",
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
    "--desktop",
    action="store_true",
    default=False,
    help="Desktop or mobile",
)

parser.add_argument(
    "--binarypath",
    help="path to firefox binary (desktop)",
)

parser.add_argument(
    "--webrender",
    action="store_true",
    default=True,
    help="Enable webrender (default: enabled)",
)

parser.add_argument(
    "--fullscreen",
    action="store_true",
    default=False,
    help="Run test in full-screen (Desktop)",
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

parser.add_argument(
    "--wpr_host_ip",
    help="WebPageReplay host IP (optional)",
)

parser.add_argument(
    "--reload",
    action="store_true",
    default=False,
    help="test reload of the URL",
)

parser.add_argument(
    "--condition",
    action="store_true",
    default=False,
    help="load a site before the target URL",
)

parser.add_argument(
    "--prefs",
    help="Firefox preferences to use for all runs",
)

parser.add_argument(
    "--variants",
    help="python module with the variants defined, e.g. variants_android",
)

parser.add_argument(
    "--geckodriver",
    help="path to geckodriver",
)

parser.add_argument(
    "--browsertime",
    help="path to browsertime/bin/browsertime.js",
)

parser.add_argument(
    "--output_path",
    help="Path for the browsertime json (defaults to 'browsertime-results')",
)

parser.add_argument(
    "--restart_adb",
    action="store_true",
    default=False,
    help="Restart adb between variants (workaround to adb file descriptor leak)",
)


parser.add_argument(
    "--perfstats",
    action="store_true",
    default=False,
    help="Collect PerfStats",
)

parser.add_argument(
    "--android_app_storage",
    action="store_true",
    default=False,
    help="Set geckodriver android app storage to true ",
)

parser.add_argument(
    "--android_sdcard_storage",
    action="store_true",
    default=False,
    help="Set geckodriver android sdcard storage to true ",
)

parser.add_argument(
    "--moz_logs",
    action="store_true",
    default=False,
    help="Collect moz logs ",
)

parser.add_argument(
    "--chromelogs",
    action="store_true",
    default=False,
    help="Enable chrome logs, --chrome.collectPerfLog --chrome.collectNetLog ",
)

parser.add_argument(
    "--chrometrace",
    action="store_true",
    default=False,
    help="Enable chrome trace ",
)

options = parser.parse_args()

base = os.path.dirname(os.path.realpath(__file__))

if options.reload:
    preload_script = os.path.join(base, 'reload.js')
elif options.condition:
    preload_script = os.path.join(base, 'preload.js')
else:
    preload_script = os.path.join('preload_slim.js')

if options.variants != None:
    print('Using variant file ' + options.variants)
    variants_import = importlib.import_module(options.variants)
else:
    if options.desktop:
        variants_import = importlib.import_module('variants_desktop')
    else:
        variants_import = importlib.import_module('variants_android')

if options.sites != None:
    sites = options.sites
else:
    sites = os.path.join(base, 'sites.txt')

if options.serial:
    android_serial = options.serial

if options.geckodriver:
    geckodriver_path = options.geckodriver

if options.browsertime:
    browsertime_bin = options.browsertime

if options.output_path:
    output_path = options.output_path
else:
    output_path = 'browsertime-results'

additional_prefs = options.prefs
if additional_prefs != None:
    print("Additional_prefs = " + additional_prefs, flush=True)

launch_url = "data:,"

common_options = '--pageCompleteWaitTime 10000 '

# Use the parent process initiated pagedload instead of window.location writes
common_options += '--webdriverPageload true '

# flush DNS, where possible
common_options += '--flushDNS true '

if options.webrender:
    print("Enabling WebRender", flush=True)
    common_options += '--firefox.preference gfx.webrender.enabled:true --firefox.preference gfx.webrender.precache-shaders:true '
else:
    common_options += '--firefox.preference gfx.webrender.force-disabled:true '

if options.fullscreen:
    common_options += '--viewPort maximize '

# Gecko profiling?
if (options.profile):
    common_options += '--firefox.geckoProfiler true --firefox.geckoProfilerParams.interval 10  --firefox.geckoProfilerParams.features "java,js,stackwalk,leaf" --firefox.geckoProfilerParams.threads "GeckoMain,Compositor,ssl,socket,url,cert,js" '

if options.debug:
    common_options += '-vvv '

if options.visualmetrics:
    common_options += '--visualMetrics true --video true --visualMetricsContentful true --visualMetricsPerceptual true --firefox.windowRecorder false '
    common_options += '--videoParams.addTimer false --videoParams.createFilmstrip false --videoParams.keepOriginalVideo false '
else:
    common_options += '--visualMetrics false '

common_options += '-n %d ' % options.iterations 

if options.reload:
    common_options += '--reload '
    common_options += '--firefox.preference dom.ipc.keepProcessesAlive.webIsolated.timed.max:30 '

if additional_prefs != None:
    wordlist = additional_prefs.split()
    for pref in wordlist:
        common_options += '--firefox.preference ' + pref + ' '
        print('Added "' + '--firefox.preference ' + pref + ' ' + '"', flush=True)

if options.desktop:
    if options.binarypath != None:
        firefox_binary_path = options.binarypath
    else:
        firefox_binary_path = default_firefox_binary_path

if options.perfstats:
    print("Capturing PerfStats")
    common_options += '--firefox.perfStats '

if options.wpr_host_ip != None:
    print("Adding WebPageReplay options", flush=True)
    common_options += '--firefox.preference network.dns.forceResolve:' + options.wpr_host_ip + ' --firefox.preference network.socket.forcePort:"80=4040;443=4041"' + ' --firefox.acceptInsecureCerts true '

if options.android_app_storage:
    print("Enabling geckodriverArgs android-storage app")
    common_options += '--firefox.geckodriverArgs="--android-storage" --firefox.geckodriverArgs="app" '

if options.android_sdcard_storage:
    print("Enabling geckodriverArgs android-storage sdcard")
    common_options += '--firefox.geckodriverArgs="--android-storage" --firefox.geckodriverArgs="sdcard" '

if options.moz_logs:
    print("Collecting mozlogs")
    common_options += '--firefox.collectMozLog --firefox.setMozLog="timestamp,nsHttp:5,nsHostResolver:5,cache2:5,nsSocketTransport:5,socket,NetworkPredictor:5,nsIOService:5,profilermarkers:5" '

if options.chromelogs:
    print("Enabling Chrome perf logs")
    common_options += '--chrome.collectPerfLog --chrome.collectNetLog '

if options.chrometrace:
    print("Collect Chrome traces")
    common_options += '--chrome.traceCategories="disabled-by-default-devtools.timeline,disabled-by-default-devtools.timeline.frame,disabled-by-default-devtools.timeline.stack,disabled-by-default-v8.compile,disabled-by-default-lighthouse"  '

def main():
    site_count = len(open(sites).readlines())

    file = open(sites, 'r')
    for site_num, line in enumerate(file):
        url = line.strip()

        print('Loading url: ' + url + ' with browsertime')

        url_arg = '--browsertime.url \"' + url + '\" '
        result_arg = '--resultDir "' + os.path.join(output_path, cleanUrl(url))

        for variant_num, variant in enumerate(variants_import.variants):
            name = variant[0]
            script = variant[1]

            if options.desktop:
                env = 'env GLEAN_DEBUG_VIEW_TAG=browsertimetest FIREFOX_BINARY_PATH="%s" GECKODRIVER_PATH=%s BROWSERTIME_BIN=%s LAUNCH_URL=%s' %(firefox_binary_path, geckodriver_path, browsertime_bin, launch_url)
                variant_options = variant[2]
                print('Starting ' + firefox_binary_path + ' with arguments ' + variant_options)
            else:
                package_name = variant[2]
                apk_location = variant[3]
                variant_options = variant[4]

                if options.restart_adb:
                    print('Restarting adb')
                    os.system('adb kill-server')
                    os.system('adb devices')

                env = 'env ANDROID_SERIAL=%s PACKAGE=%s GECKODRIVER_PATH=%s BROWSERTIME_BIN=%s LAUNCH_URL=%s' %(android_serial, package_name, geckodriver_path, browsertime_bin, launch_url)
                print('Starting ' + name + ', ' + package_name + ', from ' + apk_location + ' with arguments ' + variant_options)
                if apk_location:
                    uninstall_cmd = 'adb uninstall ' + package_name
                    print(uninstall_cmd)
                    os.system(uninstall_cmd)

                    install_cmd = 'adb install ' + apk_location
                    print(install_cmd)
                    os.system(install_cmd)

            completeCommand = env + ' bash ' + script + ' ' + common_options  + ' ' + preload_script +  ' ' + variant_options + url_arg + os.path.join(result_arg, name) +'" '
            print( "\ncommand " + completeCommand)

            print_progress(site_count, len(variants_import.variants), site_num, variant_num)
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

def print_progress(site_count, num_variants, current_site, current_variant):
    total = site_count * num_variants    
    # sites processed so far + variants completed for current site
    current = (current_site * num_variants) + current_variant
    progress_percent = float(current) / float(total)

    progress_bar_length = 78
    print ('Progress')
    print ('[' +  '=' * int(progress_bar_length * progress_percent) + ' ' * int(progress_bar_length * (1.0-progress_percent)) + ']')


if __name__=="__main__":
   main()
