import PyPDF2
import re
import json

pdf_file_path = 'utils\example.pdf'  # Replace with the path to your PDF file

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            extracted_text = ''

            for page_number in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_number]
                page_text = page.extract_text()
                extracted_text += page_text

            return extracted_text

    except Exception as e:
        print(f"Error: {e}")
        return None

def replace_bullet_points(text):
    # Replace bullet points (•) with newline characters
    text_with_newlines = re.sub(r'•', '\n', text)
    return text_with_newlines

def text_to_json(text):
    lines = text.split('\n')
    json_data = {}

    # Extract name
    json_data["name"] = lines[0].strip()

    # Extract contact information
    contact_info = {}
    for line in lines[1:]:
        if "|" in line:
            parts = line.split("|")
            for part in parts:
                part = part.strip()
                if re.match(r'^\+\d', part):  # Phone number starts with a '+' character
                    contact_info["phone"] = part
                elif "@" in part:  # Email contains '@'
                    contact_info["email"] = part
                elif "linkedin.com" in part:
                    contact_info["linkedin"] = part
                elif "github.com" in part:
                    contact_info["github"] = part
                elif "hackerrank.com" in part or "leetcode.com" in part:
                    contact_info["hackerrank/leetcode"] = part
    json_data["contact_information"] = contact_info

    # Initialize sections as lists
    sections = []
    current_section = None

    # Process the lines into sections
    for line in lines[1:]:
        line = line.strip()
        if line.isupper():
            current_section = line
        elif line:
            sections.append((current_section, line))

    # Group section lines into sections
    grouped_sections = {}
    for section, line in sections:
        if section not in grouped_sections:
            grouped_sections[section] = []
        grouped_sections[section].append(line)

    # Convert grouped sections into a JSON object
    for section, lines in grouped_sections.items():
        if section == "EDUCATION":
            education_data = {}
            if len(lines) > 1:
                education_data["institution"] = lines[0]
                education_data["degree"] = lines[1]
                gpa_match = re.search(r"(\d+\.\d+)", lines[1])
                if gpa_match:
                    education_data["gpa"] = float(gpa_match.group(1))
                location_duration = lines[1].split()[-6:]
                education_data["location"] = " ".join(location_duration[:-3])
                education_data["duration"] = " ".join(location_duration[-3:])
            json_data["education"] = education_data
        elif section == "COURSEWORK / SKILLS":
            json_data["coursework_skills"] = lines
        elif section == "PROJECTS":
            projects = []
            project_data = {}
            for line in lines:
                if "|" in line:
                    project_parts = line.split("|")
                    if len(project_parts) > 1:
                        project_data["name"] = project_parts[0].strip()
                        project_info = project_parts[1].strip().split()
                        if len(project_info) >= 5:
                            project_data["technologies"] = project_info[:-5]
                            project_data["duration"] = " ".join(project_info[-5:-2])
                            project_data["description"] = project_info[-1]
                            projects.append(project_data.copy())
                else:
                    project_data["description"] = line.strip()
            json_data["projects"] = projects
        elif section == "INTERNSHIP":
            internships = []
            internship_data = {}
            for line in lines:
                if "|" in line:
                    internship_parts = line.split("|")
                    if len(internship_parts) > 1:
                        internship_data["company"] = internship_parts[0].strip()
                        internship_info = internship_parts[1].strip().split()
                        if len(internship_info) >= 5:
                            internship_data["position"] = internship_info[:-5]
                            internship_data["duration"] = " ".join(internship_info[-5:-2])
                            internship_data["description"] = internship_info[-1]
                            internships.append(internship_data.copy())
                else:
                    internship_data["description"] = line.strip()
        elif section == "TECHNICAL SKILLS":
            technical_skills = {}
            skills_data = lines[0].split("Developer  Tools:")
            if len(skills_data) > 1:
                technical_skills["languages"] = skills_data[0].strip().split(":")[1].strip().split(",")
                technical_skills["developer_tools"] = skills_data[1].strip().split(",")
            technologies_frameworks_match = re.search(r"Technologies/Frameworks:([\w\s,]+)", lines[1])
            if technologies_frameworks_match:
                technical_skills["technologies_frameworks"] = technologies_frameworks_match.group(1).strip().split(",")
            json_data["technical_skills"] = technical_skills
        elif section == "CO/EXTRA-CURRICULAR ACTIVITIES":
            activities = []
            activity_data = {}
            for line in lines:
                if "|" in line:
                    activity_parts = line.split("|")
                    if len(activity_parts) > 1:
                        activity_data["organization"] = activity_parts[0].strip()
                        activity_info = activity_parts[1].strip().split()
                        if len(activity_info) >= 5:
                            activity_data["position"] = activity_info[:-5]
                            activity_data["location"] = activity_info[-4]
                            activity_data["duration"] = " ".join(activity_info[-3:-1])
                            activity_data["description"] = activity_info[-1]
                            activities.append(activity_data.copy())
                else:
                    activity_data["description"] = line.strip()
            json_data["co_curricular_activities"] = activities
        elif section == "CERTIFICATIONS":
            certifications = []
            for line in lines:
                if line:
                    certifications.append(line.strip())
            json_data["certifications"] = certifications

    return json_data

extracted_text = extract_text_from_pdf(pdf_file_path)

if extracted_text:
    # Replace bullet points with newlines
    text_with_newlines = replace_bullet_points(extracted_text)

    # Convert the text into a structured JSON object
    structured_json = text_to_json(text_with_newlines)

    # Print the JSON object
    print(json.dumps(structured_json, indent=2))
else:
    print("Extraction failed.")
