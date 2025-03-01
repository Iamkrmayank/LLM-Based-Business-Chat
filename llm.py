'''import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def validate_data(row):
    prompt = f"Verify the following business data:\nName: {row['name']}\nAddress: {row['address']}\nWebsite: {row['website']}\nPhone: {row['phone_number']}\nReviews: {row['reviews']}\nRating: {row['rating']}\nLatitude: {row['latitude']}\nLongitude: {row['longitude']}\nIs this business data correct?"
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": "You are a data validation assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]
    def validate_data(row):
    # Strip column names to remove spaces (if row is a pandas DataFrame row)
    if hasattr(row, 'index'):
        row.index = row.index.str.strip()
    
    prompt = f"""
    Verify the following business data:
    Name: {row.get('name', '')}
    Address: {row.get('address', '')}
    Website: {row.get('website', '')}
    Phone: {row.get('phone_number', '')}
    Reviews: {row.get('reviews', '')}
    Rating: {row.get('rating', '')}
    Latitude: {row.get('latitude', '')}
    Longitude: {row.get('longitude', '')}
    Is this business data correct?
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a data validation assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message["content"]'''


import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def validate_data(data):
    prompt = ""
    if "query" in data:
        prompt = data["query"]
    else:
        # Original Prompt for Business Data Validation
        prompt = f"Verify the following business data:\nName: {data['name']}\nAddress: {data['address']}\nWebsite: {data['website']}\nPhone: {data['phone_number']}\nReviews: {data['reviews']}\nRating: {data['rating']}\nLatitude: {data['latitude']}\nLongitude: {data['longitude']}\nIs this business data correct?"

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a data validation assistant and chatbot."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message["content"]



    


