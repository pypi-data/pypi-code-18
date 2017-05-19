import json
from collections import Counter
from urllib.request import urlopen, HTTPError
from valleydata.exceptions import InvalidIPAddressException


class valleydata:
    """Class for generate stats
    """

    def __init__(self, date_list=[], locations=[]):
        """
        Args:
            date_list (list, optional): List of datetime's
        """
        self.date_list = date_list
        self.locations = locations

    def _sort_dates_by(self, value):
        """Internal function for sort dates

        Args:
            value (int): strftime

        Returns:
            LIST: sorted date list
        """
        return sorted(
            [date.strftime(value) for date in self.date_list]
        )

    def get_start_date(self):
        return sorted(self.date_list)[0]

    def get_top_hours(self, amount=3):
        """Get list of ordered hours and occurrences

        Args:
            amount (int, optional): amount of desired results

        Returns:
            [(string, integer)]: List of tuples (hour, occurrences)
        """
        occurrences = Counter(self._sort_dates_by('%H hs'))
        return sorted(occurrences.most_common(amount), key=lambda tup: tup[0])

    def get_top_weekdays(self, amount=3):
        """Get list of ordered weekdays and occurrences

        Args:
            amount (int, optional): amount of desired results

        Returns:
            [(string, integer)]: List of tuples (weekday, occurrences)
        """
        occurrences = Counter(self._sort_dates_by('%w'))
        days = ['Monday', 'Tuesday',
                'Wednesday', 'Thursday', 'Friday',
                'Saturday', 'Sunday']
        results = (
            sorted(occurrences.most_common(amount), key=lambda tup: tup[0])
        )
        return [(days[int(result[0])], result[1]) for result in results]

    def get_top_cities(self, amount=3):
        """Get list of ordered cities and occurrences"""
        occurrences = Counter(self.locations)
        results = (
            sorted(occurrences.most_common(amount), key=lambda tup: tup[1],
                   reverse=True)
        )

        return results

    def get_ip_info(self, ip_address):
        """Get info from the IP (uses external API)

        Args:
            ip_address (str): IPv4 address

        Returns:
            dict: {
              "ip": str,
              "hostname": str,
              "city": str,
              "region": str,
              "country": str,
              "loc": str(coordinates),
              "org": str,
              "postal": str
            }

        Raises:
            InvalidIPAddressException: Wrong ip format
        """
        url = 'http://ipinfo.io/%s/json' % ip_address
        try:
            with urlopen(url) as response:
                raw_data = response.read().decode()
                data = json.loads(raw_data)
                return data
        except HTTPError:
            raise InvalidIPAddressException
