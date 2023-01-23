from unittest import mock
import pytest
from briq_api.indexer.events.common import encode_int_as_bytes

from briq_api.indexer.events.set import send_to_set_indexer

class FakePost:
    def __init__(self, a, json):
        # somewhat arbitrary OK number
        assert len(json['transaction_data']) > 10

    def raise_for_status(self):
        pass

@mock.patch('briq_api.indexer.events.set.requests.post')
def test_send_to_set_indexer(mock: mock.MagicMock, tx_data):
    mock.side_effect = lambda a, json, timeout: FakePost(a, json)
    send_to_set_indexer(b'0xcafe', tx_data)
    assert mock.call_count == 2


@pytest.fixture(scope="module")
def tx_data() -> list[bytes]:
    return [encode_int_as_bytes(x) for x in [
        0x3,
        0x6f18ebcc76b6bd3560da141aeae53f9af3d80c2001415c963ecddbba4e8ba12,
        0x25b09dda48c8b20c9ca39a74e140308e9266619a02f3f41415e45eb4fbc44df,
        0x0,
        0x3,
        0x5f9e1c4975b0f71f0b1af2b837166d321af1cdba5c30c09b0d4822b493f1347,
        0x2f2e26c65fb52f0e637c698caccdefaa2a146b9ec39f18899efe271f0ed83d3,
        0x3,
        0xc9,
        0x5f9e1c4975b0f71f0b1af2b837166d321af1cdba5c30c09b0d4822b493f1347,
        0x2f2e26c65fb52f0e637c698caccdefaa2a146b9ec39f18899efe271f0ed83d3,
        0xcc,
        0xec,
        0x1b8,
        0x22030445da671e4f5bdab7802a061ca0c55754d9703c5390266fd8b814de880,
        0x1,
        0x6017,
        0x22030445da671e4f5bdab7802a061ca0c55754d9703c5390266fd8b814de880,
        0x5a6f6d6269654475636b2e6a736f6e,
        0x1,
        0x5a6f6d6269654475636b,
        0x3,
        0x4d652077616e74206272616969696e,
        0x73202d2064757575636b2062726169,
        0x69696e73,
        0x1,
        0x1,
        0x5d,
        0x0,
        0x5d,
        0x233931386637340000000000000000000000000000000001,
        0x7ffffffffffffffc80000000000000048000000000000000,
        0x233862346635390000000000000000000000000000000001,
        0x7ffffffffffffffc80000000000000058000000000000000,
        0x233934393437390000000000000000000000000000000001,
        0x7ffffffffffffffc80000000000000068000000000000000,
        0x233934393437390000000000000000000000000000000001,
        0x7ffffffffffffffd80000000000000038000000000000000,
        0x233862346635390000000000000000000000000000000001,
        0x7ffffffffffffffd80000000000000048000000000000000,
        0x233934393437390000000000000000000000000000000001,
        0x7ffffffffffffffd80000000000000058000000000000000,
        0x233931386637340000000000000000000000000000000001,
        0x7ffffffffffffffd80000000000000068000000000000000,
        0x236234396439300000000000000000000000000000000001,
        0x7ffffffffffffffd80000000000000078000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x7ffffffffffffffd80000000000000088000000000000000,
        0x233931386637340000000000000000000000000000000001,
        0x7ffffffffffffffd80000000000000098000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x7ffffffffffffffd800000000000000a8000000000000000,
        0x233862346635390000000000000000000000000000000001,
        0x7ffffffffffffffd800000000000000b8000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x7ffffffffffffffd800000000000000c8000000000000000,
        0x236234396439300000000000000000000000000000000001,
        0x7ffffffffffffffd800000000000000d8000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x7ffffffffffffffe80000000000000008000000000000000,
        0x236234396439300000000000000000000000000000000001,
        0x7ffffffffffffffe80000000000000018000000000000000,
        0x233934393437390000000000000000000000000000000001,
        0x7ffffffffffffffe80000000000000028000000000000000,
        0x233931386637340000000000000000000000000000000001,
        0x7ffffffffffffffe80000000000000038000000000000000,
        0x233934393437390000000000000000000000000000000001,
        0x7ffffffffffffffe80000000000000048000000000000000,
        0x233937383637630000000000000000000000000000000001,
        0x7ffffffffffffffe80000000000000058000000000000000,
        0x233934393437390000000000000000000000000000000001,
        0x7ffffffffffffffe80000000000000068000000000000000,
        0x233862346635390000000000000000000000000000000001,
        0x7ffffffffffffffe80000000000000078000000000000000,
        0x233934393437390000000000000000000000000000000001,
        0x7ffffffffffffffe80000000000000088000000000000000,
        0x233931386637340000000000000000000000000000000001,
        0x7ffffffffffffffe80000000000000098000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x7ffffffffffffffe800000000000000a8000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x7ffffffffffffffe800000000000000b8000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x7ffffffffffffffe800000000000000c8000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x7ffffffffffffffe800000000000000d8000000000000000,
        0x236331393562630000000000000000000000000000000001,
        0x7ffffffffffffffe800000000000000e8000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x7fffffffffffffff80000000000000008000000000000000,
        0x233934393437390000000000000000000000000000000001,
        0x7fffffffffffffff80000000000000028000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x7fffffffffffffff80000000000000038000000000000000,
        0x233937383637630000000000000000000000000000000001,
        0x7fffffffffffffff80000000000000048000000000000000,
        0x233931386637340000000000000000000000000000000001,
        0x7fffffffffffffff80000000000000058000000000000000,
        0x236234396439300000000000000000000000000000000001,
        0x7fffffffffffffff80000000000000068000000000000000,
        0x233934393437390000000000000000000000000000000001,
        0x7fffffffffffffff80000000000000078000000000000000,
        0x233931386637340000000000000000000000000000000001,
        0x7fffffffffffffff80000000000000088000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x7fffffffffffffff80000000000000098000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x7fffffffffffffff800000000000000a8000000000000000,
        0x236131386235360000000000000000000000000000000001,
        0x7fffffffffffffff800000000000000b8000000000000000,
        0x236539633937360000000000000000000000000000000001,
        0x7fffffffffffffff800000000000000c8000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x7fffffffffffffff800000000000000d8000000000000000,
        0x236361393863340000000000000000000000000000000001,
        0x7fffffffffffffff800000000000000e8000000000000000,
        0x236331393562630000000000000000000000000000000001,
        0x7fffffffffffffff800000000000000f8000000000000000,
        0x236234396439300000000000000000000000000000000001,
        0x800000000000000080000000000000028000000000000000,
        0x233934393437390000000000000000000000000000000001,
        0x800000000000000080000000000000038000000000000000,
        0x233937383637630000000000000000000000000000000001,
        0x800000000000000080000000000000048000000000000000,
        0x233934393437390000000000000000000000000000000001,
        0x800000000000000080000000000000058000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x800000000000000080000000000000068000000000000000,
        0x233934393437390000000000000000000000000000000001,
        0x800000000000000080000000000000078000000000000000,
        0x236234396439300000000000000000000000000000000001,
        0x800000000000000080000000000000088000000000000000,
        0x236234396439300000000000000000000000000000000001,
        0x800000000000000080000000000000098000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x8000000000000000800000000000000a8000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x8000000000000000800000000000000b8000000000000000,
        0x236234396439300000000000000000000000000000000001,
        0x8000000000000000800000000000000c8000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x8000000000000000800000000000000d8000000000000000,
        0x236331393562630000000000000000000000000000000001,
        0x8000000000000000800000000000000e8000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x800000000000000180000000000000008000000000000000,
        0x233934393437390000000000000000000000000000000001,
        0x800000000000000180000000000000028000000000000000,
        0x233934393437390000000000000000000000000000000001,
        0x800000000000000180000000000000038000000000000000,
        0x233937383637630000000000000000000000000000000001,
        0x800000000000000180000000000000048000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x800000000000000180000000000000058000000000000000,
        0x233862346635390000000000000000000000000000000001,
        0x800000000000000180000000000000068000000000000000,
        0x233931386637340000000000000000000000000000000001,
        0x800000000000000180000000000000078000000000000000,
        0x233862346635390000000000000000000000000000000001,
        0x800000000000000180000000000000098000000000000000,
        0x236234396439300000000000000000000000000000000001,
        0x8000000000000001800000000000000a8000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x8000000000000001800000000000000b8000000000000000,
        0x233862346635390000000000000000000000000000000001,
        0x8000000000000001800000000000000c8000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x8000000000000001800000000000000d8000000000000000,
        0x236234396439300000000000000000000000000000000001,
        0x800000000000000280000000000000008000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x800000000000000280000000000000018000000000000000,
        0x233862346635390000000000000000000000000000000001,
        0x800000000000000280000000000000028000000000000000,
        0x233934393437390000000000000000000000000000000001,
        0x800000000000000280000000000000038000000000000000,
        0x233937383637630000000000000000000000000000000001,
        0x800000000000000280000000000000048000000000000000,
        0x233931386637340000000000000000000000000000000001,
        0x800000000000000280000000000000058000000000000000,
        0x233934393437390000000000000000000000000000000001,
        0x800000000000000280000000000000068000000000000000,
        0x236234396439300000000000000000000000000000000001,
        0x800000000000000280000000000000078000000000000000,
        0x233862346635390000000000000000000000000000000001,
        0x800000000000000280000000000000098000000000000000,
        0x233862346635390000000000000000000000000000000001,
        0x8000000000000002800000000000000a8000000000000000,
        0x233931386637340000000000000000000000000000000001,
        0x800000000000000380000000000000028000000000000000,
        0x236234396439300000000000000000000000000000000001,
        0x800000000000000380000000000000038000000000000000,
        0x233934393437390000000000000000000000000000000001,
        0x800000000000000380000000000000048000000000000000,
        0x233934393437390000000000000000000000000000000001,
        0x800000000000000380000000000000058000000000000000,
        0x233934393437390000000000000000000000000000000001,
        0x800000000000000380000000000000068000000000000000,
        0x233934393437390000000000000000000000000000000001,
        0x800000000000000380000000000000078000000000000000,
        0x233862346635390000000000000000000000000000000001,
        0x800000000000000380000000000000098000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x800000000000000480000000000000038000000000000000,
        0x233862346635390000000000000000000000000000000001,
        0x800000000000000480000000000000048000000000000000,
        0x233862346635390000000000000000000000000000000001,
        0x800000000000000480000000000000058000000000000000,
        0x236266613639360000000000000000000000000000000001,
        0x800000000000000480000000000000068000000000000000,
        0x233931386637340000000000000000000000000000000001,
        0x800000000000000580000000000000058000000000000000,
        0x233934393437390000000000000000000000000000000001,
        0x800000000000000580000000000000068000000000000000,
        0x233934393437390000000000000000000000000000000001,
        0x800000000000000680000000000000068000000000000000,
        0x1,
        0x2,
        0x22030445da671e4f5bdab7802a061ca0c55754d9703c5390266fd8b814de880,
        0x5a6f72726f4475636b2e6a736f6e,
        0x1,
        0x5a6f72726f4475636b,
        0x4,
        0x4265206361726566756c207365c3b1,
        0x6f726974612c207468657265206172,
        0x652064616e6765726f7573206d656e,
        0x2061626f7574,
        0x1,
        0x1,
        0x6e,
        0x0,
        0x6e,
        0x233131313131310000000000000000000000000000000001,
        0x7ffffffffffffffa800000000000000c8000000000000000,
        0x236563356530380000000000000000000000000000000001,
        0x7ffffffffffffffb80000000000000088000000000000000,
        0x233130313031300000000000000000000000000000000001,
        0x7ffffffffffffffb800000000000000c8000000000000000,
        0x236563356530380000000000000000000000000000000001,
        0x7ffffffffffffffc80000000000000088000000000000000,
        0x236563356530380000000000000000000000000000000001,
        0x7ffffffffffffffc80000000000000098000000000000000,
        0x233066306630660000000000000000000000000000000001,
        0x7ffffffffffffffc800000000000000c8000000000000000,
        0x233335333533350000000000000000000000000000000001,
        0x7ffffffffffffffd80000000000000038000000000000000,
        0x233337333733370000000000000000000000000000000001,
        0x7ffffffffffffffd80000000000000048000000000000000,
        0x233339333933390000000000000000000000000000000001,
        0x7ffffffffffffffd80000000000000058000000000000000,
        0x233039303930390000000000000000000000000000000001,
        0x7ffffffffffffffd80000000000000068000000000000000,
        0x236563356530380000000000000000000000000000000001,
        0x7ffffffffffffffd80000000000000088000000000000000,
        0x236664616130350000000000000000000000000000000001,
        0x7ffffffffffffffd80000000000000098000000000000000,
        0x233064306430640000000000000000000000000000000001,
        0x7ffffffffffffffd800000000000000a8000000000000000,
        0x233065306530650000000000000000000000000000000001,
        0x7ffffffffffffffd800000000000000b8000000000000000,
        0x233065306530650000000000000000000000000000000001,
        0x7ffffffffffffffd800000000000000c8000000000000000,
        0x236336383730630000000000000000000000000000000001,
        0x7ffffffffffffffd800000000000000d8000000000000000,
        0x236336383730630000000000000000000000000000000001,
        0x7ffffffffffffffd800000000000000e8000000000000000,
        0x233131313131310000000000000000000000000000000001,
        0x7ffffffffffffffd800000000000000f8000000000000000,
        0x233165316431640000000000000000000000000000000001,
        0x7ffffffffffffffe80000000000000008000000000000000,
        0x233332333233320000000000000000000000000000000001,
        0x7ffffffffffffffe80000000000000028000000000000000,
        0x233334333433340000000000000000000000000000000001,
        0x7ffffffffffffffe80000000000000038000000000000000,
        0x233335333533350000000000000000000000000000000001,
        0x7ffffffffffffffe80000000000000048000000000000000,
        0x233337333733370000000000000000000000000000000001,
        0x7ffffffffffffffe80000000000000058000000000000000,
        0x233339333933390000000000000000000000000000000001,
        0x7ffffffffffffffe80000000000000068000000000000000,
        0x233039303930390000000000000000000000000000000001,
        0x7ffffffffffffffe80000000000000078000000000000000,
        0x236664616130350000000000000000000000000000000001,
        0x7ffffffffffffffe80000000000000088000000000000000,
        0x236664616130350000000000000000000000000000000001,
        0x7ffffffffffffffe80000000000000098000000000000000,
        0x233063306330630000000000000000000000000000000001,
        0x7ffffffffffffffe800000000000000a8000000000000000,
        0x233064306430640000000000000000000000000000000001,
        0x7ffffffffffffffe800000000000000b8000000000000000,
        0x233065306530650000000000000000000000000000000001,
        0x7ffffffffffffffe800000000000000c8000000000000000,
        0x236336383730630000000000000000000000000000000001,
        0x7ffffffffffffffe800000000000000d8000000000000000,
        0x233066306630660000000000000000000000000000000001,
        0x7ffffffffffffffe800000000000000e8000000000000000,
        0x233130313031300000000000000000000000000000000001,
        0x7ffffffffffffffe800000000000000f8000000000000000,
        0x233165316431640000000000000000000000000000000001,
        0x7fffffffffffffff80000000000000008000000000000000,
        0x233165316431640000000000000000000000000000000001,
        0x7fffffffffffffff80000000000000018000000000000000,
        0x233330333033300000000000000000000000000000000001,
        0x7fffffffffffffff80000000000000028000000000000000,
        0x233332333233320000000000000000000000000000000001,
        0x7fffffffffffffff80000000000000038000000000000000,
        0x233334333433340000000000000000000000000000000001,
        0x7fffffffffffffff80000000000000048000000000000000,
        0x233165316431640000000000000000000000000000000001,
        0x7fffffffffffffff80000000000000058000000000000000,
        0x233337333733370000000000000000000000000000000001,
        0x7fffffffffffffff80000000000000068000000000000000,
        0x233039303930390000000000000000000000000000000001,
        0x7fffffffffffffff80000000000000078000000000000000,
        0x236664616130350000000000000000000000000000000001,
        0x7fffffffffffffff80000000000000088000000000000000,
        0x236664616130350000000000000000000000000000000001,
        0x7fffffffffffffff80000000000000098000000000000000,
        0x233062306230620000000000000000000000000000000001,
        0x7fffffffffffffff800000000000000a8000000000000000,
        0x236532653265320000000000000000000000000000000001,
        0x7fffffffffffffff800000000000000b8000000000000000,
        0x233064306430640000000000000000000000000000000001,
        0x7fffffffffffffff800000000000000c8000000000000000,
        0x233065306530650000000000000000000000000000000001,
        0x7fffffffffffffff800000000000000d8000000000000000,
        0x233065306530650000000000000000000000000000000001,
        0x7fffffffffffffff800000000000000e8000000000000000,
        0x233066306630660000000000000000000000000000000001,
        0x7fffffffffffffff800000000000000f8000000000000000,
        0x233265326532650000000000000000000000000000000001,
        0x800000000000000080000000000000028000000000000000,
        0x233330333033300000000000000000000000000000000001,
        0x800000000000000080000000000000038000000000000000,
        0x233165316431640000000000000000000000000000000001,
        0x800000000000000080000000000000048000000000000000,
        0x233334333433340000000000000000000000000000000001,
        0x800000000000000080000000000000058000000000000000,
        0x233335333533350000000000000000000000000000000001,
        0x800000000000000080000000000000068000000000000000,
        0x233038303830380000000000000000000000000000000001,
        0x800000000000000080000000000000078000000000000000,
        0x236664616130350000000000000000000000000000000001,
        0x800000000000000080000000000000088000000000000000,
        0x236664616130350000000000000000000000000000000001,
        0x800000000000000080000000000000098000000000000000,
        0x233061306130610000000000000000000000000000000001,
        0x8000000000000000800000000000000a8000000000000000,
        0x233062306230620000000000000000000000000000000001,
        0x8000000000000000800000000000000b8000000000000000,
        0x233063306330630000000000000000000000000000000001,
        0x8000000000000000800000000000000c8000000000000000,
        0x233064306430640000000000000000000000000000000001,
        0x8000000000000000800000000000000d8000000000000000,
        0x233065306530650000000000000000000000000000000001,
        0x8000000000000000800000000000000e8000000000000000,
        0x233065306530650000000000000000000000000000000001,
        0x8000000000000000800000000000000f8000000000000000,
        0x233165316431640000000000000000000000000000000001,
        0x800000000000000180000000000000008000000000000000,
        0x233264326432640000000000000000000000000000000001,
        0x800000000000000180000000000000028000000000000000,
        0x233265326532650000000000000000000000000000000001,
        0x800000000000000180000000000000038000000000000000,
        0x233165316431640000000000000000000000000000000001,
        0x800000000000000180000000000000048000000000000000,
        0x233332333233320000000000000000000000000000000001,
        0x800000000000000180000000000000058000000000000000,
        0x233036303630360000000000000000000000000000000001,
        0x800000000000000180000000000000068000000000000000,
        0x233037303730370000000000000000000000000000000001,
        0x800000000000000180000000000000078000000000000000,
        0x233038303830380000000000000000000000000000000001,
        0x800000000000000180000000000000088000000000000000,
        0x233039303930390000000000000000000000000000000001,
        0x800000000000000180000000000000098000000000000000,
        0x233039303930390000000000000000000000000000000001,
        0x8000000000000001800000000000000a8000000000000000,
        0x233061306130610000000000000000000000000000000001,
        0x8000000000000001800000000000000b8000000000000000,
        0x233062306230620000000000000000000000000000000001,
        0x8000000000000001800000000000000c8000000000000000,
        0x233063306330630000000000000000000000000000000001,
        0x8000000000000001800000000000000d8000000000000000,
        0x233064306430640000000000000000000000000000000001,
        0x8000000000000001800000000000000e8000000000000000,
        0x233065306530650000000000000000000000000000000001,
        0x8000000000000001800000000000000f8000000000000000,
        0x233165316431640000000000000000000000000000000001,
        0x800000000000000280000000000000008000000000000000,
        0x233165316431640000000000000000000000000000000001,
        0x800000000000000280000000000000018000000000000000,
        0x233262326232620000000000000000000000000000000001,
        0x800000000000000280000000000000028000000000000000,
        0x233264326432640000000000000000000000000000000001,
        0x800000000000000280000000000000038000000000000000,
        0x233165316431640000000000000000000000000000000001,
        0x800000000000000280000000000000048000000000000000,
        0x236232623262320000000000000000000000000000000001,
        0x800000000000000280000000000000058000000000000000,
        0x233035303530350000000000000000000000000000000001,
        0x800000000000000280000000000000068000000000000000,
        0x233036303630360000000000000000000000000000000001,
        0x800000000000000280000000000000078000000000000000,
        0x233061306130610000000000000000000000000000000001,
        0x8000000000000002800000000000000c8000000000000000,
        0x233032303230320000000000000000000000000000000001,
        0x800000000000000380000000000000008000000000000000,
        0x233033303330330000000000000000000000000000000001,
        0x800000000000000380000000000000018000000000000000,
        0x233033303330330000000000000000000000000000000001,
        0x800000000000000380000000000000028000000000000000,
        0x236164616461640000000000000000000000000000000001,
        0x800000000000000380000000000000038000000000000000,
        0x233439343934390000000000000000000000000000000001,
        0x800000000000000380000000000000048000000000000000,
        0x236230623062300000000000000000000000000000000001,
        0x800000000000000380000000000000058000000000000000,
        0x236537653765370000000000000000000000000000000001,
        0x800000000000000380000000000000068000000000000000,
        0x236539653965390000000000000000000000000000000001,
        0x800000000000000380000000000000078000000000000000,
        0x236562656265620000000000000000000000000000000001,
        0x800000000000000380000000000000088000000000000000,
        0x236565656565650000000000000000000000000000000001,
        0x800000000000000380000000000000098000000000000000,
        0x236630663066300000000000000000000000000000000001,
        0x8000000000000003800000000000000a8000000000000000,
        0x236632663266320000000000000000000000000000000001,
        0x8000000000000003800000000000000b8000000000000000,
        0x236634663466340000000000000000000000000000000001,
        0x8000000000000003800000000000000c8000000000000000,
        0x236636663666360000000000000000000000000000000001,
        0x8000000000000003800000000000000d8000000000000000,
        0x236638663866380000000000000000000000000000000001,
        0x8000000000000003800000000000000e8000000000000000,
        0x233031303130310000000000000000000000000000000001,
        0x800000000000000480000000000000008000000000000000,
        0x233032303230320000000000000000000000000000000001,
        0x800000000000000480000000000000018000000000000000,
        0x233033303330330000000000000000000000000000000001,
        0x800000000000000480000000000000028000000000000000,
        0x233033303330330000000000000000000000000000000001,
        0x800000000000000480000000000000038000000000000000,
        0x233034303430340000000000000000000000000000000001,
        0x800000000000000480000000000000048000000000000000,
        0x236164616461640000000000000000000000000000000001,
        0x800000000000000480000000000000058000000000000000,
        0x233039303930390000000000000000000000000000000001,
        0x8000000000000004800000000000000c8000000000000000,
        0x233030303030300000000000000000000000000000000001,
        0x800000000000000580000000000000008000000000000000,
        0x1,
        0x2,
    ]]
