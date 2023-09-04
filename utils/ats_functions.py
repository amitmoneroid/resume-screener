import json
class Ats_functions:
    def __init__(self):
        pass

    def resume_length(self,resume):
        with open(resume, "r") as json_file:
            data = json.load(json_file)
            extracted_data = [value for section in data.values() if isinstance(section, list) for dictionary in section for value in dictionary.values()]
            char = ''.join(map(str, extracted_data))
            for x in " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~":
                char = char.replace(x,"")

        print(char)
        if len(char)>670:
            return False
        else:
            return True

if __name__ == "__main__":
    smthn = Ats_functions()
    resume = 'temp.json'
    value = smthn.resume_length("temp.json")

