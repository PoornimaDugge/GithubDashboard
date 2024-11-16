import requests
from collections import defaultdict
import os

owner = 'PoornimaDugge'
repo = 'PythonLearning'
token = os.getenv("PAT")

headers = {
    'Authorization':f'token {token}'
}

def get_pull_requests():
    url=f'https://api.github.com/repos/{owner}/{repo}/pulls?state=all'
    response= requests.get(url,headers=headers)
    response.raise_for_status()
    return response.json()

def get_contributors():
    url=f'https://api.github.com/repos/{owner}/{repo}/contributors'
    response= requests.get(url,headers=headers)
    response.raise_for_status()
    return response.json()

def get_comments(pr_number):
    url=f'https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments'
    response= requests.get(url,headers=headers)
    response.raise_for_status()
    return response.json()

def get_file_changes(pr_number):
    url=f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files'
    response= requests.get(url,headers=headers)
    response.raise_for_status()
    return response.json()


def main():
    pull_requests= get_pull_requests()
    contributors= get_contributors()
    
  
    total_prs = len(pull_requests)
    total_contributors= len(contributors)

    comments_by_contributors=defaultdict(int)
    files_changed= defaultdict(int)
    lines_added=defaultdict(int)
    lines_removed= defaultdict(int)

    for pr in pull_requests:
        pr_number=pr['number']
        comments= get_comments(pr_number)
        #print(comments)
        files = get_file_changes(pr_number)
        for comment in comments:
            comments_by_contributors[comment['user']['login']] += 1

        for file in files:
           
            files_changed[pr_number] +=1
            lines_added[pr_number] += file['additions']
            lines_removed[pr_number] += file['deletions']

    print(f'Total pull requests: {total_prs}')
    print(f'Total contributors : {total_contributors}')
    


    print('\nComments by contributor')
    for contributor,count in comments_by_contributors.items():
        print(f'{contributor} : {count}')

    print(f'\nFiles changed in each PR')
    for pr_number,count in files_changed.items():
        print(f'PR {pr_number} : {count} file changed')

    print('\n Lines added and removed in each PR')
    for pr_number in files_changed.keys():
        print(f'PR {pr_number}: added {lines_added[pr_number]} lines, removed {lines_removed[pr_number]} lines')

if __name__ == "__main__":
        main()