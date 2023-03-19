# Check plagiarism in repository service

This service allows to index repositories and then check plain text for plagiarism

## How to start

First of all, you need to start the database. You can use the following command:
```
sudo docker run -d --name postgres-container -p 5435:5432 \
-e POSTGRES_USER=postgres  \
-e POSTGRES_HOST_AUTH_METHOD=trust \
postgres
```

Then you need to index your repositories locally. Run the following command:

```
python3 python_scripts/index.py $DIR <repository urls>
```

where $DIR is the path to directory where the repos would upload and <repository urls> 
is the list of your repository urls

For example:

```
python3 python_scripts/index.py repos https://github.com/polupanovaanna/jetbrains-test-task-LLM \
https://github.com/JetBrains/teamcity-git 
```

After indexing the repositories you can start web service to analyze code by running the command

```
./gradlew bootRun
```

then you can achieve the service by url http://localhost:8080/check

There you will see the following form:

![img.png](img.png)

There you can put plain text in any programming language and check whether it parts could be found in indexed repositories

## Run tests

To run tests you need to run the command:

```
python3 python_scripts/tests.py
```

## Another links

[Ideas how to improve this solution](./project_analyze.md)