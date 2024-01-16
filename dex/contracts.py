from web3 import Web3

# slippage: start
SLIPPAGE = 0.5
# slippage: end

# chain id: start
CHAIN_ID = {
    "ZkSync": 324,
    "Base": 8453
}
# chain id: end

# chain name: start
CHAIN_NAME = {
    CHAIN_ID["ZkSync"]: "ZkSync",
    CHAIN_ID["Base"]: "Base"
}
# chain name: end

# rpc: start
RPC = {
    CHAIN_ID["ZkSync"]: "https://mainnet.era.zksync.io",
    CHAIN_ID["Base"]: "https://mainnet.base.org"
}
# rpc: end

# tokens: start
TOKENS = {
    CHAIN_ID["ZkSync"]: {
        "ETH": Web3.to_checksum_address("0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91"),
        "STABLE": {
            "USDC": Web3.to_checksum_address("0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4")
        }
    },
    CHAIN_ID["Base"]: {
        "ETH": Web3.to_checksum_address("0x4200000000000000000000000000000000000006"),
        "STABLE": {
            "USDbC": Web3.to_checksum_address("0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA")
        }
    }
}
# tokens: end

# spacefi: start
SPACEFI_CONTRACT = {
    CHAIN_ID["ZkSync"]: {
        "router": Web3.to_checksum_address("0xbE7D1FD1f6748bbDefC4fbaCafBb11C6Fc506d1d")
    }
}
# spacefi: end

# syncswap: start
SYNCSWAP_CONTRACT = {
    CHAIN_ID["ZkSync"]: {
        "router": Web3.to_checksum_address("0x2da10A1e27bF85cEdD8FFb1AbBe97e53391C0295"),
        "pool": Web3.to_checksum_address("0xf2DAd89f2788a8CD54625C60b55cD3d2D0ACa7Cb")
    }
}
# syncswap: end

# woofi: start
WOOFI_CONTRACT = {
    CHAIN_ID["ZkSync"]: {
        "router": Web3.to_checksum_address("0xfd505702b37Ae9b626952Eb2DD736d9045876417")
    },
    CHAIN_ID["Base"]: {
        "router": Web3.to_checksum_address("0x27425e9FB6A9A625E8484CFD9620851D1Fa322E5")
    }
}
# woofi: end

# dmail: start
DMAIL_CONTRACT = {
    CHAIN_ID["ZkSync"]: {
        "router": Web3.to_checksum_address("0x981F198286E40F9979274E0876636E9144B8FB8E")
    },
    CHAIN_ID["Base"]: {
        "router": Web3.to_checksum_address("0x47fbe95e981C0Df9737B6971B451fB15fdC989d9")
    }
}
# dmail: end

# grape: start
GRAPE_CONTRACT = {
    CHAIN_ID["ZkSync"]: {
        "router": Web3.to_checksum_address("0xf343FE6d7e430cB5607Aa8CdB4a725758592b73b")
    },
    CHAIN_ID["Base"]: {
        "router": Web3.to_checksum_address("0x44c1Cf007C9761c4665d4E0172515146692509CA")
    }
}
# grape: end

# uniswap: start
UNISWAP_CONTRACT = {
    CHAIN_ID["Base"]: {
        "router": Web3.to_checksum_address("0x2626664c2603336E57B271c5C0b26F421741e481"),
        "quoter": Web3.to_checksum_address("0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a")
    }
}
# uniswap: end

# pancake: start
PANCAKESWAP_CONTRACT = {
    CHAIN_ID["Base"]: {
        "router": Web3.to_checksum_address("0x678Aa4bF4E210cf2166753e054d5b7c31cc7fa86"),
        "quoter": Web3.to_checksum_address("0xB048Bbc1Ee6b733FFfCFb9e9CeF7375518e25997")
    }
}
# pancake: end

# izumi: start

IZUMI_CONTRACT = {
    CHAIN_ID["ZkSync"]: {
        "router": Web3.to_checksum_address("0x943ac2310D9BC703d6AB5e5e76876e212100f894"),
        "quoter": Web3.to_checksum_address("0x30C089574551516e5F1169C32C6D429C92bf3CD7")
    },
    CHAIN_ID["Base"]: {
        "router": Web3.to_checksum_address("0x02F55D53DcE23B4AA962CC68b0f685f26143Bdb2"),
        "quoter": Web3.to_checksum_address("0x2db0AFD0045F3518c77eC6591a542e326Befd3D7")
    }
}
# izumi: end

# zkstars: start
ZKSTARS_NFT = {
    CHAIN_ID["ZkSync"]: {
        1: "0xe7Ed1c47E1e2eA6e9126961df5d41798722A7656",
        2: "0x53424440d0EaD57e599529B42807a0BA1965dd66",
        3: "0x406B1195f4916B13513Fea102777DF5bd4AF06Eb",
        4: "0xd834c621deA708a21B05EAf181115793EaA2f9D9",
        5: "0xf19b7027d37c3321194d6C5F34Ea2E6cbc73fa25",
        6: "0x56Bf83E598ce80299962bE937fE0Ba54F5d5E2b2",
        7: "0xaFec8DF7b10303C3514826C9e2222a16f1486BEe",
        8: "0x8595D989a96cDBDc1651e3C87ea3D945E0460097",
        9: "0x945B1eDCd03e1D1Ad9255c2b28e1c22F2C819F0e",
        10: "0x808D59a747BfEDd9bcb11A63B7E5748D460b614D",
        11: "0xC92fc3F19645014c392825e3CfA3597412B0D913",
        12: "0x8Dd8706CBC931c87694E452CAa0a83A564753241",
        13: "0x8DD3c29F039E932eBd8eaC873b8b7A56d17e36c6",
        14: "0xCA0848cADb25e6Fcd9c8cE15BcB8f8Da6C1fC519",
        15: "0x06d52C7E52E9F28e3AD889ab2083fE8Dba735D52",
        16: "0x86f39D51C06CaC130CA59eABEdC9233A49fCC22a",
        17: "0xEE0D4A8F649D83F6BA5e5c9E6c4D4F6ae846846A",
        18: "0xfda7967C56CE80f74B06e14aB9c71c80Cb78b466",
        19: "0x0d99EFCde08269e2941A5e8A0a02d8e5722403fC",
        20: "0xf72CF790AC8D93eE823014484fC74F2f1E337Bf6",
    },
    CHAIN_ID["Base"]: {
        1: "0x657130a14E93731dFEcC772d210AE8333303986c",
        2: "0x4C78c7D2F423cf07c6DC2542ac000c4788f03657",
        3: "0x004416bef2544DF0F02F23788C6adA0775868560",
        4: "0x39B06911D22F4D3191827ED08AE35b84F68843e4",
        5: "0x8a6a9Ef84CD819A54EEe3cF7CFD351d21Ab6b5FE",
        6: "0x8fb3225D0A85f2A49714Acd36cDCD96a7B2B7FbC",
        7: "0x91ad9Ed35B1E9FF6975aa94690fa438EFB5A7160",
        8: "0x32D8EEB70eAB5f5962190A2bb78A10A5A0958649",
        9: "0xAB62313752F90c24405287AD8C3bcf4c25c26E57",
        10: "0x6F562B821b5cb93d4de2B0Bd558cc8E46b632a08",
        11: "0xb63159A26664A89abce783437fC17786af8bb46d",
        12: "0x7E6B32D7Eecddb6BE496f232Ab9316a5bf9f4e17",
        13: "0xCB03866371FB149F3992F8d623D5AAa4B831e2Fd",
        14: "0x78C85441F53A07329e2380e49f1870199F70cEE1",
        15: "0x54C49cB80a0679E3217F86d891859B4E477b56C3",
        16: "0xAd6f16F5fF3461c83d639901BAE1fb2A8A68aA31",
        17: "0x023A7c97679F2C121A31BaCF37292Dabf7AB97E9",
        18: "0xd3c6386362daBAb1a30aCC2c377D9AC2cc8B7B16",
        19: "0x5dabFf127caD8D075b5ceA7f795DCBae1ddf471d",
        20: "0xeD0407D6B84B2c86418CaC16a347930B222B505C",
    }
}
# zkstars: end

# maverick: start
MAVERICK_CONTRACT = {
    CHAIN_ID["ZkSync"]: {
        "router": "0x39E098A153Ad69834a9Dac32f0FCa92066aD03f4",
        "pool_information": "0x57D47F505EdaA8Ae1eFD807A860A79A28bE06449",
        "position": "0xFd54762D435A490405DDa0fBc92b7168934e8525",
        "position_inspector": "0x852639EE9dd090d30271832332501e87D287106C",
        "pool_address": "0x41C8cf74c27554A8972d3bf3D2BD4a14D8B604AB",
    },
    CHAIN_ID["Base"]: {
        "router": "0x32AED3Bce901DA12ca8489788F3A99fCe1056e14",
        "pool_information": "0x6E230D0e457Ea2398FB3A22FB7f9B7F68F06a14d",
        "position": "0x0d8127A01bdb311378Ed32F5b81690DD917dBa35",
        "position_inspector": "0x550056A68cB155b6Cc3DeF4A7FA656260e7842e2",
        "pool_address": "0x06e6736cA9e922766279A22b75A600Fe8B8473B6",
    }
}
# maverick: end

# other: start
ZERO_ADDRESS = Web3.to_checksum_address("0x0000000000000000000000000000000000000000")
ETH_MASK = Web3.to_checksum_address("0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE")
# other: end
