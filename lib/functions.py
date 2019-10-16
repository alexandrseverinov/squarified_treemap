def _layout_row(sizes, x, y, dy):
    covered_area = sum(sizes)
    width = covered_area / dy
    rects = []
    for size in sizes:
        rects.append({"x": x, "y": y, "dx": width, "dy": size / width})
        y += size / width
    return rects


def _layout_col(sizes, x, y, dx):
    covered_area = sum(sizes)
    height = covered_area / dx
    rects = []
    for size in sizes:
        rects.append({"x": x, "y": y, "dx": size / height, "dy": height})
        x += size / height
    return rects


def layout(sizes, x, y, dx, dy):
    if dx >= dy:
        return _layout_row(sizes, x, y, dy)
    return _layout_col(sizes, x, y, dx)


def _leftover_row(sizes, x, y, dx, dy):
    # compute remaining area when dx >= dy
    covered_area = sum(sizes)
    width = covered_area / dy
    leftover_x, leftover_y = x + width, y
    leftover_dx, leftover_dy = dx - width, dy
    return leftover_x, leftover_y, leftover_dx, leftover_dy


def _leftover_col(sizes, x, y, dx, dy):
    # compute remaining area when dx >= dy
    covered_area = sum(sizes)
    height = covered_area / dx
    leftover_x, leftover_y = x, y + height
    leftover_dx, leftover_dy = dx, dy - height
    return leftover_x, leftover_y, leftover_dx, leftover_dy


def leftover(sizes, x, y, dx, dy):
    if dx >= dy:
        return _leftover_row(sizes, x, y, dx, dy)
    return _leftover_col(sizes, x, y, dx, dy)


def worst_ratio(sizes, x, y, dx, dy):
    return max(
        [
            max(rect["dx"] / rect["dy"], rect["dy"] / rect["dx"])
            for rect in layout(sizes, x, y, dx, dy)
        ]
    )


def normalize_sizes(sizes, dx, dy):
    total_size = sum(sizes)
    total_area = dx * dy
    sizes = map(float, sizes)
    sizes = map(lambda size: size * total_area / total_size, sizes)
    return list(sizes)
