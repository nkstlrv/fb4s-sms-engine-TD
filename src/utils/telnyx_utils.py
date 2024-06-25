from logs.logging_config import logger
import requests
from dataclasses import dataclass


@dataclass
class TelnyxService:
    api_key: str
    profile_id: str
    from_phone_numbers: list
    url: str = "https://api.telnyx.com/v2/messages"


    def send_sms(self, to_phone_number: str, sms_body: str) -> bool | None:
        if not self.from_phone_numbers and not isinstance(self.from_phone_numbers, list):
            raise ValueError("No Phone Numbers selected")
        
        # select & shift used phone number [1, 2, 3] -> [2, 3, 1]
        from_phone_number = self.from_phone_numbers[0]
        self.from_phone_numbers.append(self.from_phone_numbers.pop(0))
        
        logger.info(f"Telnyx: send SMS - (from: {to_phone_number}; to: {to_phone_number}; body: {sms_body})")
        
        response = requests.post(
            url=self.url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "type": "SMS",
                "text": f"{sms_body}",
                "from": from_phone_number,
                "to": to_phone_number,
                "messaging_profile_id": self.profile_id,
                "webhook_url": "https://google.com"
            }
        )
        
        status_code = response.status_code
        logger.info(f"Telnyx API: Status Code - ({status_code})")
        
        if status_code == 200:
            return True
        else:
            logger.error(f"!!! Telnyx API: Error - ({response.text})")
            return False
        
        