import re
import sys
def parse_string(string):
    pattern = r'\$\(.*?\)'
    matches = re.findall(pattern, string)
    results = [match[2:-1] for match in matches]
    return results

string = sys.argv[1]
parsed_array = parse_string(string)
print(parsed_array)
