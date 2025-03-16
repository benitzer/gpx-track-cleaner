# GPX Track Cleaner

A Python script for cleaning GPX tracks. It removes consecutive duplicate track points (based on latitude, longitude, and elevation) and allows retaining only every nth track point. Especially useful for processing GPS data from FPV drones with Betaflight.

## Purpose
This script efficiently reduces and cleans GPX data for better analysis and visualization in software like GeoTracker, OsmAnd, or Google Earth Pro.

### Use Cases
- Post-flight analysis and visualization of FPV drone flights.
- Improving data quality from Betaflight logs by removing redundant entries.
- Preventing issues with flight visualization (e.g., incorrect speed calculations, display errors on maps).

## Generating GPX Files from Betaflight

If you are using an FPV drone with Betaflight and GPS logging enabled, you can generate GPX files using the following steps:

1. **Enable GPS Logging** in Betaflight: Ensure that Blackbox logging is activated and GPS data is being recorded.
2. **Carry out your drone flight**.
3. **Download Blackbox Logs**: Retrieve the `.bbl` log files from your flight controller.
4. **Convert to GPX**:
   - Open the logs in **Betaflight Blackbox Explorer**.
   - Use the **Export to GPX** function to generate the GPX files.

These GPX files can now be processed with this script to remove redundant data and optimize them for further analysis.

## Installation & Requirements
### Requirements
- **Python** must be installed.
- The script **gpx-cleaner.py** must be downloaded.

## Usage
### Running the Script
Use the following command in the terminal:
```sh
python3 gpx-cleaner.py <keep_every_nth_trkpt> <path-to-directory-with-gpx-files>
```
Replace `<keep_every_nth_trkpt>` with an integer specifying how many track points to retain (e.g., `1` to keep all, `5` to keep every 5th point). Replace `<path-to-directory-with-gpx-files>` with the directory containing your GPX files.

### Example
If your GPX files are in `/home/user/gpx_data` and you want to keep every 5th track point, run:
```sh
python3 gpx-cleaner.py 5 /home/user/gpx_data
```
The cleaned files will be stored in `/home/user/gpx_data/output/`.

### Output
- Cleaned GPX files are saved in a subfolder `/output` within the specified directory.
- Duplicate entries are removed, and depending on the setting, only every nth track point is retained.

### Elevation Adjustment
In addition to filtering track points, the script includes an `elevation_increase` parameter that allows increasing the elevation of all track points by a fixed number of meters. This is particularly useful for better visualization in Google Earth Pro, where terrain data can sometimes cause track points to be hidden beneath the ground. By increasing the elevation (e.g., by 20 meters), these points remain visible.

The `elevation_increase` parameter is hardcoded within the script and is not passed via the command line. By default, it is set to `0` meters, meaning no elevation adjustment is applied. If you need to modify it, open `gpx-cleaner.py` and adjust the value manually.

## Forked From

This project is a fork of [gpx-track-cleaner by codeOfJannik](https://github.com/codeOfJannik/gpx-track-cleaner). Thanks to the original author for their work!

## License
This script is open-source and released under the MIT license. Feel free to use and modify it!