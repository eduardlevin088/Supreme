import requests
import os
import uuid
import json
import config
import logging

logger = logging.getLogger(__name__)

api_key = config.LANGFLOW_API
url = config.LANGFLOW_WEBHOOK


def agent_response(message: str, session_id: str) -> str:
    """Generates LangFlow Agent response to the message"""
    
    logger.info(f"Processing agent request - session_id: {session_id}, message length: {len(message) if message else 0}")

    payload = {
        "output_type": "chat",
        "input_type": "chat",
        "input_value": message,
        "session_id": session_id
    }

    headers = {
        "x-api-key": api_key
    }

    try:
        logger.debug(f"Sending request to LangFlow API: {url}")
        response = requests.request("POST", url, json=payload, headers=headers)
        
        logger.debug(f"Response status code: {response.status_code}")
        response.raise_for_status()

        data = response.json()
        logger.debug(f"Response received successfully")
        
        output_message = data['outputs'][0]['outputs'][0]['outputs']['message']['message']
        logger.info(f"Agent response generated successfully - response length: {len(output_message) if output_message else 0}")
        
        return output_message

    except requests.exceptions.RequestException as e:
        logger.error(f"Error making API request to LangFlow: {e}", exc_info=True)
        raise

    except (KeyError, IndexError, ValueError) as e:
        logger.error(f"Error parsing LangFlow response: {e}", exc_info=True)
        logger.debug(f"Response data: {data if 'data' in locals() else 'N/A'}")
        raise