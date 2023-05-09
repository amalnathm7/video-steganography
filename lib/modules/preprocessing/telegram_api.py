import requests
import asyncio
import telegram
bot = telegram.Bot(token='5882351675:AAFdKzSj2houUk9MSvE_Gqh7OWmRt86IDkY')
def send_to_telegram(message):

    apiToken = '5882351675:AAFdKzSj2houUk9MSvE_Gqh7OWmRt86IDkY'
    chatID = '-848597745'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)

#send_to_telegram('/assets/cover_video/akiyo_cif.y4m')
# bot.send_video(chat_id=-277411123, video=open('D:/Final Year Project/video_steganography/assets/cover_videos/video.mp4', 'rb'), supports_streaming=True)

send_to_telegram("Hello from Python!")
async def send_video():
    # await asyncio.sleep(1)
    print("inside the function");
    await bot.send_video(chat_id=-848597745, video=open('assets/cover_videos/Movie.mp4', 'rb'), supports_streaming=True)
    # await bot.send_video(chat_id=-848597745, video=open('assets/cover_videos/akiyo_cif.y4m', 'rb'), supports_streaming=True)
    
async def main():
    await send_video()
    
asyncio.run(main())






























































# # import os
# # import telegram
# # import asyncio

# # # Replace with your bot's API key
# # bot = telegram.Bot(token='5882351675:AAFdKzSj2houUk9MSvE_Gqh7OWmRt86IDkY')

# # # Replace with the chat id of the group you want to send the video to
# # chat_id = -277411123

# # # Replace with the path to the video file you want to send
# # video_file = 'assets/cover_videos/akiyo_cif.y4m'

# # # Send the video file
# # async def send_video():
# #     await bot.send_video(chat_id=chat_id, video=open(video_file, 'rb'))


# # asyncio.run(send_video())