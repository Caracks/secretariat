from tools.evolution_api import EvolutionAPI
from core.config import MSG_CALL, Settings


def main():
    evolution_api = EvolutionAPI(
        api_url=Settings.evolution_api_url,
        instance=Settings.evolution_instance,
        api_key=Settings.evolution_api_key,
    )

    result = evolution_api.call(
        endpoint="settings",
        action="set",
        payload={
            "rejectCall": True,
            "msgCall": MSG_CALL,
            "alwaysOnline": False,
            "readMessages": False,
            "readStatus": False,
            "groupsIgnore": False,
            "syncFullHistory": False

        },
        persist=False,
    )


if __name__ == "__main__":
    main()
