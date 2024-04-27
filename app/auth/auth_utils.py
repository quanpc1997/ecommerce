from datetime import datetime, timedelta

import jwt
from loguru import logger

ALGORITHM_ENCODE = "RS256"
ACCESS_TOKEN_EXPIRY_DAYS = 2
REFRESH_TOKEN_EXPIRY_DAYS = 7


def get_payload(payload, token_type="access_token"):
    new_payload = payload

    if token_type == "access_token":
        expiry_date = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRY_DAYS)
    else:
        expiry_date = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS)

    new_payload["exp"] = expiry_date

    return new_payload


async def create_token_pair(payload, public_key, private_key, header=None):
    try:
        access_token = jwt.encode(
            get_payload(payload, "access_token"),
            private_key,
            algorithm=ALGORITHM_ENCODE,
        )
        refesh_token = jwt.encode(
            get_payload(payload, "refresh_token"),
            private_key,
            algorithm=ALGORITHM_ENCODE,
            headers=header,
        )
        payload_decode = jwt.decode(
            access_token, public_key, algorithms=[ALGORITHM_ENCODE]
        )
        if payload_decode is None:
            logger.error("Can't verify access token")
        else:
            logger.info(f"payload_decode = {payload_decode}")

        return access_token, refesh_token
    except Exception as e:
        logger.error(f"Error: {e}")
        return e
