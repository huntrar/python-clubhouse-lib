# This is the counterpart to the API slurper. It takes the description files that were generated and builds Python code to pop into the client object

import os
import json
from typing import List

from api_slurper import Documentation, DocParameter

class APIFunc:
    """Represents a clubhouse API function, sorted by category, title"""
    def __init__(self, data: Documentation):
        self.data: Documentation = data
    def __lt__(self, other):
        if self.data['category'] != other.data['category']:
            return self.data['category'] < other.data['category']
        return self.data['title'] < other.data['title']


if __name__ == "__main__":
    funcs:List[APIFunc] = []

    for fname in os.listdir('api_def'):
        if fname.endswith(".json"):
            with open('api_def/'+fname, 'r') as f:
                funcs.append(APIFunc(json.load(f)))

    funcs.sort()

    prev_category = ''

    for api_func in funcs:
        func: Documentation = api_func.data
        # Separate query params from body params
        url_params:List[DocParameter] = []
        body_params:List[DocParameter] = []
        for param in func['params']:
            if param['body_param']:
                body_params.append(param)
            else:
                url_params.append(param)
        
        # Whether or not the dict should be explicitly built
        build_dict = True
        # Build the Python parameter list and documentation parameter list
        py_parameter_list:List[str] = []
        doc_parameter_list:List[str] = []
        for p in func['params']:
            np = ''
            if not p['required']:
                np = ' = Omit'
            new_name = p['name']
            if new_name.find('-') != -1:
                new_name = new_name.replace('-', '_')
                build_dict = True
            if not p['body_param']:
                build_dict = True
            py_parameter_list.append('{}: {}{}'.format(new_name, p['type'], np))
            doc_parameter_list.append('param {}: {}'.format(new_name, p['desc']))

        # Convert the parameter list into properly spaced and tabbed parameters
        py_parameters = ''
        if len(py_parameter_list) > 0:
            if len(py_parameter_list) <= 3 and not True in [p.endswith(' = Omit') for p in py_parameter_list]:
                # For short function parameter lists where none of the parameters are optional, don't get fancy with newlines
                py_parameters = ', {}'.format(', '.join(py_parameter_list))
            else:
                last = len(py_parameter_list) - 1
                py_parameters = ',\n'
                for i in range(last + 1):
                    p = py_parameter_list[i]
                    py_parameters += p
                    if i != last:
                        py_parameters += ','
                    if p.endswith(' = Omit'):
                        py_parameters += ' # type: ignore'
                    if i != last:
                        # The final newline needs a different tab level
                        py_parameters += '\n'
                # Replace newlines with tabbed newlines
                py_parameters = py_parameters.replace('\n', '\n        ')
                # For the final paren, since it needs different tab depth
                py_parameters += '\n    '
        
        # Generate the docstr
        docstr = ''
        has_desc = func['description'] != None and len(func['description']) > 0 
        has_args = len(py_parameter_list) > 0
        if has_desc or has_args:
            if has_desc:
                docstr += '\n'.join(func['description'])
            if has_args:
                if has_desc:
                    docstr += '\n\n'
                docstr += '\n'.join(doc_parameter_list)
            if docstr.find('\n') == -1: # Single line docstrings should be all on one line
                docstr = '"""{}"""\n'.format(docstr)
            else:
                docstr = '"""\n{}\n"""\n'.format(docstr)
            
        # Replace newlines with tabbed newlines
        docstr = docstr.replace('\n', '\n        ')

        # Build the string used to fetch/update data from Clubhouse
        request_string = 'self.{}("{}"'.format(func['http_verb'], func['url_path'])
        if len(url_params) > 0:
            request_string += '.format(' + ','.join([f['name'] + '=' + f['name'] for f in url_params]) + ')'
        if len(body_params) > 0:
            if not build_dict:
                request_string += ', PrepareLocals(locals())'
            else:
                request_string += ', PrepareLocals({'
                if len(func['params']) == 0:
                    request_string += '})'
                else:
                    request_string += '\n            '
                    request_string += ',\n            '.join([
                        "'{}': {}".format(p['name'], p['name'].replace('-', '_')) 
                        for p in body_params
                    ])
                    request_string += '\n        })'

        request_string += ')'

        return_str = ''
        result_str = ''
        if func['response'] != 'void':
            result_str = ' -> ' + func['response']
            # Only convert the result and return if there's something to return
            return_str = 'return '
            request_string += '.json()'

        
        # Generate the function and throw it on stdout
        result = """
    def {title}(self{py_params}){result}:
        {description}{return_str}{request_string}
        """.format(
            title=func['identifier'], 
            py_params=py_parameters,
            result=result_str,
            description=docstr,
            request_string=request_string,
            return_str=return_str
        )
        # If we've encountered a new category, print it with a # border
        if func['category'] != prev_category:
            prev_category = func['category']
            length = len(prev_category) + 4
            fence = '#' * length
            print('\n{fence}\n# {category} #\n{fence}'.replace('\n', '\n    ').format(category=prev_category, fence=fence))
        print(result)