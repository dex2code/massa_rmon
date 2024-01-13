from loguru import logger
from time import sleep as t_sleep
from requests import post as r_post
from sys import exit as sys_exit
import json


@logger.catch
def send_telegram_message(message: str="") -> bool:

    try:
        tg_answer = r_post(
            url=f"https://api.telegram.org/bot{app_settings['telegram_key']}/sendMessage",
            headers={
                "content-type": "application/x-www-form-urlencoded"
            },
            data={
                "chat_id": app_settings['telegram_chat'],
                "text": f"{app_settings['telegram_nickname']}: {message}"
            },
            timeout=60
        )
    except Exception as E:
        logger.warning(f"Cannot send Telegram message to chat id {app_settings['telegram_chat']}: ({str(E)})")
        return False

    if tg_answer.status_code != 200:
        logger.warning(f"Cannot send Telegram message to chat id {app_settings['telegram_chat']}: HTTP {tg_answer.status_code}")
        return False
    else:
        logger.info(f"Telegram message sent to chat id {app_settings['telegram_chat']} successfully")
        return True


@logger.catch
def pull_node_api(node_api: str="") -> int:
    logger.info(f"Checking node API: '{node_api}'")

    api_header = {
        "content-type": "application/json"
    }

    api_payload = {
        "id": 0,
        "jsonrpc": "2.0",
        "method": "get_status",
        "params": []
    }

    try:
        api_response = r_post(
            url=node_api,
            headers=api_header,
            data=json.dumps(api_payload),
            timeout=app_settings['probe_timeout_seconds']
        )
        api_response = api_response.json()
        api_response = api_response['result']['chain_id']
        api_response = int(api_response)
    except Exception as E:
        return 0
    else:
        return api_response


@logger.catch
def main() -> None:
    logger.info(f"Entering main loop")

    while True:
        for node_name in app_settings['nodes']:
            node_api = app_settings['nodes'][node_name]
            node_status = pull_node_api(node_api=node_api)

            if node_status:
                logger.info(f"Node '{node_name}' seems alive with chain_id {node_status}")
                if nodes_status[node_name] != "alive":
                    nodes_status[node_name] = "alive"
                    send_telegram_message(f"✅ Node '{node_name}' ({node_api}) became alive with chain_id={node_status}!")
            else:
                logger.warning(f"Node '{node_name}' ({node_api}) seems dead or unavailable!")
                if nodes_status[node_name] != "dead":
                    nodes_status[node_name] = "dead"
                    send_telegram_message(f"⚠ Node '{node_name}' ({node_api}) seems dead or unavailable! Check node status or firewall settings (sudo ufw allow 33035/tcp)")
        
        logger.info(f"Sleeping for {app_settings['loop_timeout_seconds']} seconds...")
        t_sleep(app_settings['loop_timeout_seconds'])


if __name__ == "__main__":
    logger.add("main.log", format="{time} -- {level} -- {message}", level="DEBUG", rotation="1 week", compression="zip")
    logger.info(f"*** MASSA remote monitoring starting service...")

    with open("settings.json", "r") as settings_file:
        app_settings = json.load(settings_file)
    
    if app_settings['loop_timeout_seconds'] < 600:
        logger.error(f"There is no reason to set main delay less than 600 seconds (10 minutes). Please adjust your settings.")
        send_telegram_message(message=f"‼ Configuration error: 'loop_timeout_seconds' must be greater than 600. Service stopped!")
        sys_exit(1)
    
    if app_settings['probe_timeout_seconds'] > 60:
        logger.error(f"There is no reason to set probe timeout more than 60 seconds (1 minute). Please adjust your settings.")
        send_telegram_message(message=f"‼ Configuration error: 'probe_timeout_seconds' must be less than 60. Service stopped!")
        sys_exit(1)
    
    nodes_list = ""
    nodes_status = {}

    for node_name in app_settings['nodes']:
        node_api = app_settings['nodes'][node_name]
        nodes_status[node_name] = "unknown"
        nodes_list += f" - {node_name}: {node_api}\n"
        logger.info(f" - '{node_name}': '{node_api}'")

    logger.info(f"Settings file loaded successfully!")
    logger.info(f"Watching nodes with {app_settings['loop_timeout_seconds']} seconds loop delay:")

    send_telegram_message(message=f"💡 Service successfully started to watch the following nodes:\n{nodes_list.rstrip()}\n\nMain loop delay: {app_settings['loop_timeout_seconds']} seconds\n")

    main()
