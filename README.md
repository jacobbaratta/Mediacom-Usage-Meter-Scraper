# Mediacom Usage Meter Scraper
>Because it's too much damn work to log into Mediacom's crappy website every time I want to check my bandwidth usage status.

This simple Python script uses Selenium with a headless instance of Chrome (via chromedriver) to log into the Mediacom bandwidth usage site, scrape some data about your current monthly bandwidth usage, and display it to you in the console output.

![](screenshot.png)

## Installation

Download or clone the repo into a folder. Download a copy of the latest version of [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads), place it in the project folder, and make sure the binary is named `chromedriver`. Edit `config.example.json` with your Mediacom username & password, then rename the file to `config.json`. Check to make sure that you have all the dependencies (you may need to install selenium via pip). If you are not running on OSX, edit `chrome_options.binary_location` in `scrape.py` to correctly reflect the path to your Chrome binary.

## Usage

```sh
python3 scrape.py
```


## Release History

* 1.0
    * First public release

## Meta

Written by Jacob Baratta.

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/jacobbaratta](https://github.com/jacobbaratta)
