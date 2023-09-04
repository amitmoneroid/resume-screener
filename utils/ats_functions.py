import json
class Ats_functions:
    def __init__(self):
        pass


#this func returns the value true or false 
    def resume_length(self,resume):
        threshold_limit = 670  
#This needs to be updated with the correct data
        with open(resume, "r") as json_file:
            data = json.load(json_file)
            extracted_data = [value for section in data.values() if isinstance(section, list) for dictionary in section for value in dictionary.values()]
            char = ''.join(map(str, extracted_data))
#droppin all the special characters and whitespces
            for x in " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~":
                char = char.replace(x,"")
        if len(char)>threshold_limit:
            return False
        else:
            return True

if __name__ == "__main__":
    smthn = Ats_functions()
    resume = 'temp.json'
    value = smthn.resume_length(resume)
# 'resume' consists of the input json file 

