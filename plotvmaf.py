#!/usr/bin/env python3

import sys
import shutil
import argparse
import subprocess
import json

# check for matplot lib
try:
    import numpy
    import matplotlib.pyplot as matplot
except ImportError:
    sys.stderr.write("Error: Missing package 'python3-matplotlib'\n")
    sys.exit(1)

import os
if not 'DISPLAY' in os.environ:
    matplot.switch_backend('Agg')

# get list of supported matplotlib formats
format_list = list(
    matplot.figure().canvas.get_supported_filetypes().keys())
matplot.close()  # destroy test figure

# parse command line arguments
parser = argparse.ArgumentParser(
    description="Graph bitrate for vmaf/psnr/ssim")
parser.add_argument('input', help="input file/stream", metavar="INPUT")

parser.add_argument('-o', '--output', help="output file")
parser.add_argument('-f', '--format', help="output file format",
    choices=format_list)

args = parser.parse_args()

# check if format given w/o output file
if args.format and not args.output:
    sys.stderr.write("Error: Output format requires output file\n")
    sys.exit(1)

vmaf_data = []
psnr_data = []
ssim_data = []
frame_count = 0

with open(args.input) as json_file:
    data = json.load(json_file)
    for frame in data['frames']:
        vmaf_data.append(frame['metrics']['vmaf'])
        psnr_data.append(frame['metrics']['psnr'])
        ssim_data.append(frame['metrics']['ssim'])

# end frame subprocess

global_peak_bitrate = 0.0
global_mean_bitrate = 0.0

# render charts in order of expected decreasing size
vmaf_array = numpy.array(vmaf_data)
psnr_array = numpy.array(psnr_data)
ssim_array = numpy.array(ssim_data)

frame_count = len(data['frames'])

x = numpy.linspace(0, frame_count, frame_count, dtype = int)

vmaf_y = vmaf_array
psnr_y = psnr_array
ssim_y = ssim_array

fig, (vmaf_ax, psnr_ax, ssim_ax) = matplot.subplots(3, 1)
fig.canvas.set_window_title(args.input)

fig_size_x_inches = 40
fig_size_y_inches = 20
fig_dpi = 100

fig.set_size_inches(fig_size_x_inches, fig_size_y_inches)

vmaf_ax.set_title("VMAF")
psnr_ax.set_title("PSNR")
ssim_ax.set_title("SSIM")

#x_tick step calculation
pixels_all = fig_size_x_inches * fig_dpi
pixel_step = 100

frame_number = pixels_all / pixel_step
x_tick = numpy.linspace(0, frame_count, frame_number, dtype = int)

vmaf_ax.set_xticks(x_tick)
psnr_ax.set_xticks(x_tick)
ssim_ax.set_xticks(x_tick)

vmaf_ax.set_ylim(ymin=60, ymax=100)
psnr_ax.set_ylim(ymin=35, ymax=60)
ssim_ax.set_ylim(ymin=0.9, ymax=1)

vmaf_ax.grid(True)
psnr_ax.grid(True)
ssim_ax.grid(True)

vmaf_ax.plot(x, vmaf_y)
psnr_ax.plot(x, psnr_y)
ssim_ax.plot(x, ssim_y)

# render graph to file (if requested) or screen
if args.output:
    matplot.savefig(args.output, format=args.format, dpi=fig_dpi)
else:
    matplot.show()                