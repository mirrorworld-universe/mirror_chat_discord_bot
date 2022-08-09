import requests
from config import Config


class Pegasus:
    def __init__(self, node_id):
        self.node_id = node_id

    def generate_response(self, input_text):
        try:
            data = requests.post(
                Config.PEGASUS_BASE_URL + Config.PEGASUS_APP_ID + "/nodes/" + self.node_id +
                "/conversation?accessKey=" + Config.PEGASUS_ACCESS_KEY + "&accessToken=" + Config.PEGASUS_ACCESS_TOKEN,
                json={"text": input_text}
            )

            return data.json()['data'][0]['text']
        except Exception as e:
            print(repr(e))
            return ""
