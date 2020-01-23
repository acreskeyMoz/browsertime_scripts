# browsertime_on_android_scripts
Scripts to run tests with browsertime on android

• Clone https://github.com/mozilla/browsertime
• Configure `run_android.py`:
    host_ip (if using WebPageReplay)
    android_serial
    geckodriver_path
    browsertime_bin
    iterations
    variants (experiment name, app, driving script, firefox preferences)

• Add the sites you'd like tested to `sites.txt`

• Run with `python run_android.py`
