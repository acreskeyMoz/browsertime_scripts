# browsertime_scripts

Scripts to run local performance tests with browsertime.

Supports Firefox and Chrome desktop and android apps (e.g. geckoview_example, fenix).

## Usage ##

• Clone the browsertime repo, https://github.com/sitespeedio/browsertime
        • run `npm install`

• Download the latest `geckodriver` release: https://github.com/mozilla/geckodriver/releases

• Clone this repo, and  `chmod +x` the `.sh` scripts

• Configure `run_test.py` to point to your browsertime and geckodriver paths (or specify them with `--browsertime` and `--geckodriver` )

        • browsertime_bin (point to bin/browsertime.js within the newly cloned browsertime repo)
        • geckodriver_path (point to the geckodriver binary you just downloaded)

• If you're running on android, configure `android_serial` within `run_test.py`

• Configure the browser variants you'd like to compare. These can be seperate binaries or else preferences.

  See `variants_android.py` or `variants_desktop.py` for examples.

  For instance, to compare fenix without and with HTTP/3 enabled, you may do something like this:

        variants = [('fenix', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly_location, ''),
                    ('fenix_h3', 'fenix.sh', 'org.mozilla.fenix', fenix_nightly_location, ' --firefox.preference network.http.http3.enabled:true' )]
        This will include specifying paths the binaries you which to test.
  
• Configure the sites you'd like tested in `sites.txt` or create a new sites text file and specify `--sites my_sites.txt`

• Run with `python run_test.py`

• Additional options:

          -h, --help            show this help message and exit
          --debug               pass debugging flags to browsertime (-vvv)
          -i ITERATIONS, -n ITERATIONS, --iterations ITERATIONS
                                Number of iterations
          -s SITES, --sites SITES
                                File of sites
          --serial SERIAL       Android serial #
          --desktop             Desktop or mobile
          --binarypath BINARYPATH
                                path to firefox binary (desktop)
          --webrender           Enable webrender (default: disabled)
          --fullscreen          Run test in full-screen (Desktop)
          --profile             Enable profiling
          --visualmetrics       Calculate visualmetrics (SI/CSI/PSI)
          --wpr_host_ip WPR_HOST_IP
                                WebPageReplay host IP (optional)
          --reload              test reload of the URL
          --condition           load a site before the target URL
          --prefs PREFS         Firefox preferences to use for all runs
          --variants VARIANTS   python module with the variants defined, e.g.
                                variants_android
          --geckodriver GECKODRIVER
                                path to geckodriver
          --browsertime BROWSERTIME
                                path to browsertime/bin/browsertime.js
          --output_path OUTPUT_PATH
                                Path for the browsertime json (defaults to
                                'browsertime-results')
          --restart_adb         Restart adb between variants (workaround to adb file
                                descriptor leak)

## Examples ##

• Run on Desktop, with variants defined in a new file, `variants_fission.py`

    python run_test.py --desktop --variants variants_fission
• Run on android, load each site 10 times, and add the given additional prefs for each run

    python run_test.py -n 10 --sites sites_1.txt --serial 89PX0DD5W --prefs "nglayout.debug.paint_flashing:true network.http.speculative-parallel-limit:7"
    
• Run on Desktop, specifying the binary path

    python run_test.py --desktop --binarypath "/Applications/Firefox Nightly.app/Contents/MacOS/firefox"
