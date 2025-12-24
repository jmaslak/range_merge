"""Validate that tuple lists are properly merged."""

import range_merge


def test_tuple_empty():
    """Test with an empty tuple list."""
    src = []
    result = range_merge.merge(src)
    assert result == src


def test_tuple_single():
    """Test with an single-element tuple list."""
    src = [(5, 7)]
    result = range_merge.merge(src)
    assert result == src


def test_tuple_no_merges():
    """Test a sorted list with no mergable tuples are returned properly."""
    src = [(1, 2), (4, 5), (7, 7)]
    result = range_merge.merge(src)
    assert result == src


def test_tuple_no_merges_data():
    """Test a sorted list with no mergable tuples with data are returned properly."""
    src = [(1, 2, "a"), (4, 5, "b"), (7, 7, "a")]
    result = range_merge.merge(src, use_attr=True)
    assert result == src


def test_tuple_no_merges_reorder():
    """Test a non-sorted list with no mergable tuples are returned properly."""
    src = [(1, 2), (4, 5), (7, 7)]
    src.reverse()  # Reverse the list, so it's now not properly sorted.

    expected = [(1, 2), (4, 5), (7, 7)]
    result = range_merge.merge(src)
    assert result == expected


def test_tuple_no_merges_reorder_data():
    """Test a non-sorted list with no mergable tuples with data are returned properly."""
    src = [(1, 2, "a"), (4, 5, "b"), (7, 7, "a")]
    src.reverse()  # Reverse the list, so it's now not properly sorted.

    expected = [(1, 2, "a"), (4, 5, "b"), (7, 7, "a")]
    result = range_merge.merge(src, use_attr=True)
    assert result == expected


def test_custom_object():
    """Test custom object merging/sorting."""
    src = [(2, 1), (5, 4), (7, 7)]  # End comes before start
    src.reverse  # Deliberately move out-of-order

    expected = [(2, 1), (5, 4), (7, 7)]

    def new_custom(x, y, _):
        return (y, x)

    result = range_merge.merge(src, start=lambda x: x[1], end=lambda x: x[0], new=new_custom)
    assert result == expected


def test_basic_merge():
    """Test merging without attributes."""
    src = [(5, 9), (7, 8), (8, 8), (12, 100)]
    expected = [(5, 9), (12, 100)]
    result = range_merge.merge(src)
    assert result == expected


def test_basic_merge_with_data():
    """Test merging with attributes."""
    src = [
        (5, 9, "foo"),
        (7, 8, "bar"),
        (8, 8, "foo"),
        (12, 100, "foo"),
    ]
    expected = [
        (5, 6, "foo"),
        (7, 7, "bar"),
        (8, 9, "foo"),
        (12, 100, "foo"),
    ]
    result = range_merge.merge(src, use_attr=True)
    assert result == expected


def test_basic_merge_with_data2():
    """Test merging with attributes (second version)."""
    src = [(66, 100, "a"), (60, 67, "b"), (2, 3, "c"), (4, 4, "c"), (0, 1, "e")]
    expected = [(0, 1, "e"), (2, 4, "c"), (60, 65, "b"), (66, 100, "a")]
    result = range_merge.merge(src, use_attr=True)
    assert result == expected


def test_overlaps_wrong_ordering():
    """Test for overlaps using wrong ordering."""
    src = [
        (5, 9, 1),
        (5, 6, 2),
        (7, 8, 3),
        (8, 8, 4),
        (12, 100, 5),
    ]
    expected = [
        (5, 6, 2),
        (7, 7, 3),
        (8, 8, 4),
        (9, 9, 1),
        (12, 100, 5),
    ]
    result = range_merge.merge(src, use_attr=True)
    assert result == expected


def test_complete_overlap():
    """Test a complete overlap."""
    src = [(1, 1, "a"), (1, 1, "a")]
    expected = [(1, 1, "a")]
    result = range_merge.merge(src, use_attr=True)
    assert result == expected


def test_custom_before_after_cmp():
    """Test custom before/after/cmp."""

    # This uses numbers written backwards.
    def cmp(x, y):
        a = int(str(x)[::-1])
        b = int(str(y)[::-1])
        if a < b:
            return -1
        if a == b:
            return 0
        return 1

    def before(x):
        i = int(str(x)[::-1]) - 1
        return str(i)[::-1]

    def after(x):
        i = int(str(x)[::-1]) + 1
        return str(i)[::-1]

    src = [
        ("9", "001", "a"),  # 9 - 100
        ("71", "23", "b"),  # 17 - 32
        ("33", "43", "b"),  # 33 - 34
    ]
    expected = [
        ("9", "61", "a"),  # 9-16
        ("71", "43", "b"),  # 17-34
        ("53", "001", "a"),  # 35-100
    ]

    result = range_merge.merge(src, before=before, after=after, cmp=cmp, use_attr=True)
    assert result == expected
