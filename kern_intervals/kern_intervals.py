import numpy as np
import re
import pandas as pd


def get_octave(kern_pitch):
    if kern_pitch[0] == 'r':
        return 'r'
    octs = len(re.findall(r'^[a-gA-G]+', kern_pitch)
               [0]) - kern_pitch[0].islower()
    sign = kern_pitch[0].islower() * 2 - 1
    return octs * sign


def step_distance(p1, p2):
    d = {c: i for i, c in enumerate('abcdefg')}

    v1 = get_pitch(p1)
    v2 = get_pitch(p2)
    od1 = get_octave(p2) - get_octave(p1)
    od = od1
    iv = d[p2[0].lower()] - d[p1[0].lower()]
    chrom = v2 - v1

    step = iv % 7
    step += 7 * od
    if np.sign(step) == -np.sign(chrom):
        step = iv % (-7)
    if step % 7 == 6 and chrom == 0:
        step = iv % (-7)

    return step + 7 * round(chrom / 12 - step / 7)


def chromatic_distance(p1, p2):
    return get_pitch(p2) - get_pitch(p1)


def staff_interval(p1, p2):
    sv = {
        0: 0,
        3: 5,
        4: 7
    }
    p1_n = p1.replace('-', '').replace('#', '')
    p2_n = p2.replace('-', '').replace('#', '')
    steps = step_distance(p1_n, p2_n)
    try:
        return sv[steps % 7] + 12 * (steps // 7)
    except:
        return chromatic_distance(p1_n, p2_n)


def get_interval(p1, p2):
    iv_type = {
        0: "P",
        1: "m",
        2: "M",
        3: "m",
        4: "M",
        5: "P",
        6: np.NaN,
        7: "P",
        8: "m",
        9: "M",
        10: "m",
        11: "M"
    }
    steps = step_distance(p1, p2)
    chrom = chromatic_distance(p1, p2)
    staff = staff_interval(p1, p2)
    alter = chrom - staff

    # Correct the alteration values for a few exceptions.
    if alter < 0 and iv_type[abs(staff) % 12] == 'M' and chrom >= 0:
        alter -= np.sign(alter)
    elif alter > 0 and iv_type[abs(staff) % 12] == 'M' and chrom <= 0:
        alter -= np.sign(alter)

    # Interval direction.
    sgn = np.sign(chrom or steps)

    iv = ''
    if (alter > 0 and sgn >= 0) or (alter < 0 and sgn < 0):
        iv += 'A' * abs(alter)
    elif (alter < 0 and sgn >= 0) or (alter > 0 and sgn < 0):
        iv += 'D' * abs(alter)
    else:
        iv += iv_type[abs(chrom) % 12]

    iv += str(abs(steps) + 1)

    drs = sgn
    drs = '+' if drs >= 0 else '-'
    return drs + iv


def get_pitch(kern_pitch):
    if kern_pitch[0] == 'r':
        return 'r'
    octs = len(re.findall(r'^[a-gA-G]+', kern_pitch)
               [0]) - kern_pitch[0].islower()
    sign = kern_pitch[0].islower() * 2 - 1
    ords = {'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11}
    accs = len(re.findall(r'#+', kern_pitch)) - \
        len(re.findall(r'\-+', kern_pitch))
    pitch = 60 + ords[kern_pitch[0].lower()] + sign * 12 * octs + accs
    return pitch


# #test
# d = []
# for c1 in 'abcdefg':
#     for a1 in ' -#':
#         for c2 in 'abcdefg':
#             for a2 in ' -#':
#                 p1 = c1 + a1
#                 p2 = c2 + a2
#                 sd = step_distance(p1, p2)
#                 iv = get_interval(p1, p2)

#                 d.append([p1, p2, iv])
# df = pd.DataFrame(d)

# print(df.to_string())
# print(sorted(list(set(df[2]))))

