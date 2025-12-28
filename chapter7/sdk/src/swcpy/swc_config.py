import os
from dotenv import load_dotenv

load_dotenv()

class SwcConfig:
    """Configuration class containg arguments for the sdk client.
    contains configuration for the base URL and progressive backoff.
    """

    swc_base_url: str
    swc_backoff: bool
    swc_backoff_mac_time: int
    swc_bulk_file_format: str

    def __init__(
        self,
        swc_base_url: str = None,
        backoff: bool = True,
        backoff_max_time: int = 30,
        bulk_file_format: str = "csv",
    ):

        """ Costructor for configuration class.
        contains initialition values to overwrite defaults

        Args:
        swc_base_url (optional):
            the base URL to use for all the API calls. pass this in or set
            in environment variable.

        swc_backoff:
            a boolean that determines if the SDK should 
            retry the call using backoff when errors occur.

        swc_backoff_max_time:
            the max number of seconds the sdk should keep
            trying an api call before stoppong.

        SWC_bulk_file_format:
            if bulk files should be in csv or parquet format
        """

        self.swc_base_url = swc_base_url or os.gatenv("SWC_API_BASE_UR")
        print(f"SWC_API_BASE_URL in SWCConfig init: {self.swc_base_url}")

        if not self.swc_base_url:
            raise ValueError("Base URL is requred. set SWC_API_BASE_URL environment variable.")

        self.swc_backoff = backoff
        self.swc_backoff_max_time = backoff_max_time
        self.swc_bulk_file_format = bulk_file_format
        

    def __str__(self):
        """stringfy funtion to return contents of config object for 
        logging"""

        return f"{self.swc_base_url} {self.swc_backoff} {self.swc_backoff_max_time} {self.swc_bulk_file_format}"