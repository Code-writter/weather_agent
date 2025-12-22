from dotenv import load_dotenv
load_dotenv()
import asyncio
import speech_recognition as sr
from openai import OpenAI, AsyncOpenAI
from openai.helpers import LocalAudioPlayer

client = OpenAI(
    api_key="AIzaSyAGM5Ax4czi3bCbVrqEHUF7iAu_yjwjd6Y",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

async_client = AsyncOpenAI()

async def tts(speech : str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        instructions="Always speek in cheerfull manner with full of delight and happyness",
        input=speech,
        response_format="pcm"
    )as reponse:
        await LocalAudioPlayer().play(reponse)




def main():
    r = sr.Recognizer() # Speech to text 

    # Get access to microphone
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source) # Removing bg noise
        r.pause_threshold = 2 # If user pause for 2 sec start the recogniniton
        SYSTEM_PROMPT = """
            You are an expert voice agent. You are given transcript of what user has said using voice you need to output as if you are a voice agent and what ever you speek will be converted back to audio using AI and played back to user.
            """
        # For History
        messages = [
            {
                "role" : "system",
                "content" : SYSTEM_PROMPT
            },
        ]

        while True:

            print("Speak Somthing...")
            audio = r.listen(source)
            print("Processing audio (STT)...")
            stt = r.recognize_google(audio)

            print("*-*-"*10)
            # print("\n You said, ",stt)

            # Append in History
            messages.append(
                {
                    "role" : "user",
                    "content" : stt
                }
            )

            response = client.chat.completions.create(
                model="gemini-2.5-flash",
                messages=messages
            )

            # print("AI Response : ", response.choices[0].message.content)
            asyncio.run(tts(speech=response.choices[0].message.content))


main()