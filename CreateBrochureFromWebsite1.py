import json
from openai import OpenAI

from Website import Website

OPEN_AI_URL= "http://localhost:11434/v1"
OPEN_AI_MODEL= "llama3.2"
COM_NAME="Anthropic"
COM_URL="https://anthropic.com"
openai = OpenAI(api_key="ollama", base_url=OPEN_AI_URL)

LINK_SYSTEM_PROMPT = "You are provided with a list of links found on a webpage.\
You are able to decide which of the link would be most relevant to include in brochure about the company \
such as links to About page or career/jobs page or company page \n"
LINK_SYSTEM_PROMPT += """
{
 "links" : [{"type": "About Page", "url": "https://fullurl/About"}, {"type": "Career Page", "url": "https://another.fulllurl/careerr"}]
}
"""

def get_website_link_user_prompt(website):
    link_user_prompt = f"Website Title is {website.title} \n"
    link_user_prompt += f"Here is the list of all the links found in the website {website.title} - \
Please go through all the links & respond with the links which are relevant to include in company brochure.\
Respond in json format with complete https url only & dont include email, privacy links or other non relevant links"
    link_user_prompt += "\n".join(website.links)
    return link_user_prompt

def get_website_links(url):
    website = Website(url)
    resp = openai.chat.completions.create(messages=[
        {"role": "system", "content": LINK_SYSTEM_PROMPT},
        {"role": "user", "content": get_website_link_user_prompt(website)}
    ], model= OPEN_AI_MODEL, response_format={"type": "json_object"})
    return json.loads(resp.choices[0].message.content)

def get_all_details(url):
    website = Website(url)
    result = f"Landing Page: \n"
    result += website.getContent()
    links = get_website_links(url)
    print("Links found: ", links)
    for link in links['links']:
        result += f"\n \n {link['type']}\n"
        result += Website(link['url']).getContent()
        result += "\n \n"
    return result

BROCHURE_SYSTEM_PROMPT = "You are provided a company Website landing page & other relevant pages contents \
Analyze all deeply & write an informative brochure for company advertisement. \
Make sure to include all important information about the company, its customer prospective, its locations, job/career & other relevant information \
attributed to company.Do not include any private and terms & services related stuff which is not relevant for brochure. Please provide \
all information in markdown"

def get_brochure_user_prompt(companyname, url):
    brochure_user_prompt = f"You are looking at a company called {companyname}. Below are its landing & other relevant pages contents.\
Please go through all of them & create a brochure describing well about the company, in markdown \n"
    brochure_user_prompt += get_all_details(url)
    return brochure_user_prompt

def create_brochure(companyname, url):
    brochureresponse = openai.chat.completions.create(model=OPEN_AI_MODEL, messages=[{"role":"system", "content":BROCHURE_SYSTEM_PROMPT},
                                                                {"role":"user", "content":get_brochure_user_prompt(companyname, url)}
                                                                ]
                                                      )
    return brochureresponse.choices[0].message.content

#print(LINK_SYSTEM_PROMPT)
#print(get_website_link_user_prompt(Website(COM_URL)))
#print(get_website_links(COM_URL))
#print(get_all_details(COM_URL))
print(create_brochure(COM_NAME, COM_URL))