# estimate228

重要更新


- 170226
	- (228.py/estimate228.ipynb) 增加不同版本的SDR 估計，以及對應的228死亡人數推估數（研討會使用crossYearSDR, 為各年份對應月份的男性死亡數加總除以女性死亡數加總；新增meanSDR 估計，為各年份對應月份的SDR 的簡單平均）
	- (228.py/estimate228.ipynb) 增加appendix: 用1947 年其他月份的資料來估計本文推估方法的誤差。

檔案說明：

- 228.py: 228 死亡人數估計計算過程
- cleanCompenData.py: 補償基金會資料清理程式
- cleanCompenData.txt: 清理完成的補償資料
- compensate.txt : 補償基金會資料，由林邑軒整理
- data.txt: 1947, 1949, 1950, 1951 年台灣地區逐月死亡人數按性別分
	- 1947 年資料來源：台灣省政府衛生處，台灣省衛生統計要覽。（見http://tinyurl.com/h778uxz）
	- 1949~1951 年資料來源：台灣省行政長官公署統計室編，台灣省統計要覽。第三冊～第五冊（藏中研院民族所圖書館）
- estimate228.ipynb：228 死亡人數估計過程示範檔（同228.py）
- README.md：你現在看到的檔案

副檔名為 .py/.ipynb 的檔案為使用 python Anaconda 2 Distribution 寫成，使用python 版本 2.7.13。
