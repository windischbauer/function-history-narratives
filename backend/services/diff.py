import difflib
import json

from services import snapshot as _snapshot


def get_diff(crs_a, crs_b, filename, func_name):
    a = _snapshot.read_by_commit_and_file_and_fname(crs_a, filename, func_name)
    b = _snapshot.read_by_commit_and_file_and_fname(crs_b, filename, func_name)

    fname = ''
    if 'filename' not in b:
        if 'filename' not in a:
            return 'Something went horribly wrong'

    fname = b['filename']

    a_c = ''
    if 'content' in a:
        a_c = a['content'].splitlines(keepends=False)[a['lineno'] - 1:a['end_lineno']]

    b_c = ''
    if 'content' in b:
        b_c = b['content'].splitlines(keepends=False)[b['lineno'] - 1:b['end_lineno']]

    diff_result = difflib.unified_diff(a_c, b_c, fromfile=fname, tofile=fname, lineterm='', n=100)
    result_string = '\n'.join(diff_result)
    # result_string = json.dumps(result_string)

    # print(result_string)
    return {'diff': result_string}
