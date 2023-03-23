from twilio.rest import Client

account_sid = 'AC5d21bd445d5dc11dc5e0524ef0a9dad6'
auth_token = 'd8ff47fca11d8e905a07f21363282b76'
client = Client(account_sid, auth_token)

# message = client.messages.create(
#     from_='whatsapp:+14155238886',  # Twilio sandbox number
#     media_url=['assets/cover_videos/movie.mp4'],
#     to='whatsapp:K2OCxNAl8uTADZTOwRztx6'
# )


video_url = 'assets/cover_videos/movie.mp4'

# Upload the video file to Twilio's servers
video = client \
    .videos \
    .create(
        friendly_name='My Video',
        asset_url=video_url
    )

from_whatsapp_number='whatsapp:+14155238886'
to_whatsapp_number='whatsapp:K2OCxNAl8uTADZTOwRztx6'

# Send the video to the WhatsApp group
message = client \
    .messages \
    .create(
        from_=from_whatsapp_number,
        body='',
        media_url=[video.sid],
        to=to_whatsapp_number
    )

print(message.sid)
