from dataclasses import dataclass
from datetime import datetime, timedelta
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from range_merge import merge, merge_discrete, merge_ip_ranges, merge_cidr_ranges


def test_quickstart():
    # Test the quickstart example

    # Merge / Compact ranges
    ranges = [(1, 5), (3, 8), (10, 15)]
    result = merge(ranges)
    assert result == [(1, 8), (10, 15)]

    # Merge / Compact ranges with an attribute
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


def test_merge_ip_ranges():
    """Test IP range merge example."""
    src = [
        ("1.0.0.0", "1.255.240.0", "foo"),
        ("1.255.240.1", "2.0.255.255", "foo"),
        ("2000::", "2fff:ffff:ffff:ffff:ffff:ffff:ffff:ffff", "foo"),
        ("3000::", "3fff:ffff:ffff:ffff:ffff:ffff:ffff:ffff", "foo"),
    ]

    result = merge_ip_ranges(src)

    expected = [
        (IPv4Address("1.0.0.0"), IPv4Address("2.0.255.255"), "foo"),
        (IPv6Address("2000::"), IPv6Address("3fff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"), "foo"),
    ]

    assert result == expected


def test_merge_cidr_ranges():
    """Test CIDR range merge example."""
    src = [
        ("1.0.0.0/8", "foo"),
        ("1.255.240.0/24", "bar"),
        ("2000::/4", "foo"),
        ("3000::/4", "foo"),
    ]

    result = merge_cidr_ranges(src)

    expected = [
        (IPv4Network("1.0.0.0/9"), "foo"),
        (IPv4Network("1.128.0.0/10"), "foo"),
        (IPv4Network("1.192.0.0/11"), "foo"),
        (IPv4Network("1.224.0.0/12"), "foo"),
        (IPv4Network("1.240.0.0/13"), "foo"),
        (IPv4Network("1.248.0.0/14"), "foo"),
        (IPv4Network("1.252.0.0/15"), "foo"),
        (IPv4Network("1.254.0.0/16"), "foo"),
        (IPv4Network("1.255.0.0/17"), "foo"),
        (IPv4Network("1.255.128.0/18"), "foo"),
        (IPv4Network("1.255.192.0/19"), "foo"),
        (IPv4Network("1.255.224.0/20"), "foo"),
        (IPv4Network("1.255.240.0/24"), "bar"),
        (IPv4Network("1.255.241.0/24"), "foo"),
        (IPv4Network("1.255.242.0/23"), "foo"),
        (IPv4Network("1.255.244.0/22"), "foo"),
        (IPv4Network("1.255.248.0/21"), "foo"),
        (IPv6Network("2000::/3"), "foo"),
    ]

    assert result == expected
