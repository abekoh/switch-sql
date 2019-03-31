import sys


def parse_sql(lines):
    parsed = []
    for line in lines:
        # line = line.replace('\n', '').replace('\t', '')
        s_lines = line.split(' ')
        for s_line in s_lines:
            # if s_line != '':
            parsed.append(s_line)
    return parsed


def judge_expanded(parsed):
    # not-expanded: 0, expanded: 1, error: -1
    sum_sharp = 0
    before = ''
    has_01 = False
    for current in parsed:
        if '01.' in current:
            has_01 = True
        if has_01 and 'union' in before and 'all' in current:
            return 1
        if '##.' in current:
            sum_sharp += 1
        before = current
    if sum_sharp == 1:
        return 0
    return -1


def expand(parsed, num):
    depth = 0
    before = ''
    start_i, end_i = -1, -1
    for i, current in enumerate(parsed):
        if '(' in current:
            depth += 1
        if ')' in current:
            depth -= 1
        if depth == 1 and '(' in before:
            start_i = i
        if depth == 0 and ')' in current:
            end_i = i - 1
        before = current
    if start_i == -1 or end_i == -1:
        sys.exit(1)
    new_parsed = []
    for i in range(start_i):
        new_parsed.append(parsed[i])
    for i in range(1, num + 1):
        pad_i = '{:0>2}'.format(i)
        for j in range(start_i, end_i + 1):
            new_parsed.append(parsed[j].replace('##', pad_i))
        if i != num:
            new_parsed.extend(['union', 'all\n'])
    for i in range(end_i + 1, len(parsed)):
        new_parsed.append(parsed[i])
    return new_parsed


def unexpand(parsed):
    depth = 0
    before = ''
    start_i, end_i = -1, -1
    for i, current in enumerate(parsed):
        if '(' in current:
            depth += 1
        if ')' in current:
            depth -= 1
        if depth == 1 and 'union' in before and 'all' in current:
            j = i - 1
            while (j > 1):
                if parsed[j - 1] != '':
                    break
                j -= 1
            start_i = j
        if depth == 0 and ')' in current:
            end_i = i - 1
        before = current
    if start_i == -1 or end_i == -1:
        print('Error: cannot unexpand.')
        sys.exit(1)
    new_parsed = []
    for i in range(start_i):
        new_parsed.append(parsed[i].replace('01.', '##.'))
    for i in range(end_i + 1, len(parsed)):
        new_parsed.append(parsed[i])
    return new_parsed


def unparse_sql(parsed):
    return ' '.join(parsed)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('length of args must be 2.')

    src_path = sys.argv[1]
    num = int(sys.argv[2])

    with open(src_path, 'r') as f:
        lines = f.readlines()

    parsed = parse_sql(lines)
    judged = judge_expanded(parsed)
    if judged == -1:
        print('Error: context is not matched expanded/notexpanded.')
        sys.exit(1)
    elif judged == 0:
        new_parsed = expand(parsed, num)
    elif judged == 1:
        new_parsed = unexpand(parsed)
    new_sql = unparse_sql(new_parsed)
    print(new_sql)

