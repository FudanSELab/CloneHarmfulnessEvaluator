2020/09/25 最新华为克隆危害检测 使用说明：
(1)修改配置configMaker.properties
(2)修改clone_group_map3.py文件路径配置，一般情况下只需要修改repo_path。
(3)修改main.ps1 ，一般情况下需要修改echo 'step 2 -> detect'，路径为\\blobInfo\\CC_OUT\\blobs的绝对路径，
step 6 -> detect-snapshot，路径为单版本的文件路径。 step 7中的参数为项目名。