from typing import List
from starknet_py.net.models import StarknetChainId
from dataclasses import dataclass, field


@dataclass
class NetworkMetadata:
    id: str
    chain_id: int = 0
    storage_bucket: str = ''
    base_domain: str = 'briq.construction'
    auction_address: str = '0'
    auction_ducks: str = '0'
    box_address: str = '0'
    briq_address: str = '0'
    booklet_address: str = '0'
    set_address: str = '0'
    erc20_address: str = '0'
    attributes_registry_address: str = '0'
    factory_address: str = '0'
    box_addresses: List[str] = field(default_factory=list)
    booklet_addresses: List[str] = field(default_factory=list)
    sets_addresses: List[str] = field(default_factory=list)
    sets_1155_addresses: List[str] = field(default_factory=list)


DEVNET = NetworkMetadata(
    id="localhost",
    auction_address="0x00c126cf6a2deda8af86deefb15ed85967f12e2deae0848e90918be0caa9ecce",
    box_address="0x0386dfa3727b66bc2c10bee1941b47d247cf24a06b89f087dc9e6072ccfdd559",
    briq_address="0x001fd19cbb5df0d12db9050f0ab86a55866ee4ce3d5cf3f897587b9513d8a134",
    booklet_address="0x03203d30b47a3c659e936cd44971a3d1ff522c138488a26250b191eef8199abb",
    erc20_address="0x62230ea046a9a5fbc261ac77d03c8d41e5d442db2284587570ab46455fd2488",
)

TESTNET = NetworkMetadata(
    id="starknet-testnet",
    chain_id=StarknetChainId.GOERLI.value,
    base_domain='test.sltech.company',
    auction_address="0x033f840d4f7bfa20aaa128e5a69157355478d33182bea6039d55aae3ffb861e2",
    auction_ducks="0x04ef0bd475fb101cc1b5dc2c4fc9d11b4fa233cfa1876924ec84b2f3dcf32f75",
    box_address="0x043bafcb15f12c137229406f96735eba51018fe75e5330058479556bc77dfd94",
    briq_address="0x0068eb19445f96b3c3775fba757de89ee8f44fda42dc08173a501acacd97853f",
    booklet_address="0x018734a90e5df97235c0ff83f92174cf6f16ad3ec572e38e2e146e47c8878839",
    attributes_registry_address="0x06a780187cfd58ad6ce1279cb4291bcf4f8acb2806dc1dccc9aee8183a9c1c40",
    set_address="0x038bf557306ab58c7e2099036b00538b51b37bdad3b8abc31220001fb5139365",
    erc20_address="0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7",

    box_addresses=["0x043bafcb15f12c137229406f96735eba51018fe75e5330058479556bc77dfd94"],
    booklet_addresses=["0x018734a90e5df97235c0ff83f92174cf6f16ad3ec572e38e2e146e47c8878839"],
    sets_addresses=["0x038bf557306ab58c7e2099036b00538b51b37bdad3b8abc31220001fb5139365"],
)

TESTNET_DOJO = NetworkMetadata(
    id="starknet-testnet-dojo",
    chain_id=StarknetChainId.SEPOLIA_TESTNET.value,
    storage_bucket="briq-bucket-test-1",
    base_domain='test.sltech.company',

    briq_address="0x78af24bd385d041ad87df067908dc6710baac4c7eed5e1cb3bc0ca28a7e1d1d",
    factory_address="0x7679e15068cc0d308ff270d340862d52362b1d0f9833f14d829d8e7f39d366f",

    box_addresses=[
        "0x32ccbf4f8832f75e4484602d624ba2d43780f480cb6c3ca6c4cb9ead398a0fd",  # box_nft_sp
        "0x222e344352c9b757c002a83ce87484284a50924fb3014040740bc6e171242a0",  # box_nft_briqmas
    ],

    booklet_addresses=[
        "0x161f7d29180fbce59ed7e73edd1a2ea3268c9aff22335cbbd856bfbcf84445d",  # booklet_ducks
        "0x32b0abe087c2e30c34b64944250dafcabf7642f3a82cff9ea52fd6f86aa212c",  # booklet_starknet_planet
        "0x6b05f3548418c462262d6e4b9ec9f2835b4b8aacc0736e5c3cd152abb811fe6",  # booklet_briqmas
        "0x3d3fdccf11997bb97b75d5f1818318f9648043bb4dba7b82a78ed57d67d9eac",  # booklet_fren_ducks
    ],

    sets_addresses=[
        "0x515428b8c0b1524f370d298998bb0c8681f745dbb7ebcb57934f5575beb5252",  # set_nft
        "0x611ed988cd95e6c59f31b5fafd1fcd2194b77bf8421c44112a280f6bbe4f943",  # set_nft_ducks
        "0x67e94f5fb9bf932e0d1ca38c4fadd4734b549ae7332eae93ab81646c3261c7b",  # set_nft_sp
        "0x695f67f607c255194c29eaa584a9098636f961708cdaf4f1a1707d7c431dc7f",  # set_nft_briqmas
    ],

    sets_1155_addresses=[
        "0x12555f235252050fa12d49393b7975afb91746fc80318ab3511b8577c8dfb97",  # set_nft_1155_fren_ducks
    ],

    erc20_address="0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7",
)


MAINNET = NetworkMetadata(
    id="starknet-mainnet",
    chain_id=StarknetChainId.MAINNET.value,
    storage_bucket="briq-bucket-prod-1",
    base_domain='briq.construction',

    auction_address="0x01712e3e3f133b26d65a3c5aaae78e7405dfca0a3cfe725dd57c4941d9474620",
    auction_ducks="0x00b9bb7650a88f7e375ae8d31d48b4d4f13c6c34344839837d7dae7ffcdd3df0",
    box_address="0x01e1f972637ad02e0eed03b69304344c4253804e528e1a5dd5c26bb2f23a8139",
    briq_address="0x00247444a11a98ee7896f9dec18020808249e8aad21662f2fa00402933dce402",
    booklet_address="0x05faa82e2aec811d3a3b14c1f32e9bbb6c9b4fd0cd6b29a823c98c7360019aa4",
    attributes_registry_address="0x008d4f5b0830bd49a88730133a538ccaca3048ccf2b557114b1076feeff13c11",
    set_address="0x01435498bf393da86b4733b9264a86b58a42b31f8d8b8ba309593e5c17847672",
    erc20_address="0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7",

    box_addresses=["0x01e1f972637ad02e0eed03b69304344c4253804e528e1a5dd5c26bb2f23a8139"],
    booklet_addresses=["0x05faa82e2aec811d3a3b14c1f32e9bbb6c9b4fd0cd6b29a823c98c7360019aa4"],
    sets_addresses=["0x01435498bf393da86b4733b9264a86b58a42b31f8d8b8ba309593e5c17847672"],
)

MAINNET_DOJO = NetworkMetadata(
    id="starknet-mainnet-dojo",
    chain_id=StarknetChainId.MAINNET.value,
    storage_bucket="briq-bucket-prod-dojo",
    base_domain='briq.construction',

    briq_address="0x2417eb26d02947416ed0e9d99c7a023e3565fc895ee21a0a0ef88a524a665d6",
    factory_address="0x3374d4a1b4f8dc87bd680ddbd4f1181b3ec3cf5a8ef803bc4351603b063314f",

    box_addresses=[
        "0x73e3b5e6c7924f752a158c2b07f606bd5b885029da0ac1e3cde254985303f50",  # box_nft_sp
        "0x69699ce808b5459a3b652b5378f8c141e1dc79e10f4e7b486439fd989b7dfb1",  # box_nft_briqmas
    ],

    booklet_addresses=[
        "0x3311cdef78f70c1b13568e6dabda043c5e9d2736c0c02a35aa906d91d69836b",  # booklet_ducks
        "0x2fd50e1bdd7400a8fc97eb63aa4f3423a7ec72ebe78d413ce410ec60a35afea",  # booklet_starknet_planet
        "0x4bbb2000c80ff79c2aa3b8aa83ee69c103469181a19d01d7f3ee4313a8031",  # booklet_briqmas
        "0x35d3f5be7b3b06a2d02a539faecd45bf4a04644aee7290359bd595047929a92",  # booklet_fren_ducks
    ],

    sets_addresses=[
        "0x3f96949d14c65ec10e7544d93f298d0cb07c498ecb733774f1d4b2adf3ffb23",  # set_nft
        "0x4fa864a706e3403fd17ac8df307f22eafa21b778b73353abf69a622e47a2003",  # set_nft_ducks
        "0xe9b982bdcbed7fa60e5bbf733249ff58da9fe935067656e8175d694162df3",  # set_nft_sp
        "0x12a6eeb4a3eecaf16667e2b630963a4c215cdf3715fb271370a02ed6e8c1942",  # set_nft_briqmas
    ],

    sets_1155_addresses=[
        "0x433a83c97c083470a1e2f47e24cbc53c4a225f69ffc045580a7279e7f077c79",  # set_nft_1155_fren_ducks
    ],

    erc20_address="0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7",
)

TESTNET_LEGACY = NetworkMetadata(id="starknet-testnet-legacy", storage_bucket="briq-bucket-prod-1")


def get_network_metadata(network: str):
    return {
        'localhost': DEVNET,
        'starknet-testnet': TESTNET,
        'starknet-testnet-dojo': TESTNET_DOJO,
        'starknet-mainnet': MAINNET,
        'starknet-mainnet-dojo': MAINNET_DOJO,
    }[network]

