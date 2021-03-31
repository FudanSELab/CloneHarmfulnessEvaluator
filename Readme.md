# Clone Harmfulness Evaluator

The clone harmfulness evaluator presented here is related to the paper "Assessing Code Clone Harmfulness: Indicators, Factors, and Counter Measures", published by IEEE in the Proceedings of SANER 2021.

Please feel free to contact Yijian (wuyijian at fudan dot edu dot cn) for the replication package.

The following is a brief intro of the usage.

### Run Evaluator
First, fill in the configuration file - configMaker.properties. 

Second, modify the main script. The parameters of step two and four should be change to the absolute path of the analysed project. The parameters of step seven should be changed to the projectName which is configed in the configMaker.properties.

Then, run the main script.


    ./main.sh   [linux]
    ./mian.ps1  [windows]

### Configuration
Here is a configuration example. 

    #repoPath: the absolute path of the project。 Example：repoPath=/Users/dataset/redis
    #startCommit： start commit id of the project, there is no need to use the first commit。Example： startCommit=ed9b544e10b84cd43348ddfab7068b610a5df1f7
    #endCommit: end commit id of the project。Example： endCommit=324e22accf457edc996971bc97f5474349cd7c4c
    #traceCommit: if the value is 'overall-detection', all the blobfiles will be extracted. If the value is the same with endCommit, only those blobfiles which have the same absolute file with the files in the endCommit revision。Example： traceCommit=324e22accf457edc996971bc97f5474349cd7c4c
    #threadNum: thread number, used for DB insertion。Example： threadNum=10
    #projectName: project name, which is used for DB table name。 Example： projectName=redis, then table name is:MeasureIndex_redis
    #language： the language of the project。 Example：language=c
    #suffix: suffix name the project files，seperated by comma. Example：suffix=c,h
    #ip: ip of the database。 Example：ip=localhost
    #database: database name。 Example：database=code_clone_check
    #username: username of the database. Example：username=root
    #password: password of the database。 Example：password=root
    #sepNum: the size of the token file, 100000000 is suggested. Example：sepNum=200000000
    #keyWordList: key word for extracting bug fix commit message
    #exeName: clone detection script。 Example：exeName=executable_gpu_linux
    #commitInterval: if the value is 1, all the blob files will be extrated. Otherwise, the program extract blob file according the the interval number Example：commitInterval=1
    #extractedPath: specify certain file path which we want to analyse, seperated by comma。 Example：extractedPath=src/
    #blobSnapshotMapResult, Example：blobSnapshotMapResult=../map_result2.txt
    #
    #Fri Sep 25 16:16:51 CST 2020
    password=111111
    threadNum=10
    suffix=c,h
    commitInterval=1
    username=root
    projectName=redisnoStruct
    extractedPath=all
    ip=localhost
    endCommit=324e22accf457edc996971bc97f5474349cd7c4c
    startCommit=ed9b544e10b84cd43348ddfab7068b610a5df1f7
    repoPath=H:\\WinterHolidayTask\\Dataset\\redis
    database=code_clone_check
    urlParams=useSSL\=false&serverTimezone\=Asia/Shanghai&autoReconnect\=true&characterEncoding\=utf-8&allowPublicKeyRetrieval\=true
    keyWordList=bug,fix,fail,problem
    language=c
    traceCommit=overall-detection
    sepNum=100000000
    exeName=executable_gpu_win10.exe
    blobSnapshotMapResult=..\\map_result2.txt

### Running environment

    JDK 1.8 +
    Python 3.5 +
    Mysql 5.6 +

    If you run clone detection on gpu machine, you need install cuda10
