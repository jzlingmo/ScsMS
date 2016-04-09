编码问题可在目录D:\bin\Python27\Lib\site-packages下增加文件sitecustomize.py改变系统默认编码方式(默认为ASCII)
sitecustomize.py:[
# encoding=utf8  
import sys  
  
reload(sys)  
sys.setdefaultencoding('GBK') 
]