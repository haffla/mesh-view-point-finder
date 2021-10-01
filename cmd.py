import sys
import json
from view_spot_finder import ViewSpotFinder

def main():
    argv = sys.argv

    if len(argv) < 3:
        return err_out("Wrong number of arguments.\nUsage: python %s [filepath] [number of view points]" % argv[0])

    file = argv[1]
    n_maxima = argv[2]

    try:
        n_maxima = int(n_maxima)
    except ValueError:
        return err_out("Second argument is not a number")

    try:
        with open(file) as f:
            data = json.load(f)
            finder = ViewSpotFinder(data, n_maxima)
            print(json.dumps(finder.get_local_maxima()))
    except FileNotFoundError:
        err_out("File %s does not exist." % file)
    except json.decoder.JSONDecodeError:
        err_out("Invalid JSON in file %s." % file)

def err_out(message):
    print("Error: %s" % message, file=sys.stderr)

if __name__ == "__main__":
    main()
