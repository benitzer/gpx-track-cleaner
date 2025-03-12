import xml.etree.ElementTree as ET
import os
import sys

def get_gpx_files(directory):
    """
    Creates an array of all gpx files inside a given directory.
    """
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(".gpx"):
            files.append(filename)
    return files

def parse_gpx_file(gpx_file):
    # Register the custom namespace of gpx files and parse the xml structure
    ET.register_namespace('', 'http://www.topografix.com/GPX/1/1')
    gpx_data = ET.parse(gpx_file)
    return gpx_data

def clean_gpx_track(gpx_data):
    """
    Removes consecutive duplicate trackpoints based on lat, lon and ele.
    """
    # get root element
    root = gpx_data.getroot()
    
    # Find the track segment (trkseg)
    trkseg = root.find('.//{http://www.topografix.com/GPX/1/1}trkseg')
    if trkseg is None:
        return gpx_data
    
    points = trkseg.findall('{http://www.topografix.com/GPX/1/1}trkpt')
    
    previous_position = None  # (lat, lon, ele)

    for point in points[:]:  # Iterate over a copy to allow safe removal
        lat = float(point.attrib['lat'])
        lon = float(point.attrib['lon'])
        ele_element = point.find('{http://www.topografix.com/GPX/1/1}ele')
        ele = float(ele_element.text) if ele_element is not None else None
        
        current_position = (lat, lon, ele)
        
        if current_position == previous_position:
            trkseg.remove(point)
        else:
            previous_position = current_position

    return gpx_data

def keep_every_nth_trkpt(gpx_data, keep_every_nth_trkpt=1):
    """
    Keeps every nth trkpt in gpx data (keep_every_nth_trkpt has to be an int), others are deleted
    -> ensures fewer data points
    -> less noise, smaller files
    In practice, for example, a value of 5 for keep_every_nth_trkpt is well suited (or 1 for no additional deletion)
        -> delivers about one entry per second (logging in Betaflight with 200 Hz) and makes nice smooth velocity calculation possible
    keep_every_nth_trkpt = 1 leads to no change (all entries are retained)
    """
    if keep_every_nth_trkpt == 0 or keep_every_nth_trkpt == 1: # 0 is not allowed because of modulo operation, 1 does not change anything
        return gpx_data

    # get root element
    root = gpx_data.getroot()
    
    # Find the track segment (trkseg)
    trkseg = root.find('.//{http://www.topografix.com/GPX/1/1}trkseg')
    if trkseg is None:
        return gpx_data
    
    points = trkseg.findall('{http://www.topografix.com/GPX/1/1}trkpt')
    
    entry_counter = 0

    for point in points[:]:  # Iterate over a copy to allow safe removal
        if entry_counter % keep_every_nth_trkpt != 0:
            trkseg.remove(point)
        entry_counter += 1

    return gpx_data

def write_gpx_file(gpx_data, file_path):
    """
    Saves the gpx data to the given file location.
    """
    gpx_data.write(file_path, xml_declaration=True, encoding='utf-8', method="xml")


def main(directory):
    """
    Processes all GPX files in a directory, removing consecutive duplicate trackpoints based on lat, lon and ele.
    """
    # Check if passed argument is existing directory
    if not os.path.isdir(directory):
        print("Can't find directory ", directory)
        sys.exit(0)

    # Get all gpx files inside the given directory
    gpx_files = get_gpx_files(directory)
    print("Found {} gpx files in directory {}".format(len(gpx_files), directory))

    # Check if output directory exists and create new output dir if not
    output_dir = os.path.join(directory, "output")
    if len(gpx_files) > 0 and not os.path.isdir(output_dir):
        try:
            os.mkdir(output_dir)
        except:
            print("Failed to create output directory")
            sys.exit(1)

    # For each gpx file: clean track points and save new gpx to output dir
    for filename in gpx_files:
        gpx_file = os.path.join(directory, filename)

        gpx_data = parse_gpx_file(gpx_file)

        # clean gpx data (consecutive duplicate entries based on lat, lon and ele are removed)
        cleaned_gpx_data = clean_gpx_track(gpx_data)
        # retain only every keep_every_nth_trkpt trkpt
        cleaned_gpx_data = keep_every_nth_trkpt(cleaned_gpx_data, keep_every_nth_trkpt=5)

        extensive_procecure = True  # if True, execution needs more time, but it can help in some rare cases
        if extensive_procecure:
            # clean gpx data again, to ensure that no new consecutive duplicate entries were created by the deletion in the step before
            cleaned_gpx_data = clean_gpx_track(cleaned_gpx_data)

        # edit file names so that the cleaned file is called differently than the original
        name, extension = filename.rsplit(".gpx", 1)  # Split at the last ".gpx"
        filename_cleaned = f"{name}.cleaned.gpx"

        write_gpx_file(cleaned_gpx_data, os.path.join(output_dir, filename_cleaned))


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Too many arguments! Pass only one directory of gpx files!")
        sys.exit(1)
    if len(sys.argv) < 2:
        print("No argument found! Pass path of directory of gpx files as argument.")
        sys.exit(1)
    main(sys.argv[1])