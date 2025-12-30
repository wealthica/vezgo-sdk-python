"""
Teams Resource.

Teams represent your Vezgo application and its configuration.
"""

from typing import Any, Dict

from vezgo.resources.base import BaseResource


class Teams(BaseResource):
    """
    Teams API resource.

    This resource allows you to retrieve information about your Vezgo
    team/application configuration.

    Example:
        ```python
        team = vezgo.teams.info()
        print(f"Team: {team['name']}")
        ```
    """

    def info(self) -> Dict[str, Any]:
        """
        Get information about your Vezgo team/application.

        Returns:
            Team information including name, redirect_uris, features, etc.

        Example:
            ```python
            team = vezgo.teams.info()
            print(f"Team: {team['name']}")
            print(f"Features: {team['features']}")
            ```
        """
        return self._get(f"/teams/info?client_id={self.client.client_id}")

