#!/usr/bin/env python3

import sys
import json
import argparse
from view_spot_finder import ViewSpotFinder

def main():
    parser = argparse.ArgumentParser(description="Find the highest view spots in a given mesh.")
    parser.add_argument("file_path", help="The path to the JSON file containing the mesh")
    parser.add_argument("nr_view_spots", help="Number of view spots", type=int)
    args = parser.parse_args()

    try:
        with open(args.file_path) as f:
            data = json.load(f)
            finder = ViewSpotFinder(data, args.nr_view_spots)
            print(json.dumps(finder.get_local_maxima()))
    except FileNotFoundError:
        err_out("File %s does not exist." % args.file_path)
    except json.decoder.JSONDecodeError:
        err_out("Invalid JSON in file %s." % args.file_path)

def err_out(message):
    print("error: %s" % message, file=sys.stderr)

if __name__ == "__main__":
    main()
