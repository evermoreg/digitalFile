
from twilio.rest import Client

class Twilio:

	def phoneMessage(receiver):
		account_sid="ACd41e3f5c3fc3297497082469b1731095"
		auth_token="a0642ac646c6fbbe095d5ffcabc20471"

		client = Client(account_sid, auth_token)

		client.messages.create(to=receiver, from_="+13522932377", body="testing")

