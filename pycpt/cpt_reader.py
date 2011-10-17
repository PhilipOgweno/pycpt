import re
from pycpt.ast import CommentNode

comment_pattern = r'^\s*\#\s*(.*)'
color_model_pattern = r'^\s*\#\s*COLOR_MODEL\s*=\s*(\+?)\s*(HSV|RGB|CMYK)'
int_pattern = r'\d+'
float_pattern = r'([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)'
hex_rgb_pattern = r'\#([0-9A-Fa-f]{6})\b'
label_pattern = r';\s*(?P<label>.+)'
triple_pattern = r'{float}\s+{float}\s+{float}'.format(float=float_pattern)
cmyk_pattern = r'{float}\s+{float}\s+{float}\s+{float}'.format(float=float_pattern)
gray_pattern = float_pattern
name_pattern = r'[A-Za-z]\w+'
annotation_pattern = r'(?P<annotation>[ULB])'

substitutions = { 'float' : float_pattern,
                  'triple' : triple_pattern,
                  'cmyk' : cmyk_pattern,
                  'gray' : gray_pattern,
                  'name' : name_pattern,
                  'label' : label_pattern,
                  'hexrgb' : hex_rgb_pattern,
                  'annotation' : annotation_pattern }

comment_regex = re.compile(comment_pattern)

# The following combinations are ambiguous and are not accepted
# r'\s*{float}\s+{gray}\s+{float}\s+{triple}' - 6 floats
# r'\s*{float}\s+{triple}\s+{float}\s+{gray}' - 6 floats
# r'\s*{float}\s+{gray}\s+{float}\s+{cmyk}'   - 7 floats
# r'\s*{float}\s+{cmyk}\s+{float}\s+{gray}'   - 7 floats
# r'\s*{float}\s+{triple}\s+{float}\s+{cmyk}' - 9 floats
# r'\s*{float}\s+{cmyk}\s+{float}\s+{triple}' - 9 floats

interval_formats = [ ('triple', 'triple'),
                     ('triple', 'hexrgb'),
                     ('triple', 'float'),
                     ('cmyk',   'cmyk'),
                     ('cmyk',   'hexrgb'),
                     ('cmyk',   'name'),
                     ('gray',   'gray'),
                     ('gray',   'hexrgb'),
                     ('gray',   'name'),
                     ('hexrgb', 'hexrgb'),
                     ('hexrgb', 'cmyk'),
                     ('hexrgb', 'name'),
                     ('hexrgb', 'gray'),
                     ('name',   'name'),
                     ('name',   'hexrgb'),
                     ('name',   'triple'),
                     ('name',   'cmyk'),
                     ('name',   'gray') ]

value1_pattern = r'(P?<value1>{float})'.format(float=float_pattern)
value2_pattern = r'(P?<value2>{float})'.format(float=float_pattern)


interval_patterns = []
for type1, type2 in interval_formats:
    color1_pattern = r'(P?<color1>{type1})'.format(type1=substitutions[type1])
    color2_pattern = r'(P?<color2>{type2})'.format(type2=substitutions[type2])
    interval_pattern = r'\s*{value1}\s+{color1}\s+{value2}\s+{color2}(\s+{annotation})?(\s+{label})?'.format(
                            value1=value1_pattern,
                            value2=value2_pattern,
                            color1=color1_pattern,
                            color2=color2_pattern,
                            annotation=annotation_pattern,
                            label=label_pattern)
    interval_patterns.append(interval_patterns)


# TODO: Make appropriate substitutions and compile to regexes

augmented_interval_patterns = (pattern + r'(\s+{annotation})?(\s+{label})?'.format(*substitutions) for pattern, groups in interval_patterns)

interval_regexes = [re.compile(pattern) for pattern in augmented_interval_patterns]



def read_cpt(f):
    statements = []
    color_model = 'RGB'
    interpolation_model = 'RGB'
    for line in f:

        # Put each section below into a function which returns True if
        # successfull, otherwise False and loop over them in order for each
        # line
        

        # Match COLOR_MODEL directives
        color_model_match = color_model_regex.match(line)
        if color_model_match:
            color_model = color_model_match.group(2)
            if color_model_match.group(1) == '+':
                interpolation_model = color_model


        # Match other comments
        comment_match = comment_regex.match(line)
        if comment_match:
            comment = CommentNode(comment_match.group(1))
            statements.append(comment)


        # Match interval specifications
        for interval_regex, create_interval in interval_patterns:
            interval_match = interval_regex.match(line)
            if interval_match:
                interval_spec = create_interval(interval_match)
                statements.append(interval_spec)







        




  