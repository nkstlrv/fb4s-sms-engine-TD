from utils.fub_utils import FUB
from utils.twilio_utils import Twilio
from logs.logging_config import logger
import json


def get_signature(team_member_id: int):

    team_member_signature = "\n\nFB4S Team"

    try:
        with open("database/signatures.json", "r") as f:
            all_signatures = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_signatures = []

    for signature in all_signatures:
        if signature.get("fub_id") == team_member_id:
            team_member_signature = signature.get("signature")
            break

    return team_member_signature


def send_note_to_buyer_by_sms_view(note_id: int) -> dict:
    result = {
        "sms_text": None,
        "contact_name": None,
        "contact_phone": None,
        "sms_sent": False,
        "assigned_team_member_id": None,
        "sms_signature": None
    }

    fub = FUB()

    # get note data
    note_data = fub.get_note(note_id)

    if note_data["success"] is True:

        # get buyer_id and note message for sms
        buyer_id = note_data["data"]["personId"]
        note_message: str = note_data["data"]["body"]

        # get buyer data
        buyer_data = fub.get_buyer(buyer_id)

        if buyer_data["success"] is True and "[scheduled]" in note_message:

            buyer_name = buyer_data["data"]["name"]
            assigned_team_member_id = buyer_data["data"]["assignedUserId"]
            result["assigned_team_member_id"] = assigned_team_member_id

            team_member_signature = get_signature(assigned_team_member_id)
            result["sms_signature"] = team_member_signature

            note_message += team_member_signature

            result["contact_name"] = buyer_name

            buyer_phones = buyer_data["data"]["phones"]

            # get buyer phone number
            buyer_phone = buyer_phones[0]["value"] if buyer_phones and isinstance(buyer_phones, list) else None

            logger.info(f"{send_note_to_buyer_by_sms_view.__name__} -- BUYER NAME - {buyer_name}; BUYER PHONE - {buyer_phone}")

            if buyer_phone:
                twilio = Twilio()
                result["contact_phone"] = buyer_phone

                note_message = note_message.replace("[scheduled] ", "")

                # send sms
                logger.info(f"{send_note_to_buyer_by_sms_view.__name__} -- SENDING NOTE AS SMS - {note_message}")
                sending_result = twilio.send_sms(buyer_phone, note_message)
                result["sms_sent"] = sending_result["success"]

        result["sms_text"] = note_message

    return result
