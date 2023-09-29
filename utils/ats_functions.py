import json

class Ats_Functions:
    def __init__(self, path):
        self.path = path
        with open(self.path, 'r') as json_file:
            self.data = json.load(json_file)

    def pronoun(self):
        pers_pron = ['I', 'We', 'Me', 'My', 'Mine', 'Myself', 'You', 'Your', 'Yours', 'Yourself', 'She', 'Her', 'Hers', 'Herself', 'He', 'Him', 'Himself', 'His', 'They', 'Them', 'Themself', 'Themselves', 'Their', 'Us', 'Our', 'Ourselves', 'Ourself', 'Ours', 'It', 'Itself']
        
        # Extract the text from your JSON data (adjust the key as needed)
        text = self.data.get('text_field', '') 

        lowercase = text.lower().split(" ")

        count = 0

        for pronoun in pers_pron:
            count += lowercase.count(pronoun.lower())

        threshold = 5
        if count >= threshold:
            print("Resume rejected due to overuse of personal pronouns")
            return False
        else:
            print("Resume accepted!")
            return True

