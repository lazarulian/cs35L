# General Imports
import argparse
import random
import sys


# Class Definitions
class randline:
    def __init__(self, filename):
        f = open(filename, 'r')
        self.lines = f.readlines()
        f.close()
        
    def chooseline(self):
        return random.choice(self.lines)
    
    def getNumLines(self):
        return (len(self.lines))
    
    def shuffle(self, length):
        return random.sample(self.lines, length)
    
class testInputs:
    # Class to ensure that all of the inputs are valid.
    def __init__(self, args, parser):
        self.args = args
        self.parser = parser
        
    def testHeadCount(self):
        if self.args.numlines:
            try:
                numlines = int(self.args.numlines)
            except:
                self.parser.error("invalid NUMLINES: {0}". format(self.args.numlines))
            if numlines < 0:
                self.parser.error("negative count: {0}".
                            format(numlines))
            
    def testInputFile(self):
        try:
            generator = randline(self.args.input_file)
            for index in range(self.args.numlines):
                sys.stdout.write(generator.chooseline())
        except IOError as err:
            self.parser.error("I/O error({0}): {1}".
                        format(err.errno, err.strerror))
        
        

# Main    
def main():
    
    # Setup Argument Parser
    parser = argparse.ArgumentParser(prog = 'Shuf.py', description='Write a random permutation of the input lines to standard output.', epilog='Written by Apurva Shah')
    parser.add_argument('-v', '--version', action='store_true')
    parser.add_argument('-n', '--head-count', action='store', dest='numlines', type=int)
    parser.add_argument('-i', '--input-range')
    parser.add_argument('-e', '--echo')
    parser.add_argument('-r', '--repeat')
    parser.add_argument('input_file', nargs='?', default=sys.stdin)
    
    # Parse the Arguments
    args = parser.parse_args()
    
    # Calling Class Function
    testMod = testInputs(args, parser)
    
    
    # Running the Arguments
    if args.version:
        print("Hello to the argument world. V-Cheek.0")
        
    # Checking Whether Input of Numlines is Accurate
    testMod.testHeadCount()
        
    try:
        generator = randline(args.input_file)
        if args.numlines:
            for i in generator.shuffle(args.numlines):
                sys.stdout.write(i)
        else:
            for i in generator.shuffle(generator.getNumLines()):
                sys.stdout.write(i)
        
    except IOError as err:
        parser.error("I/O error({0}): {1}".
                    format(err.errno, err.strerror))
    
        
        
if __name__ == "__main__":
    main()