from speech_recognition import Microphone, Recognizer, AudioFile, UnknownValueError, RequestError

from text_to_speech import talk

def listen():
    recog = Recognizer()
    mic = Microphone()

    with mic:
        recog.adjust_for_ambient_noise(mic,1.2)

        print("parlez ->")
        audio = recog.listen(mic,2)

    try:
        recognized = recog.recognize_google(audio, language="fr-FR")
        print("vous ->", recognized)
        talk(recognized)
        return recognized
    except RequestError as err:
        print(err)
        return None
    except UnknownValueError:
        print("Unable to recognize")
        return None


if __name__ == '__main__':
    listen()
