import time

real_path_csv_file = '.\\blobInfo\\CC_OUT\\realPath.csv'
blob_measure_index_file = '.\\detect\\result\\MeasureIndex.csv'
blob_clone_group_file = '.\\detect\\result\\type123_method_group_result.csv'
snapshot_measure_index_file = '.\\snapshot\\result\\MeasureIndex.csv'
snapshot_clone_group_file = '.\\snapshot\\result\\type123_method_group_result.csv'
repo_path = 'H:\\WinterHolidayTask\\Dataset\\redis'
cloneSummary_path = '.\\dangerCheck\\result\\preCloneGroupInfo.csv'
output_file = 'map_result2.txt'

blob_id_to_path_dict = dict()
blob_measures = dict()
snapshot_measures = dict()
mapped_groups = dict()
unmapped_groups = dict()
extract_group_set = set()


def init():
	#加载realPath.csv
	f = open(real_path_csv_file, 'r')
	for line in f:
		infos = line.split(',')
		blob_id = infos[0]
		path = infos[1].strip()
		blob_id_to_path_dict[blob_id] = path
	f.close()
	print(len(blob_id_to_path_dict))

	#加载blob多版本的measure index
	blobMeasureId2GroupId = dict()
	group_id = 0
	f = open(blob_clone_group_file, 'r')
	for line in f:
		group_id += 1
		mids = line.strip().split(',')
		for mid in mids:
			blobMeasureId2GroupId[mid] = group_id
	f.close()
	f = open(blob_measure_index_file, 'r')
	for line in f:
		tmp = line.strip().split(',')
		mid = tmp[0]
		abs_path = tmp[1].replace('\\', '/')
		temp = abs_path[:abs_path.rindex('.src')]
		temp = temp.split('/')
		blob_id = temp[-2] + temp[-1]
		path = ''
		if blob_id in blob_id_to_path_dict:
			path = blob_id_to_path_dict[blob_id]
		else:
			path = ''
		if mid in blobMeasureId2GroupId:
			blob_measures[link(path, tmp[2], tmp[3])] = blobMeasureId2GroupId[mid]
		else:
			blob_measures[link(path, tmp[2], tmp[3])] = 0
	f.close()

	#加载snapshot单版本的measure index
	snapshotMeasureId2GroupId = dict()
	group_id = 0
	f = open(snapshot_clone_group_file, 'r')
	for line in f:
		group_id += 1
		unmapped_groups[group_id] = 0
		mids = line.strip().split(',')
		for mid in mids:
			snapshotMeasureId2GroupId[mid] = group_id
	f.close()
	f = open(snapshot_measure_index_file, 'r')
	for line in f:
		tmp = line.strip().split(',')
		mid = tmp[0]
		abs_path = tmp[1].replace('\\', '/')
		path = abs_path[len(repo_path)+1:]
		if mid in snapshotMeasureId2GroupId:
			snapshot_measures[link(path, tmp[2], tmp[3])] = snapshotMeasureId2GroupId[mid]
		else:
			snapshot_measures[link(path, tmp[2], tmp[3])] = 0
	f.close()

	#加载最终分析结果groupId
	# f = open(cloneSummary_path, 'r')
	# for line in f:
	# 	lineArray = line.strip().split(',')
	# 	if(lineArray[0] == "groupId"):
	# 		continue
	# 	extract_group_set.add(lineArray[0])
	# f.close()
		

def process():
	cnt = 0
	size = len(snapshot_measures)
	for measure in snapshot_measures:
		cnt+=1
		print('%.2f%%' % (cnt*100.0/size))
		sgid = snapshot_measures[measure]
		if sgid == 0:
			continue
		if measure in blob_measures:
			bgid = blob_measures[measure]
			key = '%d@%d' % (bgid, sgid)
			if key in mapped_groups:
				continue
			mapped_groups[key] = 0
			if sgid in unmapped_groups:
				del unmapped_groups[sgid]
	

def output():
	f = open(output_file, 'w', encoding='utf8')
	for g in mapped_groups:
		curArr = g.split("@")
		"""
		if(curArr[0] in extract_group_set):
			g = g + " => extracted"
		"""
		f.write(g + '\n')
	f.write('----------------------------\n')
	for g in unmapped_groups:
		f.write(str(g) + '\n')
	f.close()


def link(path, startLine, endLine):
	return '%s@%s@%s' % (path, startLine, endLine)


if __name__ == '__main__':
	time_start = time.process_time()
	print('init...')
	init()
	print('process...')
	process()
	print('output...')
	output()
	time_end = time.process_time()
	print('finish, time cost:%.1f s' % (time_end - time_start))

