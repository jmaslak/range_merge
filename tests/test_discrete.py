"""Validate that discrete lists are properly merged."""

import range_merge


def test_empty():
    """Test an empty range."""
    src = []
    result = range_merge.merge_discrete(src)
    assert result == src


def test_single():
    """Test an single-element range."""
    src = [1]
    expected = [(1, 1)]
    result = range_merge.merge_discrete(src)
    assert result == expected


def test_overlaps():
    """Test a range where elements are overlapping."""
    src = [1, 3, 2, 1]
    expected = [(1, 3)]
    result = range_merge.merge_discrete(src)
    assert result == expected


def test_full_overlap():
    """Test a range where two elements completely overlap."""
    src = [1, 1]
    expected = [(1, 1)]
    result = range_merge.merge_discrete(src)
    assert result == expected


def test_no_merge():
    """Test a range where elements not mergeable."""
    src = [1, 3, -2, -11]
    expected = [(-11, -11), (-2, -2), (1, 1), (3, 3)]
    result = range_merge.merge_discrete(src)
    assert result == expected
