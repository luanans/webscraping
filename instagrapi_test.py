import email
import imaplib
import json
import os
import random
import re

from dotenv import find_dotenv, load_dotenv
from instagrapi import Client
from instagrapi.mixins.challenge import ChallengeChoice

env_path = find_dotenv(usecwd=True)
load_dotenv(dotenv_path=env_path)

CHALLENGE_EMAIL = os.environ.get("CHALLENGE_EMAIL")
CHALLENGE_PASSWORD = os.getenv("CHALLENGE_PASSWORD")
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def get_code_from_email(username):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(CHALLENGE_EMAIL, CHALLENGE_PASSWORD)
    mail.select("inbox")
    result, data = mail.search(None, "(UNSEEN)")
    print(result)
    print(data)
    assert result == "OK", "Error1 during get_code_from_email: %s" % result
    ids = data.pop().split()
    for num in reversed(ids):
        mail.store(num, "+FLAGS", "\\Seen")  # mark as read
        result, data = mail.fetch(num, "(RFC822)")
        assert result == "OK", "Error2 during get_code_from_email: %s" % result
        msg = email.message_from_string(data[0][1].decode())
        payloads = msg.get_payload()
        if not isinstance(payloads, list):
            payloads = [msg]
        code = None
        for payload in payloads:
            body = payload.get_payload(decode=True).decode()
            if "<div" not in body:
                continue
            match = re.search(">([^>]*?({u})[^<]*?)<".format(u=username), body)
            if not match:
                continue
            print("Match from email:", match.group(1))
            match = re.search(r">(\d{6})<", body)
            if not match:
                print('Skip this email, "code" not found')
                continue
            code = match.group(1)
            if code:
                return code
    return False


def challenge_code_handler(username, choice):
    if choice == ChallengeChoice.EMAIL:
        return get_code_from_email(username)
    return False


def change_password_handler(username):
    # Simple way to generate a random string
    chars = list("abcdefghijklmnopqrstuvwxyz1234567890!&£@#")
    password = "".join(random.sample(chars, 10))
    return password


def toJSON(obj):
    return json.dumps(
                      obj,
                      default=lambda o: o.__dict__,
                      sort_keys=True,
                      indent=4
                      )


if __name__ == "__main__":
    cl = Client()
    cl.challenge_code_handler = challenge_code_handler
    cl.login(IG_USERNAME, IG_PASSWORD)

    media_pk = cl.media_pk_from_url("https://www.instagram.com/p/CiDbLQQA7K5/")
    media_path = cl.video_download(media_pk)
    hashtag = cl.hashtag_info("dhbastards")
    user_info = cl.user_info_by_username("anitta")

    with open("instagrapi.json", "w") as f:
        media_path_json = toJSON({"media_path": str(media_path)})

        f.write(json.dumps([
                            media_path_json,
                            hashtag.dict(),
                            user_info.dict()
                            ]))

# Source: https://adw0rd.github.io/instagrapi/usage-guide/media.html
# Obs: Create a APP Password for access the gmail from imap
