from typing import List
from pygments import highlight
from pygments.formatters import RawTokenFormatter
from pygments.lexers import guess_lexer
from pathlib import Path
from database import Database


max_percentage = 0.85

#here the path are hardcoded
indexing_path = "/home/anna/github_actions_test_project"

formatter = RawTokenFormatter()


def index_local_repo(repo_path: str, db: Database):
    #initializing out local structure
    data = {}

    p = Path(repo_path)
    for x in p.rglob("*"):
        if "/." in str(x):
            continue
  
        with open(x) as f:
            contents = f.read()

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


def index_repos(db: Database):
    db.connect_database()
    db.clear_table()
    db.init_database()
    index_local_repo(indexing_path, db)



#set up
db = Database()
index_repos(db) 
db.close()
