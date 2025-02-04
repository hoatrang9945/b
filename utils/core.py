import requests
from loguru import logger
from solana.publickey import PublicKey 
from solana.rpc.api import Client
from solana.rpc.types import TokenAccountOpts

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




def get_token_account(endpoint: str, owner: PublicKey, mint: PublicKey):
    account_data = Client(endpoint).get_token_accounts_by_owner(owner, TokenAccountOpts(mint))
    if account_data["result"]["value"] == []: return PublicKey("So11111111111111111111111111111111111111112")
    return PublicKey(account_data['result']['value'][0]['pubkey'])


def sale_info(balance_before: dict, balance_after: dict):
    base_symbol, quote_symbol = balance_before.keys()
    base_before, quote_before = balance_before.values()
    base_after, quote_after = balance_after.values()
    sold_amount = base_before - base_after
    quote_received = quote_after - quote_before
    price = quote_received / sold_amount
    logger.info(
        f'Sold {sold_amount} {base_symbol}, price: {price} {quote_symbol}, {quote_symbol} received: {quote_received}')


def purchase_info(balance_before: dict, balance_after: dict):
    base_symbol, quote_symbol = balance_before.keys()
    base_before, quote_before = balance_before.values()
    base_after, quote_after = balance_after.values()
    bought_amount = base_after - base_before
    quote_spent = quote_before - quote_after
    price = quote_spent / bought_amount
    logger.info(
        f'Bought {bought_amount} {base_symbol}, price: {price} {quote_symbol}, {quote_symbol} spent: {quote_spent}')
