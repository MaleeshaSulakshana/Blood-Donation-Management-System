import re
import os
import random
from datetime import datetime


# For validate email
def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        return True

    else:
        return False


# Function for get current date
def date_picker():
    current_datetime = datetime.now()
    date = str(current_datetime.strftime("%Y-%m-%d"))
    return date


# Function for get current date
def date_picker_no_space():
    current_datetime = datetime.now()
    date = str(current_datetime.strftime("%Y%m%d"))
    return date


# Function for genarate random number
def random_number():
    rand_no = str(random.randint(100000, 999999))
    return rand_no


# Function for genarate random number
def random_number_with_date():
    date = date_picker_no_space()
    rand_no = random_number()
    new_rand_no = str(date) + str(rand_no)

    return new_rand_no


# Function for save deseases images
def file_save(image, save_folder, image_name):
    if image != None:
        file_name = image.filename
        extension = os.path.splitext(file_name)[1]
        save_file_name = image_name + "." + extension
        image.save(save_folder + save_file_name)

    else:
        save_file_name = None
        extension = None

    return str(save_file_name), str(extension)
