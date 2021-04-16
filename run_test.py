import argparse
import importlib
import os
import sys
import time
import glob
import subprocess
from subprocess import Popen, PIPE

# A script for larger browsertime performance experiments
#   
#  For each site in sites.txt
#     For each app (name, script, package name, apk location, custom prefs)
#        Measure pageload on the given site, n iterations

# Customize these paths, or pass by argument
browsertime_bin = './tools/browsertime/node_modules/browsertime/bin/browsertime.js'
#browsertime_bin='/Users/acreskey/tools/browsertime/bin/browsertime.js'
geckodriver_path='/Users/acreskey/dev/gecko-driver/0.26/geckodriver'
android_serial='89PX0DD5Waa'

def write_policies_json(location, policies_content):
    policies_file = os.path.join(location, "policies.json")
    
    with open(policies_file, "w") as fd:
        fd.write(policies_content)

def normalize_path(path):
    path = os.path.normpath(path)
    if os.name == "Windows":
        return path.replace("\\", "\\\\\\")
    return path


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
    "--verbose",
    "-v",
    action="store_true",
    default=False,
    help="Verbose output and logs",
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
    "--binarypath",
    "--path",
    help="path to firefox binary (desktop)",
)

parser.add_argument(
    "--wpr",
    help="connect to WPR replay IP (ports 4040/4041)",
)

parser.add_argument(
    "--mitm",
    help="connect to mitmproxy IP (port 8080)",
)

parser.add_argument(
    "--desktop",
    action="store_true",
    default=False,
    help="Desktop or mobile",
)

parser.add_argument(
    "--preload",
    help="preload script",
)

parser.add_argument(
    "--webrender",
    action="store_true",
    default=False,
    help="Enable webrender (default: disabled)",
)

parser.add_argument(
    "--fullscreen",
    action="store_true",
    default=False,
    help="Run test in full-screen (Desktop)",
)

parser.add_argument(
    "--url",
    help="specific site",
)

parser.add_argument(
    "--perf",
    action="store_true",
    default=False,
    help="Record a trace using perf",
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
    "--remoteAddr",
    help="geckodriver target IP:port",
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
    "--hdmicap",
    action="store_true",
    default=False,
    help="HDMI capture from /dev/video0",
)

parser.add_argument(
    "--restart_adb",
    action="store_true",
    default=False,
    help="Restart adb between variants (workaround to adb file descriptor leak)",
)

parser.add_argument(
    "--prefs_variant",
    help="prefs to use for a second run of everything",
)

parser.add_argument(
    "--log",
    help="MOZ_LOG values to set",
)
options = parser.parse_args()

base = os.path.dirname(os.path.realpath(__file__)) + '/'
print("Base: " + base)

if options.reload:
    preload_script = os.path.join(base, 'reload.js')
elif options.condition:
    preload_script = os.path.join(base, 'preload.js')
elif options.preload:
    preload_script = base + options.preload
else:
    preload_script = os.path.join('preload_slim.js')

log = options.log

if options.hdmicap and not options.fullscreen:
    print("************** WARNING: using --hdmicap without --fullscreen will give incorrect results!!!!", flush=True)


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

# to install mitmproxy certificate into Firefox and turn on/off proxy
POLICIES_CONTENT_ON = """{
  "policies": {
    "Certificates": {
      "Install": ["%(cert)s"]
    },
    "Proxy": {
      "Mode": "manual",
      "HTTPProxy": "%(host)s:%(port)d",
      "SSLProxy": "%(host)s:%(port)d",
      "Passthrough": "%(host)s",
      "Locked": true
    }
  }
}"""
POLICIES_CONTENT_OFF = """{
  "policies": {
    "Proxy": {
      "Mode": "none",
      "Locked": false
    }
  }
}"""

launch_url = "data:,"

common_options = '--pageCompleteWaitTime 10000 '

# Use the parent process initiated pagedload instead of window.location writes
common_options += '--webdriverPageload true '

# Restore the speculative connection pool that marionette disables
common_options += '--firefox.preference network.http.speculative-parallel-limit:6 '

if options.webrender:
    print("Enabling WebRender", flush=True)
    common_options += '--firefox.preference gfx.webrender.enabled:true --firefox.preference gfx.webrender.precache-shaders:true '
else:
    common_options += '--firefox.preference gfx.webrender.force-disabled:true '

if options.fullscreen:
    common_options += '--viewPort maximize '

if log:
    common_options += '--firefox.setMozLog ' + log + ' ' + '--firefox.collectMozLog '

# Gecko profiling?
if (options.profile):
    # threads: ssl, cert, js
    common_options += '--firefox.geckoProfiler true --firefox.geckoProfilerParams.interval 1  --firefox.geckoProfilerParams.features "java,js,stackwalk,leaf,ipcmessages" --firefox.geckoProfilerParams.threads "GeckoMain,Compositor,IPDL,Worker" --firefox.geckoProfilerParams.bufferSize 200000000 '

if options.debug:
    common_options += '-vvv '

if options.visualmetrics:
    common_options += '--visualMetrics true --video true --visualMetricsContentful true --visualMetricsPerceptual true '
    common_options += '--videoParams.addTimer false --videoParams.createFilmstrip false --videoParams.keepOriginalVideo false '
    if options.hdmicap:
        common_options += '--videoParams.captureCardHostOS linux --videoParams.captureCardFilename /tmp/output.mp4 '
        common_options += '--firefox.windowRecorder=false '
    else:
        #XXX Add option for   --firefox.windowRecorder false
        common_options += '--firefox.windowRecorder=true '
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
        firefox_binary_path = '/Applications/Firefox Nightly.app/Contents/MacOS/firefox'

if options.remoteAddr != None:
    # reference laptops are slow
    common_options += '--selenium.url http://' + options.remoteAddr + ' ' + '--timeouts.pageLoad 60000 --timeouts.pageCompleteCheck 60000 '

if options.wpr_host_ip != None:
    print("Adding WebPageReplay options", flush=True)
    common_options += '--firefox.preference network.dns.forceResolve:' + options.wpr_host_ip + ' --firefox.preference network.socket.forcePort:"80=4040;443=4041"' + ' --firefox.acceptInsecureCerts true '

if options.perf:
    env_perf = "PERF=1 "
else:
    env_perf = ""

# Use mitmproxy?
# XXX use mozproxy to avoid needing to download mitmproxy 5.1.1 and the dumped page load files
# Doing a './mach raptor --browsertime --test imgur' will download mitmproxy 5.1.1
# right now assumes you've used tooltool to download the relevant recordings and store them in ../site_recordings/mitm (and unzipped them there).
# https://tooltool.mozilla-releng.net/static/index.html
# you can find the right hashes to download by looking at the manifest files
if options.mitm != None:
    common_options += '--firefox.preference network.dns.forceResolve:' + options.mitm + ' --firefox.preference network.socket.forcePort:"80=8080;443=8080"' + ' --firefox.acceptInsecureCerts true '
    if not options.remoteAddr:
        # path for mitmproxy certificate, generated auto after mitmdump is started
        # on local machine it is 'HOME', however it is different on production machines
        try:
            cert_path = os.path.join(
                os.getenv("HOME"), ".mitmproxy", "mitmproxy-ca-cert.cer"
            )
        except Exception:
            cert_path = os.path.join(
                os.getenv("HOMEDRIVE"),
                os.getenv("HOMEPATH"),
                ".mitmproxy",
                "mitmproxy-ca-cert.cer",
            )
        # browser_path is the exe, we want the folder
        policies_dir = os.path.dirname(firefox_binary_path)
        # on macosx we need to remove the last folders 'MacOS'
        # and the policies json needs to go in ../Content/Resources/
        # WARNING: we must clean it up on exit!
        if sys.platform == "darwin":
            policies_dir = os.path.join(policies_dir[:-6], "Resources")
        # for all platforms the policies json goes in a 'distribution' dir
        policies_dir = os.path.join(policies_dir, "distribution")
        if not os.path.exists(policies_dir):
            os.makedirs(policies_dir)
        write_policies_json(
            policies_dir,
            policies_content=POLICIES_CONTENT_ON
            % {"cert": cert_path, "host": options.mitm, "port": 8080},
        )
    # else you must set up the proxy by hand!
    
    # start mitmproxy
    recordings = glob.glob(base + "../site_recordings/mitm/*.mp")
    if options.verbose:
        print(str(recordings) + '\n',flush=True)
    mitmdump_args = [
#        "mitmdump",
        "obj-opt/testing/mozproxy/mitmdump-5.1.1/mitmdump",
        "--listen-host", options.mitm,
        "--listen-port", "8080",
        "-v",
        "--set",  "upstream_cert=false",
        "--set",  "websocket=false",
#        "-k",
#        "--server-replay-kill-extra",
        "--script", base + "../site_recordings/mitm/alternate-server-replay.py",
        "--set",
        "server_replay_files={}".format(
            ",".join(
                [
                    normalize_path(playback_file)
                    for playback_file in recordings
                ]
            )
        ),
    ]
    print("****" + str(mitmdump_args) + '\n', flush=True)
    if options.verbose:
        mitmout = open(base + "mitm.output", 'w')
    else:
        mitmout = open("/dev/null", 'w')
    mitmpid = Popen(mitmdump_args, stdout=mitmout, stderr=mitmout).pid

def main():

    site_count = len(open(sites).readlines())
    file = open(sites, 'r')
    for site_num, line in enumerate(file):
        url = line.strip()

        print('Loading url: ' + url + ' with browsertime')

        url_arg = '--browsertime.url \"' + url + '\" '
        result_arg = '--resultDir "' + os.path.join(output_path, cleanUrl(url))

        variant_prefs_list = [""]
        if options.prefs_variant != None:
            variant_args = ""
            wordlist = options.prefs_variant.split()
            for pref in wordlist:
                variant_args += '--firefox.preference ' + pref + ' '
                if options.verbose:
                    print('Added variant "' + '--firefox.preference ' + pref + ' ' + '"', flush=True)
                    # add more variants
            variant_prefs_list = ["", variant_args]

        for variant_prefs in variant_prefs_list:
          for variant_num, variant in enumerate(variants_import.variants):
            name = variant[0]
            if variant_prefs != "":
                name += "_plus_prefs"
            script = variant[1]

            if options.desktop:
                env = 'env FIREFOX_BINARY_PATH="%s" GECKODRIVER_PATH=%s BROWSERTIME_BIN=%s LAUNCH_URL=%s' %(firefox_binary_path, geckodriver_path, browsertime_bin, launch_url)
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

                env = env_perf + 'env ANDROID_SERIAL=%s PACKAGE=%s GECKODRIVER_PATH=%s BROWSERTIME_BIN=%s LAUNCH_URL=%s' %(android_serial, package_name, geckodriver_path, browsertime_bin, launch_url)
                print('Starting ' + name + ', ' + package_name + ', from ' + apk_location + ' with arguments ' + variant_options)
                if apk_location:
                    uninstall_cmd = 'adb uninstall ' + package_name
                    print(uninstall_cmd)
                    os.system(uninstall_cmd)

                    install_cmd = 'adb install ' + apk_location
                    print(install_cmd)
                    os.system(install_cmd)

            completeCommand = env + env_perf + ' bash ' + (base+script) + ' ' + common_options  + ' ' + variant_prefs + ' ' + preload_script +  ' ' + variant_options + url_arg + os.path.join(result_arg, name) +'" '
            if options.verbose:
                print( "\ncommand " + completeCommand, flush=True)

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
   write_policies_json(
       policies_dir,
       policies_content=POLICIES_CONTENT_OFF
       % {"cert": cert_path, "host": options.mitm, "port": 8080},
   )
