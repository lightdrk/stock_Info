import os
import sys
import shutil
import argparse
from colorama import Fore
from dotenv import load_dotenv
from helper.sheet import GSheet
from helper.github import Github
from helper.scrap_trend import Scrap


def store_data():
    ''' for creating and storing credentails'''
    print(Fore.BLUE+f"***** env *****",Fore.GREEN)
    if not os.path.exists('creds/.env'):
        username = input(Fore.CYAN+'Username: '+Fore.GREEN)
        token = input(Fore.CYAN+'Token: '+Fore.GREEN)
        repo = input(Fore.CYAN+'Repository: '+Fore.GREEN)
        sheet = input(Fore.CYAN+'Sheet: '+Fore.GREEN)
        if not os.path.exists('creds'):
            os.mkdir('creds')
        with open('./creds/.env', 'w') as env:
            env.write(f'USERNAME={username}\n')
            env.write(f'TOKEN={token}\n')
            env.write(f'REPO={repo}\n')
            env.write(f'SHEET={sheet}')
    print(Fore.GREEN+'=>valid')

    print(Fore.BLUE+"**** file path ****")
    if not os.path.exists('creds/client_secret.json'):
        client = input(Fore.GREEN+'Client cred (path): ')
        if os.path.exists(client):
            os.rename(client, './creds/client_secret.json')
            print(Fore.GREEN+'Updated')
        else:
            print(Fore.RED+'path issue')
    print(Fore.WHITE)



def main():
    ''' working function'''

    load_dotenv(dotenv_path='./creds/.env')
    username = os.getenv('USERNAME')
    token = os.getenv('TOKEN')
    repo_name = os.getenv('REPO')
    sheet = os.getenv('SHEET')
    google_sheet = GSheet()
    scraper_object = Scrap()
    github = Github(username=username, token=token, repo_name=repo_name)
    #gets access for drive
    #google_sheet.explicity_new_auth()
    google_sheet.auth_user() #authenticate the user
    google_sheet.open_google_sheet(sheet_id=sheet)
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
    parser.add_argument("--new",action='store_true', help="Example: main.py -n|--new ")
    args = parser.parse_args()

    if args.new:
        if os.path.exists('creds/.env') and os.path.exists('creds/client_secret.json'):
            confirm = input(Fore.WHITE+'Do you want to re-create[yes/no](Default : no): ')
            if confirm.casefold() == 'yes':
                shutil.rmtree('creds')
        store_data()

    if not (os.path.exists('creds/client_secret.json') and os.path.exists('creds/.env')):
        print(Fore.RED+'Suggested : use main.py --new for creds generation',Fore.WHITE+'\n use --help')
        sys.exit()
    if os.path.exists('creds/.env') and os.path.exists('creds/client_secret.json'):
        main()


