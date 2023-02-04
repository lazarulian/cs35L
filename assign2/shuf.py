# General Imports
import argparse
import random
import sys


# Class Definitions
    
class executeShuffle:
    def __init__(self, type, input):
        # Either processes a file or an input of list to create a list 
        # of the lines within the input
        if type == 'list':
            self.lines = input
            self.output_limit = len(self.lines)
        else:
            f = open(input, 'r')
            self.lines = f.readlines()
            self.output_limit = len(self.lines)
            f.close()
    
    def setOutputLimit(self, limit):
        # Allows to specify how long we want the output to be
        self.output_limit = min(limit, self.output_limit)
        
    def getRandom(self):
        return random.choice(self.lines)
        
    def getOutput(self):
        # Returns the shuffled output
        return random.sample(self.lines, self.output_limit)
    
class testInputs:
    # Class to ensure that all of the inputs are valid.
    def __init__(self, args, parser, unknown):
        self.args = args
        self.parser = parser
        self.unknown = unknown
        
    def testConflictingArgs(self):
        if self.args.echo and self.args.inputRange:
            self.parser.error("cannot combine -e and -i options\nTry 'shuf --help' for more information.")
        
    def testHeadCount(self):
        if self.args.numlines:
            try:
                numlines = int(self.args.numlines)
            except:
                self.parser.error("invalid NUMLINES: {0}". format(self.args.numlines))
            if numlines < 0:
                self.parser.error("negative count: {0}".
                            format(numlines))
                
    def testNumberInputs(self):
        if self.args.echo is False and len(self.unknown) > 1:
            self.parser.error("extra operand {0}\nTry 'shuf --help' for more information".format(self.unknown[1]))
                
    def testInputRange(self):
        if self.args.inputRange:
            # Checking for Unknown Arguments
            if len(self.unknown) != 0:
                self.parser.error("extra operand {0}\nTry 'shuf --help' for more information".format(self.unknown[0]))
            # Checking for Value Errors
            inp = self.args.inputRange.split('-')
            if len(inp) != 2:
                self.parser.error("invalid input range: {0}". format(inp[0]+"-"+inp[1]))
            elif inp[1] == '':
                self.parser.error("invalid input range: {0}". format('\'\''))                
            elif int(inp[0]) > int(inp[1]):
                self.parser.error("invalid input range: {0}". format(self.args.inputRange))                
        
        

# Main    
def main():
    
    # Setup Argument Parser
    parser = argparse.ArgumentParser(prog = 'shuf.py', description='Write a random permutation of the input lines to standard output.', epilog='Written by Apurva Shah')
    parser.add_argument('-n', '--head-count', action='store', dest='numlines', type=int)
    parser.add_argument('-i', '--input-range', action='store', dest='inputRange', type=str)
    parser.add_argument('-e', '--echo', action='store_true')
    parser.add_argument('-r', '--repeat', action="store_true")
    # parser.add_argument('input_file', nargs='?', default=sys.stdin)
    
    # Parse the Arguments
    args, unknown = parser.parse_known_args()
    
    # Testing the Inputs
    testMod = testInputs(args, parser, unknown)
    testMod.testHeadCount()  # Checking Whether Input of Numlines is Accurate
    testMod.testConflictingArgs()
    testMod.testNumberInputs()
    
    
    # Running the Arguments
        
    try:
        # Determining the Input 
        if args.inputRange:
            # Processes Input Range Argument
            testMod.testInputRange()
            inputRanges = args.inputRange.split('-')
            startRange = int(inputRanges[0])
            endRange = int(inputRanges[1])+1
            
            inp = range(startRange, endRange)
            inp = [str(i) for i in inp]
            shuffleModule = executeShuffle('list', inp)   
            
        elif len(unknown) == 0 or unknown[0] == '-':
            var = "/dev/stdin"
            shuffleModule = executeShuffle('file', var)
            
        elif args.echo:
            # Processes Echo Argument
            shuffleModule = executeShuffle('list', unknown)
        
        else:
            # Processes File Argument
            shuffleModule = executeShuffle('file', unknown[0])
                    
        #  Setting Number of Output Lines
        if args.numlines:
            shuffleModule.setOutputLimit(args.numlines)
        
        # Getting the Output
        if args.repeat:
            if args.numlines:
                for i in range(0, shuffleModule.output_limit):
                    print(shuffleModule.getRandom().rstrip())

            else:
                inf = True
                while inf:
                    print(shuffleModule.getRandom().rstrip())
                    
        else:    
            for i in shuffleModule.getOutput():
                print(i.rstrip())
    except IOError as err:
        parser.error("I/O error({0}): {1}".
                    format(err.errno, err.strerror))
    
        
        
if __name__ == "__main__":
    main()