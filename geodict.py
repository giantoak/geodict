#!/usr/bin/env python

# Geodict
# Copyright (C) 2010 Pete Warden <pete@petewarden.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import csv
import ujson as json
import sys

import geodict_lib
import cliargs

args = {
    'input': {
        'short': 'i',
        'type': 'optional',
        'description': 'The name of the input file to scan for locations. If none is set, will read from STDIN',
        'default': '-'
    },
    'output': {
        'short': 'o',
        'type': 'optional',
        'description': 'The name of the file to write the location data to. If none is set, will write to STDOUT',
        'default': '-'
    },
    'format': {
        'short': 'f',
        'type': 'optional',
        'description': 'The format to use to output information about any locations found. By default it will write out location names separated by newlines, but specifying "json" will give more detailed information',
        'default': 'text'
    }
}


def main():
    options = cliargs.get_options(args)

    if options['input'] is '-':
        input_handle = sys.stdin
    else:
        try:
            input_handle = open(options['input'], 'rb')
        except:
            die("Couldn't open file '{}'".format(options['input']))

    if options['output'] is '-':
        output_handle = sys.stdout
    else:
        try:
            output_handle = open(options['output'], 'wb')
        except:
            die("Couldn't write to file '{}'".format(options['output']))

    text = input_handle.read()

    # cProfile.run('locations = geodict_lib.find_locations_in_text(text)')

    locations = geodict_lib.find_locations_in_text(text)

    output_string = ''
    if options['format'].lower() == 'json':
        output_string = json.dumps(locations)
        output_handle.write(output_string)
    elif format.lower() == 'text':
        for location in locations:
            found_tokens = location['found_tokens']
            start_index = found_tokens[0]['start_index']
            end_index = found_tokens[len(found_tokens)-1]['end_index']
            output_string += text[start_index:(end_index+1)]
            output_string += "\n"
        output_handle.write(output_string)
    elif options['format'].lower() == 'csv':
        writer = csv.writer(output_handle)
        writer.writerow(['location', 'type', 'lat', 'lon'])
        for location in locations:
            found_tokens = location['found_tokens']
            start_index = found_tokens[0]['start_index']
            end_index = found_tokens[len(found_tokens)-1]['end_index']
            writer.writerow([text[start_index:(end_index+1)],
                             found_tokens[0]['type'].lower(),
                             found_tokens[0]['lat'],
                             found_tokens[0]['lon']])
    else:
        print("Unknown output format '{}'".format(format))
        exit()


if __name__ == "__main__":
    main()
