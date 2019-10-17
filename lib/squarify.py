import matplotlib.pyplot as plt

from . import functions as f


def squarify(sizes, x, y, dx, dy):
    sizes = list(map(float, sizes))

    if not len(sizes):
        return []

    if len(sizes) == 1:
        return f.layout(sizes, x, y, dx, dy)

    # figure out where 'split' should be
    i = 1
    while ((i < len(sizes)) and
           (f.worst_ratio(sizes[:i], x, y, dx, dy) >=
            f.worst_ratio(sizes[: (i + 1)], x, y, dx, dy))):
        i += 1
    current = sizes[:i]
    remaining = sizes[i:]

    leftover_x, leftover_y, leftover_dx, leftover_dy = f.leftover(current, x, y, dx, dy)
    return (
            f.layout(current, x, y, dx, dy) +
            squarify(remaining, leftover_x, leftover_y, leftover_dx, leftover_dy)
    )


def pad_rectangle(rect, level, width_over_height):
    pad = 0.01 / (level + 1)
    pad_x = pad / width_over_height
    pad_y = pad

    rect["x"] += pad_x
    rect["dx"] -= 2 * pad_x

    rect["y"] += pad_y
    rect["dy"] -= 2 * pad_y


def calc_full_layout(df, value_col, hierarchy_cols, width_over_height,
                     current_level, current_rect,
                     full_layout, full_labels, full_values):

    df_agg = df.groupby(hierarchy_cols[current_level])[value_col].sum()
    values, groups = list(df_agg.values), list(df_agg.index.values)
    values, groups = zip(*sorted(zip(values, groups), reverse=True))
    values_normed = [float(i) * current_rect['dx'] * current_rect['dy'] / sum(values) for i in values]
    rects = squarify(
        values_normed,
        current_rect['x'],
        current_rect['y'],
        current_rect['dx'],
        current_rect['dy']
    )

    for rect in rects:
        pad_rectangle(rect, current_level, width_over_height)

    if current_level == len(hierarchy_cols) - 1:
        full_layout += rects
        full_labels += groups
        full_values += values
        return None

    for i, rect in enumerate(rects):
        calc_full_layout(
            df[df[hierarchy_cols[current_level]] == groups[i]],
            value_col,
            hierarchy_cols,
            width_over_height,
            current_level + 1,
            rect,
            full_layout,
            full_labels,
            full_values
        )


def plot_treemap(df, value_col, hierarchy_cols, fig_size=(16, 9)):
    """
    :param df : pandas dataframe
    :param value_col : name of column with value
    :param hierarchy_cols : name of columns with hierarchy
    :param fig_size : size of figure
    :return: matplotlib fig, axes
    """
    fig_width, fig_height = fig_size
    init_rect = {'x': 0, 'y': 0, 'dx': 1, 'dy': 1}
    full_layout, labels, values = [], [], []
    calc_full_layout(
        df, value_col, hierarchy_cols, fig_width / fig_height,  0, init_rect,
        full_layout, labels, values
    )

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(fig_width, fig_height))

    patches = []
    for rect in full_layout:
        if rect['dx'] * rect['dy'] > 10 ** (-5):
            patches.append(
                plt.Rectangle(
                    (rect['x'], rect['y']), rect['dx'], rect['dy'],
                    fill=True, color="#58C4C6", alpha=0.5,
                    transform=ax.transAxes, figure=fig
                ),
            )

    for l, v, r in zip(labels, values, full_layout):
        x, y, dx, dy = r["x"], r["y"], r["dx"], r["dy"]
        if dx * dy > 10 ** (-5):
            ax.text(x + dx / 2, y + dy / 2, l, va="top", ha="center")
            ax.text(x + dx / 2, y + dy / 2, v, va="bottom", ha="center")

    fig.patches.extend(patches)
    ax.set_axis_off()
    return fig, ax
