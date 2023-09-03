import json 
import re 

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
    def Check_bullet_count(self, json_text):
        #splits the long string into multiple short string which starts with optional
        # blank <space/s> at the beginning followed by a • [alt + 0149]
        bullet_point_pattern = r'^\s*[\\u]'
        
        matches = re.findall(bullet_point_pattern, json_text, re.MULTILINE)
        
        return len(matches)
if __name__ == "__main__":
    path = 'reccomended_course.json'  # Replace with the path to your JSON file
    ats = Ats_Functions(path)
    
#test
with open('reccomended_course.json') as test:
     text=json.load(test)
# Process a specific resume
print(ats.Check_bullet_count(text))
        
