rm -r  .\blobInfo\CC_OUT
rm -r  .\detect\result
rm -r  .\detect\tokenData
rm -r  .\db\resultFolder
rm -r  .\snapshot\result
rm -r  .\snapshot\tokenData
rm -r  .\map_result2.txt
rm -r  .\cloneEvo\LinkResults
rm -r  .\dangerCheck\result
rm -r  .\dangerCheck\finalResult
rm -r  .\dangerCheck\consistResult
rm -r  .\dangerCheck\extractedJson

java -jar SingleProjConfMaker.jar

echo 'step 1 -> blobInfo'
cd blobInfo
java -jar -Xms16g -Xmx16g CommitBlobMapper.jar > blob.log
cd ..

echo 'step 2 -> detect'
cd detect
java -jar -Xms16g -Xmx16g SACloneDetector.jar H:\\HWCloneHarmfullness\\tool\\CloneHarmfullnessAnalysis-redis-snapshot\\blobInfo\\CC_OUT\\blobs > log.txt
cd ..

echo 'step 3 -> db'
cd db
java -jar -Xms16g -Xmx16g MeasureIndexInsertion.jar > log.txt
cd ..

echo 'step 4 -> detect-snapshot'
cd snapshot
java -jar -Xms16g -Xmx16g SACloneDetector.jar H:\\WinterHolidayTask\\Dataset\\redis > log.txt
cd ..

echo 'step 5 -> clone_group_map'
python clone_group_map3.py

echo 'step 6 -> cloneEvo'
cd cloneEvo
java -jar -Xms16g -Xmx16g CloneEvolution2.jar all > log.txt
cd ..

echo 'step 7 -> dangerCheck'
cd dangerCheck
java -jar -Xms16g -Xmx16g CloneDangerChecker.jar > log.txt
python CodeCloneValidation57.py redis .\result\preCloneGroupInfo.csv
python clone_group_start_end_type-ori.py redis .\finalResult\validation_result_redis.csv
python clone_group_modify_type.py redis
cd ..