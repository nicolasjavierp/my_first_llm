import os
import requests

from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url:str, mock:bool = False ):
    """
    Scrape info from linkedin profile, manually scrape information from LinkedIn profile
    """
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/nicolasjavierp/acdfc9ea2c9ae7d26940764ff28b3eec/raw/06398e861e4dc086ae6b62cbbd7f03e806c7c96d/eden-marco.json"
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint, params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10
        )
    data = response.json()
    #Cleaning the data to remove empty stings dicts and lists so we reduce the token number for our LLM
    data = {k:v for k,v in data.items() if v not in ([], "","", None) and k not in ["people_also_viewed", "certifications"]}
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
    return data

if __name__ == "__main__":
    print(scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/jonmoser/", mock=True))