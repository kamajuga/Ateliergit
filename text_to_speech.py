import pyttsx3

def talk(text):
    engine = pyttsx3.init("sapi5")
    #voice = engine.getProperty('voices')[0]
    engine.setProperty('voice', 'french')
    engine.setProperty('rate', 155)
    engine.say(text)
    engine.runAndWait()
    

if __name__ == '__main__':
    
    talk('Bonjour, je m\'appelle Julius')