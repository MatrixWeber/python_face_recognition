import sys

def checkIfVerbose():
    return len(sys.argv) > 1 and 'v' in sys.argv[1]