import sys
from pygments import highlight
from pygments.formatters import RawTokenFormatter
from pygments.lexers import guess_lexer
from database import Database

path_to_file = 'tttt.txt'

formatter = RawTokenFormatter()
max_percentage = 0.85

def check_file(path_to_file : str, db : Database):
    with open(path_to_file) as f:
        contents = f.read()

        try:
            lexer = guess_lexer(contents)
        except:
            print("Provided file could not be parsed")

        result = highlight(contents, lexer, formatter).decode("utf8").split(sep='\'')
        result = [result[i] for i in range(len(result)) if i%2 == 1]
        result = set(result)
        #in result we have all the unique tokens

        max_tokens_number = max_percentage * len(result)
        files_counter = {}

        for token in result:
            token_files = db.get_token_files(token) or []
            token_files = list(token_files)
            if token_files == []:
                continue
            files = token_files[0]
            for file in files:
                if file not in files_counter:
                    files_counter.update({file: 0})
                else:
                    files_counter[file] += 1

        for file in files_counter:
            if files_counter[file] >= max_tokens_number:
                print("file " + file + " seems to have plagiarism")


db = Database()
db.connect_database()
check_file(path_to_file, db)
db.close()