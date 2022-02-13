def get_changes(functions, call_only=False):
    functions = sorted(functions, key=lambda item: item['commit_id'])
    f1 = None
    f2 = None
    for f in functions:
        if call_only:
            f['change_type'] = 'fcall'
            continue

        introduced = False
        param_change = False
        body_change = False
        f1 = f
        if f2 is None:
            introduced = True
        else:
            # print(f1.get('parameters'))
            if f1.get('parameters') != f2.get('parameters'):
                param_change = True
            if f1.get('body') != f2.get('body'):
                body_change = True
        f2 = f1
        if (introduced and param_change) or (introduced and body_change) or (param_change and body_change):
            f['change_type'] = 'multi'
        elif introduced:
            f['change_type'] = 'introduced'
        elif param_change:
            f['change_type'] = 'param'
        elif body_change:
            f['change_type'] = 'body'
        else:
            f['change_type'] = 'fcall'

    return functions



