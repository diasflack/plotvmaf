Matplotlib tool for visual representation of libvmaf metrics.

Based on plotbitrate https://github.com/zeroepoch/plotbitrate

Usage:

Generate log file, for example 

```
ffmpeg -i distorted.mp4 -i ref.mp4 -lavfi libvmaf="psnr=1:ssim=1:log_fmt=json:log_path=log.json" -f null -
```

Show graph

```
./plotvmaf.py log.json
```

Save video stream bitrate to an SVG file

```
./plotvmaf.py -o output.svg log.json
```