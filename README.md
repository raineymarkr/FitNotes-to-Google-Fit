# FitNotes-to-Google-Fit

 How To Use

 1) Export FitNotes data as "data.csv", place in script directory
 2) Create New Project in Google's Cloud Console
 3) Enable Fit API
 4) Create Credentials for Desktop Application
 5) Download Secret File, place in script directory
 6) In csv_reader.py, replace 'SECRET_KEY' with the name of your secret key file (ending in .json)
 7) Be aware that I've hardcoded the workouts to fit my general modality, which is generally a 60 minute weight training/powerlifting session. Alter the data object as needed.
 8) Open CMD and type "py csv_reader.py data.csv"
 9) The script will upload 200 dates, wait a minute to avoid caps and continue
