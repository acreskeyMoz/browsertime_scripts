# browsertime_on_android_scripts
Scripts to run tests with browsertime on android

(e.g. geckoview_example, fennec, fenix)


• Clone https://github.com/mozilla/browsertime

• Download the latest `geckodriver` release: https://github.com/mozilla/geckodriver/releases

• Clone this repo, `chmod +x` the .sh scripts

• Configure `run_android.py`:

    geckodriver_path (just downloaded)
    
    browsertime_bin (should point within the newly cloned browsertime repo)
  
    variants (experiment name, app, driving script, firefox preferences)

• Add the sites you'd like tested to `sites.txt`

• Run with `python run_android.py --serial {device serial}`

• Additional options:

    -h, --help            show this help message and exit
    --debug               pass debugging flags to browsertime (-vvv)
    -i ITERATIONS, --iterations ITERATIONS
                        Number of iterations
    -s SITES, --sites SITES
                        File of sites
    --serial SERIAL       Android serial #
    --webrender           Enable webrender (default: disabled)
    --profile             Enable gecko profiling
    --visualmetrics       Calculate visualmetrics (SI/CSI/PSI)
