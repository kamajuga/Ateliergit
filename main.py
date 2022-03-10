

if __name__ == '__main__':
    #from text_to_speech import talk
    #from speech_r import listen
    from request_info_speech import Information
    
    User_Info = Information()


    print('Merci de vous identifier:')
    #talk('Bonjour, je m\'appelle Meya. Je suis l\'assistante de collecte de demandes de MerciYanis. Merci de vous identifier:')
    User_Info.Identify()

    print("Quelle est l'objet de votre demande?")
    #talk("Quelle est l'objet de votre demande?")
    title = input()
    #title = listen()
    User_Info.Title(title)

    print("Où avez vous eu cette panne?")
    #talk("Où avez vous eu cette panne?")
    place = input()
    #place = listen()
    User_Info.PLace(place)

    print("Insérez un commentaire (détaillez la demande):")
    #talk("Insérez un commentaire (détaillez la demande):")

    comment = input()
    #comment = listen()
    User_Info.Comment(comment)

    print("Voici un récapitulatif de vos informations:")
    #talk("Voici un récapitulatif de vos informations:")
    User_Info.Recap_Information()

    User_Info.check_infos()
    print("Merci, vos informations seront envoyés auprès du service correspondant.\nNous vous recontacterons dans les plus bref délais")
    #talk("Vos informations seront envoyés auprès du service correspondant.\nNous vous recontacterons dans les plus bref délais")



    # confirmation = ""
    # while confirmation.lower != "o" and confirmation.lower() != "n":
    #     confirmation = input("Tapez \"o\" pour oui ou \"n\" pour non:")
    #     if confirmation.lower() == "o":
    #         print("Merci, vos inforations seront envoyés auprès du service correspondant.\n Nous vous recontacteront dans les plus bref délais")
    #     elif confirmation.lower() == "n":
    #         Information.Modify()
    #     else:
    #         print("Saisie invalide!")
    #


    pass