from typing import List
from pygments import highlight
from pygments.formatters import RawTokenFormatter
from pygments.lexers import guess_lexer
from database import Database
import os
import sys

from git import Repo


formatter = RawTokenFormatter()

#all the repos from the directory would be indexed
def upload_repos(repo_urls: List[str], directory: str):

    for repo_url in repo_urls:
        repo_name = repo_url.split('/')[-1]
        empty_repo = Repo.init(os.path.join(directory, repo_name))
        origin = empty_repo.create_remote("origin", repo_url)
        origin.fetch()
        empty_repo.create_head("master", origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
        origin.pull()


def index_local_repo(repo_path: str, db: Database):
    #initializing out local structure
    data = {}

    for path, subdirs, files in os.walk(repo_path):
        for name in files:
            x = os.path.join(path, name)
            if "/." in str(x) or ".zip" in str(x) or ".xml" in str(x) or ".sh" in str(x) or "git" in str(x):
                continue

            with open(x) as f:
                try:
                   contents = f.read()
                except:
                    continue

                try:
                    lexer = guess_lexer(contents)
                except:
                    print("Provided file could not be parsed")

                result = highlight(contents, lexer, formatter).decode("utf8").split(sep='\'')
                result = [result[i] for i in range(len(result)) if i%2 == 1]
                for token in result:
                    if token not in data:
                        data.update({token: {str(x)}})
                    else:
                        data[token].add(str(x))

    for token in data:
        db.add_to_db(token, list(data[token]))


def index_repos(db: Database, directory: str):
    db.connect_database()
    db.clear_table()
    db.init_database()
    for file in os.listdir(directory):
        d = os.path.join(directory, file)
        if os.path.isdir(d):
            index_local_repo(d, db)


def main():
    #set up
    directory = sys.argv[1]
    repo_urls = sys.argv[2:]

    upload_repos(repo_urls, directory)

    db = Database()
    index_repos(db, directory)

    db.close()

if __name__ ==  '__main__':
    main()
