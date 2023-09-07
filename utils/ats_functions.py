import json 
import re 
from nltk.tokenize import word_tokenize

class Ats_Functions:
    def __init__(self,path):
        self.path=path
        
        #assigns data from the path by loading load_data
        self.load_data()
        
        
    def load_data(self):
        try: 
            #loads data into the  json.data from the Json file 
            with open(self.path, 'r' ) as json_file:
                self.data=json.load(json_file)
        
        #If there appears to be File missing error, prints the statement
        except FileNotFoundError:
            print(f"File not found: {self.path}")
            self.data= None 
            
            
            
    def Check_bullet_count(text):
    # tokenizer matches all the '•' or '-'
    tokenizer = RegexpTokenizer( r'[*•\-]\s+')
    #lst stores * and • and -
    lst=tokenizer.tokenize(text)
    return len(lst)
        
        #Checks for: If the user has used appropriate no. of bullet points. And returns an COMMENT about it
    def Check_bullet_point(self):
        ct=self.Check_bullet_count()
        if ct < 3:                                      #Lower limit for bullet point                                      
            print ("Utilize More Bullet Points")
        elif ct > 8:                                    #Higher limit for bullet point
            print("Too many Bullet Points used")
        else:
            print("Good Bullet Point Utilization")
              
        
    def IsParagraph(self):
        
        if isinstance(self.data, str):
            # This regular expression pattern starts checking/counting the sentence after the first character of [.!?]
            sentence_pattern = r'[^.!?]*[.!?]'
            
            # Split the data into sentences using the sentence_pattern. 
            sentences = re.findall(sentence_pattern, self.data)
            
            # Check for paragraph: If multiple sentence then It is  paragraph
            if len(sentences) > 1:
                return True
            else:
                return False
    
    def Resume_status(self):
        if IsParagraph():
            print("RESUME IS NOT ACCEPTIBLE")
        else:
            print("RESUME IS ACCEPTIBLE")
