from twilio.rest import Client

# put your own credentials here
account_sid = "AC75b8723f81cbd2ae29eca135a3ecb450"
auth_token = "49ad69047baa1c2ee4f3f6b320851461"

client = Client(account_sid, auth_token)

client.messages.create(
    to="+263772919383",
    from_="+14243476010",
    body="you can do everything Evermore, all what is needed is practise, practise and prasctise! :) i have done it"
)
