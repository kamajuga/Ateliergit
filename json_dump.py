import json


def dump_unknown_text(str_to_dump):
    with open('json_data.json', 'r') as outfile:
        data = json.load(outfile)
        if str_to_dump not in data:
            data.append(str_to_dump)

    outfile.close()

    with open('json_data.json', 'w') as outfile:

        json_string = json.dumps(data)
        outfile.write(json_string)
        outfile.close()


def dump_in_training_model(text, entities):
    # list must be a list of list [[...],...]
    with open('training.json', 'r') as outfile:
        data = json.load(outfile)
        outfile.close()

    dictionnary = {
        "text": text,
        "entities": entities
    }
    data["tag"].append(dictionnary)
    with open('json_data.json', 'w') as outfile:
        json_string = json.dumps(dictionnary)
        outfile.write(json_string)
        outfile.close()

    pass


if __name__ == "__main__":
    dump_unknown_text('pourquoi')
    #dump_in_training_model()
