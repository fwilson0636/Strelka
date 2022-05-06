# Strelka
Senior Capstone Project

This project is in partnership with Target to provide their analyst with a Strelka JPEG Scanner. 
The scanner allows the analyst to scan and parse a JPEG image file for malicious metadata and output it in a JSON format.
After the scanner is integrated into Target platforms, it has the ability to alert the analyst if the image may be malicous and needs further analysis.
The API for this project serves as a mock visual aid for how the Target platforms use the scanner in its script form.

# Prerequisites
 >&gt;= Python3.9

 _This code was only tested with Python3.9_

# Install Libraries 
#### Upgrade pip
``` python3 -m pip install --upgrade pip ```

You may install the libraries globally or only for this project. 
Choose between global and local install. 
### Global Install
`pip install -r requirements.txt`
### Local Install
```angular2html
# Inside of project directory
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
# Run the Project
`uvicorn app:app --reload`
