# browsertime_on_android_scripts
Scripts to run tests with browsertime on android

(e.g. geckoview_example, fennec, fenix)


• Clone https://github.com/mozilla/browsertime

• Download the latest `geckodriver` release: https://github.com/mozilla/geckodriver/releases

• Clone this repo, `chmod +x` the .sh scripts

• Configure `run_android.py`:

    host_ip (if using WebPageReplay)
    
    android_serial
    
    geckodriver_path (just downloaded)
    
    browsertime_bin (should point within the newly cloned browsertime repo)
    
    iterations
    
    variants (experiment name, app, driving script, firefox preferences)

• Add the sites you'd like tested to `sites.txt`

• Run with `python run_android.py`

-----------------------

## Cold Start Applink tests (w.i.p)
• Uncomment [these lines](https://github.com/acreskeyMoz/browsertime_on_android_scripts/blob/4f15056b96a9db5be5c4f6807cfcd98fc87c4c30/run_android.py#L70-L73), and also be sure to disabled visual metric and video
