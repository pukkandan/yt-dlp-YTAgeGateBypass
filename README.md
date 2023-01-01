A [yt-dlp](https://github.com/yt-dlp/yt-dlp) extractor [plugin](https://github.com/yt-dlp/yt-dlp#plugins) to bypass YouTube age-gate

---

Uses [account proxy](https://youtube-proxy.zerody.one) by [zerodytrash](https://github.com/zerodytrash) to fetch video formats and [a free proxy service](https://www.4everproxy.com) for download (if required)

Pass `--extractor-args youtube:no-video-proxy` to disable the download proxy service. This may prevent certain videos from downloading

Note: The account proxy has limited resources. Please do not abuse


## Installation

Requires yt-dlp `2023.01.01` or above. For older versions, use [this gist](https://gist.github.com/pukkandan/fcf5ca1785c80f64e471f0ee14f990fb)

You can install this package with pip:
```
python3 -m pip install -U https://github.com/yt-dlp/yt-dlp-sample-plugins/archive/master.zip
```

See [yt-dlp installing plugins](https://github.com/yt-dlp/yt-dlp#installing-plugins) for the many other ways this plugin package can be installed.
