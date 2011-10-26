'''
Support for Colour Palette Tables as modelled by the Generic Mapping Tools.

http://gmt.soest.hawaii.edu/gmt/html/GMT_Docs.html#x1-720004.15
'''

import math

import re

__author__ = 'rjs'

# Colour space information for GMT
# http://gmt.soest.hawaii.edu/gmt/html/GMT_Docs.html#x1-212000I

ANNOTATE_NEITHER = 0
ANNOTATE_LOWER = 1
ANNOTATE_UPPER = 2
ANNOTATE_BOTH  = 3

float_pattern = r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
byte_pattern = r'\d{1,3}'
named_color_pattern = r'\w+'

cpt_comment_regex = re.compile(r'#\s*(.)')
cpt_color_model_regex = re.compile(r'#\s*COLOU?R_MODEL = (RGB|HSV|CMYK)')

color_pattern = r'({byte})\s+({byte})\s+({byte})(\s+({byte}))?' # A 3- or 4-tuple of integers

interval_pattern = r'({float})\s+'

interval_regex = re.compile()



def load(file):
    '''
    Load a ColourPaletteTable from a CPT file.

    The format of CPT files is described at http://gmt.soest.hawaii.edu/gmt/html/GMT_Docs.html#x1-720004.15
    '''
    collecting_preamble = True
    preamble = []
    for line in file:
        stripped_line = line.strip()

        color_model_match = cpt_color_model_regex.match(stripped_line)
        if color_model_match:
            color_model = color_model_match.group(1)
            continue

        cpt_comment_match = cpt_comment_regex.match(stripped_line)
        if cpt_comment_match:
            if collecting_preamble:
                preamble.append(cpy_comment_match.group(1))


def save(file, cpt):
    '''
    Save a ColourPaletteTable to a file
    '''


def lerp(x1, y1, x2, y2, x):
    '''Linear interpolation'''
    m = (y2 - y1) / (x2 / x1)
    c = y1 - m * x1
    y = m * x + c
    return y


class Boundary(object):
    '''The boundary of an interval comprising a value and a color.'''
    def __init__(self, value, color):
        self.value = value
        self.color = color

class Interval(object):
    '''
    A coloured interval with defined by two values with corresponding colours.
    '''
    def __init__(self, lower_boundary, upper_boundary, annotate=ANNOTATE_NEITHER, label=None):
        if lower_boundary > upper_boundary:
            raise ValueError("lower_boundary must me lower than upper_boundary")
        self.lower_boundary = lower_boundary
        self.upper_boundary = upper_boundary
        self.annotate = annotate
        self.label = label

    def interpolate(self, value):
        if not (self.lower_boundary.value <= value <= upper_boundary.value):
            message = "value {0} not in range {1} to {1}".format(value,
                          self.lower_boundary.value, self.upper_boundary.value)
            raise ValueError(message)

        assert type(lower_boundary) == type(upper_boundary)

        T = type(self.lower_boundary)
        result = T(*(lerp(self.lower_boundary.value, lower_channel,
                          self.upper_boundary.value, upper_channel,
                          value)
                   for lower_channel, upper_channel in zip(self.lower_boundary.color,
                                                           self.upper_boundary.color)))
        return result

        
class ColorPaletteTable(object):
    '''A function to map from values to colours.

    The domain of the function is mapped through inclusive intervals. Intervals
    may overlap and the first interval to found to contain a value 'wins'
    '''

    def __init__(self, intervals, background_color, foreground_color, nan_color):
        '''
        Create a ColourPaletteTable from a sequence of intervals.
        '''
        self.intervals = intervals
        self.background_color = background_color
        self.foreground_color = foreground_color
        self.nan_color = nan_color
        self.description = ""

    def __len__(self):
        return len(self.intervals)

    def __call__(self, value):
        if math.isnan(value):
            return self.nan_color

        min_value = None
        max_value = None

        for interval in self.intervals:
            if interval.lower_boundary <= value <= interval.upper_boundary:
                return interval.interpolate(value)
            min_value = min(min_value, interval.lower_boundary)
            max_value = max(max_value, interval.upper_boundary)

        if value < min_value:
            return self.background_color

        assert value > max_value
        return self.foreground_color


        
  