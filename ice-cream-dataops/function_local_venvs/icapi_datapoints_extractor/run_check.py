import os
import sys

from pathlib import Path
from pprint import pprint

from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthClientCredentials

# This is necessary to import adjacent modules in the function code.
sys.path.insert(0, str(Path(__file__).parent / "local_code"))

from local_code.handler import handle # noqa: E402

try:
    from dotenv import load_dotenv

    for parent in Path(__file__).resolve().parents:
        if (parent / ".env").exists():
            load_dotenv(parent / '.env')
except ImportError:
    ...


def main() -> None:
    credentials = OAuthClientCredentials(
        token_url="https://login.microsoftonline.com/16e3985b-ebe8-4e24-9da4-933e21a9fc81/oauth2/v2.0/token",
        client_id="9c5b26bb-4eb1-4059-9f6f-99a2b3ab2cb5",
        client_secret=os.environ["ICAPI_EXTRACTORS_CLIENT_SECRET"],
        scopes=['https://westeurope-1.cognitedata.com/.default'],
    )

    client = CogniteClient(
        config=ClientConfig(
            client_name="CDF-Toolkit:0.5.30",
            project="cdf-bootcamp-67-test",
            base_url="https://westeurope-1.cognitedata.com",
            credentials=credentials,
        )
    )

    print("icapi_datapoints_extractor LOGS:")
    response = handle(
        client=client,
        data={'backfill': True, 'hours': 336},
    )

    print("icapi_datapoints_extractor RESPONSE:")
    pprint(response)


if __name__ == "__main__":
    main()
