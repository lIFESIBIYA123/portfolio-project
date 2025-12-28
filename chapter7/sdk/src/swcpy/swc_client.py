import httpx
import swcpy.swc_config as config #1
from .schemas import League, Team, Player, Performance, Counts #2
from typing import List #3
import backoff #4
import logging #5
logger = logging.getLogger(__name__) 

class SWCClent:
    """ Interacts with SportWorldCentral API.
    
    this sdk class simplifies the process of using the swc fantasy
    football api. it supports all the functions of the swc api and returns 
    validated data type.
    
    typical usage exaple:
        client = SWCClient()
        response = client.get_health_check()

    """

    HEALTH_CHECK_ENDPOINT = "/" #6
    LIST_LEAGUES_ENDPOINT = "/V0/leagues/"
    LIST_PLAYERS_ENDPOINT = "/V0/players/"
    LIST_PERFOMANCES_ENDPOINT = "/V0/performances/"
    LIST_TEAMS_ENDPOINT = "/V0/teams/"
    GET_COUNTS_ENDPOINT = "/V0/counts/"

    BULK_FILE_BASE_URL = (
        "https://raw.githubusercontent.com/125609507" #7
        + "/portfolio-project/main/bulk/"
    )

    def __init__(self, input_config: config.SWCConfig): #8
        """ class constructor that sets variables from configuration object."""

        logger.debug(f"Bulk file base URL: {self.BULK_FILE_BASE_URL}")
        logger.debug(f"Input config: {input_config}")

        self.swc_base_url = input_config.swc_base_url
        self.backoff = input_config.swc_backoff
        self.backoff_max_time = input_config.swc_backoff_max_time
        self.bulk_file_format = input_config.swc_bulk_file_format

        self.BULK_FILE_NAMES = { #9
            "players": "players_data",
            "leagues": "league_data",
            "performances": "performance_data",
            "teams": "team_data",
            "team_players": "team_player_data",
            }
        
        if self.backoff: #10
            self.call_api = backoff.on_exception(
                wait_gen=backoff.expo,
                exception=(httpx.RequestError, httpx.HTTPStatusError),
                max_time=self.backoff_max_time,
                jitter=backoff.random_jitter,
            )(self.call_api)

            if self.bulk_file_format.lower() == "parquet": #11
                self.BULK_FILE_NAMES = {
                    key: value + ".parquet" for key, value in
                    self.BULK_FILE_NAMES.items()
                }

            else:
                self.BULK_FILE_NAMES = {
                    key: value + ".csv" for key, value in
                    self.BULK_FILE_NAMES.items()
                }
            logger.debug(f"Bulk file dictionary: {self.BULK_FILE_NAMES}")


    def call_api(self,
                api_endpoint: str,
                api_params: dict = None
            ) -> httpx.Response:
            """Makes API call and logs errors."""

            if api_params:
                api_params = {key: val for key, val in api_params.items() if val is not None}

            try:
                with httpx.Client(base_url=self.swc_base_url) as client: 
                    logger.debug(f"base_url: {self.swc_base_url}, api_endpoint: {api_endpoint}, api_params: {api_params}")
                    response = client.get(api_endpoint, params=api_params)
                    logger.debug(f"Response JSON: {response.json()}")
                    return response
            except httpx.HTTPStatusError as e:
                logger.error(
                    f"HTTP status error occurred: {e.response.status_code} {e.response.text}"
                )
                raise
            except httpx.RequestError as e:
                logger.error(f"Request error occurred: {str(e)}")
                raise

########################################################################

########################################################################

    def get_helth_check(self) -> httpx.Response:
        """Checks if API is running and healthy.
        
        calls the API health check endpoint and returns a standard 
        message if the API is running normarlly. Can be used to check 
        status of API before making more complicted API calls.

        Returns:
        An httpx.Response object that contains the HTTP status,
        JSON response and other information received form the API.

        """

        logger.debug("Enter health check")
        endpoint_url = self.HEALTH_CHECK_ENDPOINT # 1
        return self.call_api(endpoint_url)

    def list_leagues(
        self,
        skip: int = 0,
        limit: int = 100,
        minimum_last_changed_date: str = None,
        league_name: str = None,
    ) -> List[League]: # 2
        """Returns a list of leagues filtered by parameters.
        
        Calls the api v0/leagues endpoint and returns a list of 
        league objects.

        returns:
        A List of schemas.league objects. Each represents one 
        SportworldCentral fantasy league.
        """

        logger.debug("Enter list leagues")
        
        params = { #3
        "skip": skip,
        "limit": limit,
        "minimum_last_changed_date": minimum_last_changed_date,
        "league_name": league_name,
        }

        response = self.call_api(self.LIST_LEAGUES_ENDPOINT, params) # 4
        return [League(**league) for league in response.json()] #5

    #    Your goal in this statement is to iterate through the list of
    #     dictionaries returned from the API and create a list of
    #     Pydantic League objects. You use a list comprehension,
    #     which is a Pythonic way to build lists without using a
    #     recursive loop. Using the general syntax list = [expression
    #     for item in iterable], you can create lists from other lists
    #     very easily. 


    ################################################################
    # bulk download
    ################################################################

    def get_bulk_player_file(self) -> bytes: #1
        """Returns a bulk file player data"""

        logger.debug("Enter get bulk player file")

        player_file_path = self.BULK_FILE_BASE_URL + self.BULK_FILE_NAMES["players"] #2

        response = httpx.get(player_file_path, follow_redirects-True) #3

        if response.status_code == 200:
            logger.debug("File downloaded successfully")
            return response.content #4