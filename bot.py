import ssl
import logging
from threading import Event
from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from config import conf
from datetime import datetime
from schema import AccessData
import crud
import json
import api
import requests

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

BOT_TOKEN = conf['bot_token']
SOCKET_TOKEN = conf['bot_socket']
BOTNAME = 'bot'

ALLOW_USERS = ['U05K140HSUQ','']

SLACK_CLIENT = SocketModeClient(
    # This app-level token will be used only for establishing a connection
    app_token=SOCKET_TOKEN,  # xapp-A111-222-xyz
    # You will be using this AsyncWebClient for performing Web API calls in listeners
    web_client=WebClient(token=BOT_TOKEN, ssl=ssl_context)  # xoxb-111-222-xyz
)

from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest

def process(client: SocketModeClient, req: SocketModeRequest):
    if req.type == "events_api":
        # Acknowledge the request anyway
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)

        if req.payload["event"]["type"] == "message" \
            and req.payload["event"].get("subtype") is None:
            access_user_id = req.payload['event']['user']
            message_text = req.payload['event']['text']
            access_time = req.payload['event']['ts']
            channel_id = req.payload['event']['channel']

            ts = float(access_time)
            convert_time = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.000000+00:00')
                    
            access_data = {
                "user_id": access_user_id,
                "channel_id": channel_id,
                "access_time": convert_time,
                "access_id": access_user_id
            }

            try:
                access_user_id = requests.post(
                    'http://localhost:8080/access',
                    json=access_data,
                    verify=False
                )
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
            
            # allow api check 
            if access_user_id:
                message_list = message_text.split(' ')
                if message_list[0] == 'ioc':
                    ioc_item = message_list[1]
                    ioc_type = message_list[2]
                    
                    ioc_input = {
                        "ioc_item": ioc_item,
                        "ioc_type": ioc_type
                    }

                    virus_ioc_data = requests.post(
                        'http://localhost:8080/ioc/virustotal',
                        json=ioc_input,
                        verify=False
                    )

                    ctx_ioc_data = requests.post(
                        'http://localhost:8080/ioc/ctx',
                        json=ioc_input,
                        verify=False
                    )

                    client.web_client.chat_postMessage(
                        text=virus_ioc_data.text,
                        channel=req.payload["event"]["channel"],
                        timestamp=req.payload["event"]["ts"]
                    )

                    client.web_client.chat_postMessage(
                        text=ctx_ioc_data.text,
                        channel=req.payload["event"]["channel"],
                        timestamp=req.payload["event"]["ts"]
                    )
                elif message_list[0] == 'bob':
                    bob_wiki_data = requests.get(
                        'http://localhost:8080/bob-wiki',
                        verify=False
                    )
                    
                    bob_wiki_list = json.loads(bob_wiki_data.text)

                    post_messages = []
                    for bob_wiki in bob_wiki_list:
                        name = bob_wiki['user_name']
                        age = bob_wiki['age']
                        hometown = bob_wiki['hometown']
                        contents = bob_wiki['contents']
                        post_messages.append(f'교육생 {name}의 나이는 {age}살이며 {hometown}에 거주한다. {contents}')

                    client.web_client.chat_postMessage(
                        text="\n".join(post_messages),
                        channel=req.payload["event"]["channel"],
                        timestamp=req.payload["event"]["ts"]
                    )
            else:
                pass

    if req.type == "interactive" \
        and req.payload.get("type") == "shortcut":
        if req.payload["callback_id"] == "hello-shortcut":
            # Acknowledge the request
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)
            # Open a welcome modal
            client.web_client.views_open(
                trigger_id=req.payload["trigger_id"],
                view={
                    "type": "modal",
                    "callback_id": "hello-modal",
                    "title": {
                        "type": "plain_text",
                        "text": "Greetings!"
                    },
                    "submit": {
                        "type": "plain_text",
                        "text": "Good Bye"
                    },
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "Hello!"
                            }
                        }
                    ]
                }
            )

    if req.type == "interactive" \
        and req.payload.get("type") == "view_submission":
        if req.payload["view"]["callback_id"] == "hello-modal":
            # Acknowledge the request and close the modal
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)

if __name__ == "__main__":
    try:
        #rtm.start()
        # Add a new listener to receive messages from Slack
        # You can add more listeners like this
        SLACK_CLIENT.socket_mode_request_listeners.append(process)
        # Establish a WebSocket connection to the Socket Mode servers
        SLACK_CLIENT.connect()
        # Just not to stop this process
        Event().wait()
    except Exception as main_e:
        error = str(main_e)
        logging.warning('main func: %s', error)