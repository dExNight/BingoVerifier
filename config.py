from dotenv import load_dotenv
import os

load_dotenv()

IS_MAINNET_STR: str = os.getenv("IS_MAINNET")
IS_MAINNET = IS_MAINNET_STR.lower() in ("true", "1") if IS_MAINNET_STR else False

TONAPI_KEY: str = os.getenv("TONAPI_KEY")
MNEMONIC_PHRASE: str = os.getenv("MNEMONIC_PHRASE")

