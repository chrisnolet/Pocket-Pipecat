#
# Copyright (c) 2024, Daily
#
# SPDX-License-Identifier: BSD 2-Clause License
#

import aiohttp
import argparse
import os

from pipecat.transports.services.helpers.daily_rest import DailyRESTHelper

async def configure(aiohttp_session: aiohttp.ClientSession):
    parser = argparse.ArgumentParser(description="Daily AI SDK Bot Sample")
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        required=False,
        help="URL of the Daily room to join")

    parser.add_argument(
        "-k",
        "--apikey",
        type=str,
        required=False,
        help="Daily API Key (needed to create an owner token for the room)",
    )

    args, unknown = parser.parse_known_args()

    key = args.apikey or os.getenv("DAILY_API_KEY")
    url = args.url or os.getenv("DAILY_SAMPLE_ROOM_URL")

    if not url:
        raise Exception(
            "No Daily room specified. Use the -u/--url option from the command line, or set DAILY_SAMPLE_ROOM_URL in your environment to specify a Daily room URL.")

    if not key:
        raise Exception("No Daily API key specified. Use the -k/--apikey option from the command line, or set DAILY_API_KEY in your environment to specify a Daily API key, available from https://dashboard.daily.co/developers.")

    daily_rest_helper = DailyRESTHelper(
        daily_api_key=key,
        daily_api_url=os.getenv("DAILY_API_URL", "https://api.daily.co/v1")
    )

    # Create a meeting token for the given room with an expiration 1 hour in
    # the future.
    expiry_time: float = 60 * 60

    token = daily_rest_helper.get_token(url, expiry_time)

    return (url, token)
