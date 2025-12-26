from ipaddress import ip_address, ip_network
from pytest import raises
from range_merge import merge_ip_ranges, merge_cidr_ranges, MismatchedIPAddressFamilies


def test_ranges_basic():
    """Do basic range tests."""
    data = [
        ("192.0.2.0", "192.0.2.255", "foo"),
        ("240.0.0.0", "255.255.255.255", "foo"),
        ("2000::", "3fff:ffff:ffff:ffff:ffff:ffff:ffff:ffff", "foo"),
    ]
    expected = [
        (ip_address("192.0.2.0"), ip_address("192.0.2.255"), "foo"),
        (ip_address("240.0.0.0"), ip_address("255.255.255.255"), "foo"),
        (ip_address("2000::"), ip_address("3fff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"), "foo"),
    ]

    assert merge_ip_ranges(data) == expected


def test_ranges_overlap():
    """Do overlapping range tests."""
    data = [
        ("0.0.0.0", "255.255.255.255", "a"),
        ("1.0.0.0", "1.255.255.255", "b"),
        ("::", "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff", "a"),
    ]
    expected = [
        (ip_address("0.0.0.0"), ip_address("0.255.255.255"), "a"),
        (ip_address("1.0.0.0"), ip_address("1.255.255.255"), "b"),
        (ip_address("2.0.0.0"), ip_address("255.255.255.255"), "a"),
        (ip_address("::"), ip_address("ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"), "a"),
    ]

    assert merge_ip_ranges(data) == expected


def test_ranges_empty():
    """Test empty ranges."""
    assert merge_ip_ranges([]) == []
    assert merge_cidr_ranges([]) == []


def test_ranges_version_mismatch():
    """Test version mismatch."""
    with raises(MismatchedIPAddressFamilies):
        merge_ip_ranges([("1.0.0.0", "ffff::")])


def test_cidr_basic():
    """Do basic CIDR merges."""
    data = [("192.0.2.0/24", "a"), ("192.0.2.0/26", "b"), ("192.0.2.64/26", "b"), ("224.0.0.0/4", "c"), ("2000::/3", "c")]
    expected = [
        (ip_network("192.0.2.0/25"), "b"),
        (ip_network("192.0.2.128/25"), "a"),
        (ip_network("224.0.0.0/4"), "c"),
        (ip_network("2000::/3"), "c"),
    ]

    assert merge_cidr_ranges(data) == expected
