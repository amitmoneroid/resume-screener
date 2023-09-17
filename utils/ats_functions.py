import json 
import re 
from nltk.tokenize import RegexpTokenizer

class Ats_Functions:
    def __init__(self,path):
        self.path=path
        
        #assigns data from the path by loading load_data
        self.load_data()
        
        #Hi I am currently in a meeting
    def load_data(self):
        try: 
            #loads data into the  json.data from the Json file 
            with open(self.path, 'r' ) as json_file:
                self.data=json.load(json_file)
        
        #If there appears to be File missing error, prints the statement
        except FileNotFoundError:
            print(f"File not found: {self.path}")
            self.data= None 
            
            
            
    def Count_bullet(text):
    # tokenizer matches all the '•' or '-'
        tokenizer = RegexpTokenizer( r'[*•\-]\s+')
    #lst stores * and • and -
        lst=tokenizer.tokenize(text)
        return len(lst)
        
        #Checks for: If the user has used appropriate no. of bullet points
    def Check_bullet_point(self):
        ct=self.Count_bullet()
        if   ct > 3 and ct < 8:                              #checks if it is within the Resume limit suggestion                                              
            return True
        else :                                    
            return False
              
        
    def Count_Paragraph(self):
        no_of_paragraph=0                                                         #   checks for no. of paragraph                        
        remove_bullet=text.split('•')                                             #                                       
        data_without_bullet = ''.join(remove_bullet)                              #   removes bullet and stores the data in data_without_bullet
        remove_hyphen_bullet=data_without_bullet.split('-')                       #          
        data_without_bullet_hyphen=''.join(remove_hyphen_bullet)                  #   removes hyohen and stores the data in data_without_bullet_hyphen          
        pattern = r' {2,}|\n'                                                     #           
        isolated_paragraaph=re.split(pattern, data_without_bullet_hyphen)         #   This splits the rest of the data with : If it is a new line or multiple spaces then split            
                                                                                  #   It lets u store multiple paragraph and lets u check more than one paragraph from a single string                     
        for pararaph in isolated_paragraaph:                                      #                           
            # regular expression                                                  #               
            paragraph_pattern = r'[^.!?]*[.!?]'                                   #   This pattern splits the string into substring without removing the punctuation marks[unlike sentence tokenization]                                 
            sentences = re.findall(paragraph_pattern, pararaph)                   #                                                   
            # Check if there are multiple sentences                                                             
            if len(sentences) > 1:                                                                                                      
                no_of_paragraph=no_of_paragraph+1
        return no_of_paragraph
        
    # checks for paragraph
    def IsParagraph(self):
        if self.Count_Paragraph > 0 :
            return True
        else:
            return False