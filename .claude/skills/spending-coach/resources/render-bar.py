#!/usr/bin/env python3

import argparse

BAR_WIDTH = 60

def to_col(amount, baseline):
    """Map a dollar amount to a bar column index in [0, BAR_WIDTH]."""
    return min(round(amount / baseline * BAR_WIDTH), BAR_WIDTH)


def build_bar(actual_col, expected_col, target_col):
    """Build the bar string.

    Filled region up to actual_col, expected marker (╎), target marker (┃).
    """
    bar = ['░'] * BAR_WIDTH
    for i in range(actual_col):
        bar[i] = '█'
    if 0 <= expected_col < BAR_WIDTH:
        bar[expected_col] = '╎'
    if 0 <= target_col < BAR_WIDTH:
        bar[target_col] = '┃'
    return ''.join(bar)

def build_pointer_row(actual_col):
    """Build a pointer row with a single ▲ under the actual spend position.

    Offset by +1 to account for the leading '[' in the bar.
    """
    row = [' '] * (BAR_WIDTH + 2)
    row[actual_col + 1] = '▲'
    return ''.join(row).rstrip()


def place_text(row, col, text, align_right=False):
    """Write text into a character list at col. align_right anchors the right edge."""
    start = (col - len(text)) if align_right else col
    for i, ch in enumerate(text):
        pos = start + i
        if 0 <= pos < len(row):
            row[pos] = ch


def build_label_row(actual_col, actual, expected_col, expected, target_col, target):
    """Build a label row with dollar amounts under each pointer.

    Expected label is omitted if it would overlap the actual or target labels.
    """
    a = actual_col + 1
    e = expected_col + 1
    t = target_col + 1

    a_text = f"${actual:,.0f} actual"
    e_text = f"${expected:,.0f} expected"
    t_text = f"${target:,.0f} target"

    row = [' '] * (BAR_WIDTH + 40)
    place_text(row, a, a_text)
    place_text(row, t, t_text, align_right=True)

    # Only place expected label if it fits without stomping on actual or target
    a_end   = a + len(a_text)
    t_start = t - len(t_text)
    e_end   = e + len(e_text)
    if e > a_end + 1 and e_end < t_start - 1:
        place_text(row, e, e_text)

    return ''.join(row).rstrip()


def render(baseline, target, actual, days_in_month, today_day):
    expected  = target * today_day / days_in_month

    actual_col   = to_col(actual,   baseline)
    expected_col = to_col(expected, baseline)
    target_col   = to_col(target,   baseline)

    bar_str     = build_bar(actual_col, expected_col, target_col)
    pointer_row = build_pointer_row(actual_col)
    label_row   = build_label_row(actual_col, actual, expected_col, expected, target_col, target)

    # Anchor line: "$0" flush-left, baseline amount flush-right
    anchor_left  = "$0"
    anchor_right = f"${baseline:,.0f}"
    anchor_line  = anchor_left + ' ' * (BAR_WIDTH + 2 - len(anchor_left) - len(anchor_right)) + anchor_right

    print()
    print(f"  {anchor_line}")
    print(f"  [{bar_str}]")
    for line in (pointer_row + '\n' + label_row).split('\n'):
        print(f"  {line}")
    print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Render a spending challenge progress bar.")
    parser.add_argument('--baseline',      type=float, required=True, help="Last month's actual spend (sets bar scale)")
    parser.add_argument('--target',        type=float, required=True, help="This month's spending target")
    parser.add_argument('--actual',        type=float, required=True, help="Spend so far this month")
    parser.add_argument('--days-in-month', type=int,   required=True)
    parser.add_argument('--today-day',     type=int,   required=True, help="Today's day-of-month (1-based)")
    args = parser.parse_args()

    render(
        baseline      = args.baseline,
        target        = args.target,
        actual        = args.actual,
        days_in_month = args.days_in_month,
        today_day     = args.today_day,
    )
