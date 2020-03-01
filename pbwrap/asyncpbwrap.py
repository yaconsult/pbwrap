import pbwrap.formatter as formatter
from pbwrap import Pastebin
from pbwrap.constants import API_OPTIONS
from pbwrap.models import Paste

try:
    import aiohttp

    class AsyncPaste:
        """Defines a Paste from Pastebin paste contains the following fields:
        key,
        date,
        title,
        size,
        expire_date,
        private,
        format_short,
        format_long,
        url,
        hits.
        """

        def __init__(self, paste_dict):
            self.key = None
            for k, v in paste_dict.items():
                setattr(self, k, v)

        def __cmp__(self, x):
            return vars(self) == vars(x)

        async def get_raw_text(self):
            """Fetch the text of a paste via the public API.
                :returns: the paste's text
                :rtype: string, None
            """
            if self.key is not None:
                r = await aiohttp.get("https://pastebin.com/raw/" + self.key)
                return await r.text
            return None

        async def scrape_raw_text(self):
            """Fetch the ext of a paste via the Paid API.
                :returns: the paste's text
                :rtype: string, None
            """
            if self.key is not None:
                parameter = {"i": self.key}
                r = await aiohttp.get(
                    "https://scrape.pastebin.com/api_scrape_item.php", params=parameter
                )

                return await r.text
            return None

    class AsyncPastebin(Pastebin):
        """Async version of Pastebin class.
        
        Represents your communication with the Pastebin API through its functions
        you can use every API endpoint avalaible.

        Most functions require at least an api_dev_key parameter.
        Functions for manipulating your pastes through the API require an api_user_key.
        """

        def __init__(self, dev_key=None):
            """Instantiate a Pastebin Object

            :param api_dev_key: Your API Pastebin key
            :type api_dev_key: string
            """
            super().__init__(api_dev_key=dev_key)

    @staticmethod
    async def get_raw_paste(paste_id):
        """Return raw string of given paste_id.

           get_raw_paste(pasted_id)

           :type paste_id: string
           :param paste_id: The ID key of the paste

           :returns: the text of the paste
           :rtype: string
        """
        r = await aiohttp.get("https://pastebin.com/raw/" + paste_id)
        return await r.text

    @staticmethod
    async def get_archive():
        """Return archive paste link list.Archive contains 25 most recent pastes.

           :returns: a list of url strings
           :rtype: list
        """
        r = await aiohttp.get("https://pastebin.com/archive")

        return formatter.archive_url_format(await r.text)

    @staticmethod
    async def get_recent_pastes(limit=50, lang=None):
        """get_recent_pastes(limit=50, lang=None)

            Return a list containing dictionaries of paste.

            :param limit: the limit of the items returned defaults to 50
            :type limit: int

            :param lang: return only pastes from certain language defaults to None
            :type lang: string

            :returns: list of Paste objects.
            :rtype: list(Paste)
        """
        parameters = {"limit": limit, "lang": lang}

        r = await aiohttp.get(
            "https://scrape.pastebin.com/api_scraping.php", params=parameters
        )
        paste_list = list()
        for paste in await r.json():
            paste_list.append(AsyncPaste(paste))
        return paste_list


except ImportError:
    pass
