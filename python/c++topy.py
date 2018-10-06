# 動的インスタン生成のため
form classes import PoseEstimatorICP
form classes import PointCloudMap
form classes import ScanPointResampler
form classes import ScanPointAnalyser
form classes import RefScanMaker
form classes import PoseFuser

class ScanMatcher2D():

	def __init__(self):
		self.cls1 = globals()[PoseEstimatorICP]
		global estim
		estim = self.cls1()
		self.cls2 = globals()[PointCloudMap]
		global pcmap
		pcmap = self.cls2()
		self.cls3 = globals()[ScanPointResampler]
		global spres
		spres = self.cls3()
		self.cls4 = globals()[ScanPointAnalyser]
		global spana
		spana = self.cls4()
		self.cls5 = globals()[RefScanMaker]
		global rsm
		rsm = self.cls5()
		self.cls6 = globals()[PoseFuser]
		global pfu
		pfu = self.cls6()

		

	# スキャンマッチングの実行
	def matchScan(self, curScan):
		c++
		t = True

		printf("----- ScanMatcher2D: cnt=%d start -----\n", cnt)

  			# spresが設定されていれば、スキャン点間隔を均一化する
  			if spres != nullptr:
				# 動的インスタンスspresの関数呼び出し
    				# spres->resamplePoints(&curScan)
				# pythonでの動的インスタンスの生成(適切な場所へ移動)
				cls = globals()[ScanPointResampler]
				spres = cls()
				spres.resamplePoints(curScan)

			# spanaが設定されていれば、スキャン点の法線を計算する
 			if spana != nullptr:
				# spana->analysePoints(curScan.lps);
				cls = globals()[ScanPointAnalyser]
				spres = cls()
				spres.analysePoints(curScan)

			# 最初のスキャンは単に地図に入れるだけ
			if cnt == 0:
				growMap(curScan, initPose)
    				prevScan = curScan  # 直前スキャンの設定
    				return(t)

	# 現在スキャンを追加して、地図を成長させる
	def growMap(self, SCAN, POSE):
		# リストの生成(適切な場所へ移動)
		# scanG = []
		# lps = []
		# R = [[]*2]*3
		# 先頭に追加 insert(追加する場所, 値)
		lps.insert(0,SCAN.lps)
		R[2] = POSE.Rmat
		tx = POSE.tx
		ty = POSE.ty

		for i in lps.size()
			lp = lps[i]
			if lp.type = ISOLATE
				continue
			x = R[0][0]*lp.x + R[0][1]*lp.y + tx
			y = R[1][0]*lp.x + R[1][1]*lp.y + ty
			nx = R[0][0]*lp.nx + R[0][1]*lp.ny
			ny = R[0][0]*lp.nx + R[0][1]*lp.ny

			mlp(cnt, x, y)
			mlp.setNormal(nx. ny)
			mlp.setType(lp.type)
			scanG.emplace_back(mlp)

		# 多分 __init__ でインスタンス生成
		cls = globals()[PointCloudMap]
		pcmap = cls()
		self.pcmap.addPose(POSE)
		self.pcmap.addPoints(scanG)
		self.pcmap.setLastPose(POSE)
		self.pcmap.setLastScan(SCAN)
		self.pcmap.makeLocalMap()
		
		# 確認用
		printf("ScanMatcher: estPose: tx=%g, ty=%g, th=%g\n", POSE.tx, POSE.ty, POSE.th)

		

				
			
	
		














		
	
				
