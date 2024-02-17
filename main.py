import os
import argparse
from colorama import Fore
from dotenv import load_dotenv
from helper.sheet import GSheet
from helper.github import Github
from helper.scrap_trend import Scrap


def store_data():
    ''' for creating and storing credentails'''
    print(f"***** env *****")
    username = input('Username: ')
    token = input('Token: ')
    repo = input('Repository: ')
    print("**** file path ****")
    client = input('Client location: ')
    with open('./creds/.env', 'w') as env:
        env.write(f'USERNAME={username}\n')
        env.write(f'TOKEN={token}\n')
        env.write(f'Repository={repo}\n')

    if os.path.exists(client):
        os.rename(client, './creds/client_secret.json')

    print(Fore.GREEN+'Updated')
    print(Fore.WHITE)



def main():
    ''' working function'''

    load_dotenv(dotenv_path='./creds/.env')
    username = os.getenv('USERNAME')
    token = os.getenv('TOKEN')
    repo_name = os.getenv('REPO')
    google_sheet = GSheet()
    scraper_object = Scrap()
    github = Github(username=username, token=token, repo_name=repo_name)
    #gets access for drive
    #google_sheet.explicity_new_auth()
    google_sheet.auth_user() #authenticate the user
    google_sheet.open_google_sheet(sheet_id="1PKDskq94WwKit6KmVFyop1fZ2yi0eHQoAVYOg7k6JpI")
    scrap_names = google_sheet.fetch_name(worksheet=0,column=1)
    print(scrap_names)
    data_pass_google_sheet = [] # list of retived data
    image_names = [] #names of the screenshot
    cycle = {0:'15 MINUTES', 1:'DAILY', 2:'WEEKLY', 3:'MONTHLY'}

    # scraps data form the site , appends image names and data to the above variables
    for i in scrap_names[1:]:
        is_avilable = google_sheet.is_worksheet(i)
        # check if is worksheet
        if is_avilable:
            google_sheet.worksheet_create(i)

        data_out = scraper_object.retrive(i)
        if (len(data_out) > 1):
            for x in range(0,3):
                path = f'image_output/{i}{x}.png'
                github.update_image_in_github(path,path)
                image_names.append(f'{i}{x}.png')
                google_sheet.open_worksheet(i)
                google_sheet.update_cells(f"A{x+1}",f"{cycle[x]}")
                google_sheet.update_img_cells(f"B{x+1}",f"{i}{x}.png")
                print(f'{i}{x}.png')
        data_pass_google_sheet.append(data_out)

    #exit from the brower
    scraper_object.exit()
    print(data_pass_google_sheet)
    #print(data_pass_google_sheet)
if __name__ == "__main__":
    usage='''%(prog)s <command> [options]
    Commands:
    1. --help | -h
    2. --new | -n
    '''
    parser = argparse.ArgumentParser(prog="", usage=usage)
    parser.add_argument("new", nargs="?", help="Example: main.py -n|--new ")
    args = parser.parse_args()

    if args.new:
        store_data()
    #main()


#TODO: gui ? / getting details
