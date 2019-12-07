import os

# Database
DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASSWORD = "postgres"

# Telegram [Bots]
BOT_TOKEN = os.getenv("ZOMICBOT_TOKEN")
BOT_URL = "https://api.telegram.org/bot{}".format(BOT_TOKEN)
OFFSET = 92714943
TELEGRAM_SLEEP = 2

# Blockchain [Utils]
WEB3_PROVIDER = "https://ropsten.infura.io"
KEYSTORE_PATH = "keystores"
DEPLOY_GAS_LIMIT = 2000000
DEFAULT_GAS_PRICE = "1"
DEFAULT_GAS_LIMIT = 500000
BALLOT_ABI = "solidity/ballot.abi"
BALLOT_BYTECODE = "solidity/ballot.bytecode"
BALLOT_ADDRESS = "0x51EC36f097b0bB78cab445d7FCD382e85EEbb4Dd"  # "0x84563aC8F1b2293ce572fdEf50886e33E1B51Ac8"
PROOFS_ABI = "solidity/proofs.abi"
PROOFS_BYTECODE = "solidity/proofs.bytecode"
PROOFS_ADDRESS = "0xE7389300c701EF4a833fA335D4228244F0fb23E8"

# Types [Utils]
DATE = "%Y-%m-%d"
TIMESTAMP = "%Y-%m-%d %H:%M:%S"
ISO_TIMESTAMP = "%Y-%m-%dT%H:%M:%S.%f"

TOPICS = ["Ambiente", "Educação", "Saúde"]
STATUS = ["Aberta", "Aprovada", "Rejeitada"]
