import json
import re

def parseErrno(headers, output_file):
    """
    parseErrno
    
    headers - list of header files to parse for errno define's
    output_file - c file to write errnoToCString function
    """
    # pattern to match
    pattern = re.compile('\#\s*define\s+(E\w+)\s+(\d+)')
    Values = {}
    for header in headers:
        contents = open(header, 'r').readlines()

        # read all E define's
        for line in contents:
            result =  re.match(pattern, line)
            if result:
                define = result.group(1)
                value = result.group(2)
                if not value in Values:
                    Values[value] = define
                else:
                    Values[value] += ',' + define

    # write function to file
    ofile = open(output_file, 'w')
    # necessary headers
    ofile.write('#include <string.h>\n')
    ofile.write('#include <errno.h>\n\n')
    # function definition
    ofile.write('const char* errnoToCString(int value) {\n')
    ofile.write('\tswitch(value) {\n')
    # switch body
    for int_value in Values:
        error_string = Values[int_value]
        ofile.write('\t\tcase {0}: return "{1}";\n'.format(error_string.split(',')[0], error_string))
    ofile.write('\t}\n\treturn NULL;\n}\n')

if __name__ == '__main__':
    import argparse
    # get arguments
    parser = argparse.ArgumentParser(description='Create massive switch on errno values')
    parser.add_argument('--headers', nargs='*',
                        help='headers with errno definitions')
    parser.add_argument('--output_file',
                        help='output file')
    args = parser.parse_args()
    # run main function
    parseErrno(args.headers, args.output_file)


