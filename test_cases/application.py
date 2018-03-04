"""
This class has fetch_name_from_file which is not implemented
However, I need to use them in is_in_team
"""


class Application:
    _members = ['Apurva', 'Prajval', 'Nikhil']

    def fetch_name_from_file(self):
        """
        :rtype: object
        """
        pass  # Not yet defined

    def is_in_team(self):
        name = self.fetch_name_from_file()
        return name in self._members
