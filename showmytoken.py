import sys  # to use sys.argv
import yaml  # Used to read .yaml files. Read: https://yaml.org
import requests  # Lets python talks to the internet
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


API_ENDPOINT = 'https://wax.eosrio.io/v2/state/get_tokens'


def load_wallets(path):
    """Loads wallets from a YAML file.

    Args:
        path: path to YAML file. Ex. 'wallets.yaml'.
    Returns:
        Dict data. Ex. {wallets: [wallet1.wam, wallets2.wam]}

    """
    # (1)
    with open(path, 'r') as f:
        wallets = yaml.safe_load(f)

    # (2)
    lst_wallets = wallets['wallets']
    print(f'Loaded wallets {wallets}')

    return lst_wallets


def get_data(wallet):
    """Get token from API_ENDPOINT.

    Args:
        wallet: wallet in string format. Ex. 'abcde.wam'.
    Returns:
        JSON data.
    Raises:
        RetryError: if retry exceeds 3.

    """
    s = requests.Session()

    # (3)
    # (4)
    retries = Retry(total=3,
                    backoff_factor=0.2,
                    status_forcelist=[i for i in range(500, 600)])

    s.mount('http://', HTTPAdapter(max_retries=retries))
    r = s.get(f'{API_ENDPOINT}?account={wallet}')

    return r.json()


def parse_token_data(data, token_name):
    """Reads amount of token from get_data() then return in float.

    Args:
        data: data from get_my_token().
        token_name: Ex. 'TLM'
    Returns:
        amount in float.

    """

    for i in data['tokens']:
        if token_name in i.values():

            return float(i['amount'])

    return float(0)


def get_token_from_wallets(lst_wallets, token_name):
    """Get token from wallets then print amount and, total amount.

    Args:
        lst_wallets: list of wallets.
        token_name: Ex. 'WAX'

    """
    total = 0

    for wallet in lst_wallets:
        d = get_data(wallet)
        amount = parse_token_data(d, token_name)
        total += amount
        print(f'{wallet}: {amount:.2f}{token_name}')

    print('='*20)
    print(f'Total: {total:.2f}')


def main(argv):
    
    print('='*20)
    print('www.teamninjaaaa.com\nLearn to code, and have fun with NFTs!')
    print('='*20)

    lst_wallets = load_wallets('wallets.yaml')
    token_name = str(sys.argv[1]).upper()

    get_token_from_wallets(lst_wallets, token_name)


if __name__ == '__main__':
    main(sys.argv)

# (1)
# Let's open our wallets.yaml
# With open closes the file automagickally!

# (2)
# Let's see our loaded wallets.yaml
# wallet object is a dic...t. We extract the list inside using wallets['wallets'] syntax.
# f string is sure useful! Read: https://realpython.com/python-f-strings/#f-strings-a-new-and-improved-way-to-format-strings-in-python.

# (3)
# Let's be nice and not spam the API.

# (4)
# https://stackoverflow.com/questions/15431044/can-i-set-max-retries-for-requests-request.
# This stackoverflow discusses strategies regarding retries.

# (5)
# https://www.geeksforgeeks.org/how-to-use-sys-argv-in-python/
# We don't want to hard code token_name so we use sys.argv to get the string
