from dataclasses import dataclass
from datetime import datetime, timedelta
from range_merge import merge, merge_discrete


def test_quickstart():
    # Test the quickstart example

    # Merge / Compact ranges
    ranges = [(1, 5), (3, 8), (10, 15)]
    result = merge(ranges)
    assert result == [(1, 8), (10, 15)]

    # Merge / Compcat ranges with an attribute
    ranges = [(1, 10, "foo"), (3, 8, "bar")]
    result = merge(ranges, use_attr=True)
    assert result == [(1, 2, "foo"), (3, 8, "bar"), (9, 10, "foo")]


def test_compact_dates():
    # Compacting case-insensitive dates
    terms = [
        ("3/1/2024", "3/5/2024", "Betty"),
        ("1/6/2025", "1/7/2025", "Ash"),
        ("1/8/2025", "1/7/2026", "Ash"),
    ]
    expected = [
        ("3/1/2024", "3/5/2024", "Betty"),
        ("1/6/2025", "1/7/2026", "Ash"),
    ]

    def to_date(x):
        return datetime.strptime(x, "%m/%d/%Y")

    def to_str(x):
        return f"{x.month}/{x.day}/{x.year}"  # strftime adds leading

    def date_cmp(x, y):
        a = to_date(x)
        b = to_date(y)
        if a < b:
            return -1
        elif a == b:
            return 0
        else:
            return 1

    result = merge(
        terms,
        use_attr=True,
        before=lambda x: to_str(to_date(x) - timedelta(days=1)),
        after=lambda x: to_str(to_date(x) + timedelta(days=1)),
        cmp=date_cmp,
    )

    assert result == expected


def test_discrete():
    values = [1, 2, 3, 5, 6, 7, 10]
    result = merge_discrete(values)
    assert result == [(1, 3), (5, 7), (10, 10)]


def test_custom_class():
    @dataclass
    class ProductGroup:
        low: int
        high: int
        group: str

    products = [
        ProductGroup(low=0, high=99, group="soup"),
        ProductGroup(low=57, high=57, group="cereal"),
        ProductGroup(low=100, high=199, group="cereal"),
    ]

    result = merge(
        products,
        start=lambda p: p.low,
        end=lambda p: p.high,
        attr=lambda p: p.group,
        new=lambda s, e, attr: ProductGroup(low=s, high=e, group=attr),
    )

    expected = [
        ProductGroup(0, 56, "soup"),
        ProductGroup(57, 57, "cereal"),
        ProductGroup(58, 99, "soup"),
        ProductGroup(100, 199, "cereal"),
    ]
    assert result == expected
