## How this solution could be improved

### Technical part

1. There should be a specific database for working with text. I used PostgreSQL,
but there are problems with using it for indexing big repositories because it was
not created for hashing big text parts. There should be key-value storage that is
created for general text storage and search, such as SphinxSearch.
2. In this solution, I used direct call of python scripts from java because
python code was simple and could be easily integrated with java service.
Ideally, there should be a Python microservice that can answer the requests from Java code.

### Algorithmic part

Current algorithmic solution is a very simple approach. There are a few points how it could be improved:

1. The solution is now entirely based on token names. So when the function names and
variable names are changed, it won't work. The simplest idea: look at the places where
the token is stored. When there are different tokens with the same type that are
stored in the same places, then they could be renamed variables. 
Improve this idea: use abstract syntax trees. There also could be a machine-learning
based algorithm, that uses these ideas.
2. It should be stated properly which files should be indexed. I excluded only some technical and XML files.
3. It can be improved by creating different storages for different languages during indexing.
We can recognize the language while parsing text, so we can get the answer faster by looking
at the current language.