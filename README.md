# xui_scan
xui弱密码扫描脚本

fofa或微步搜索语法：
`country="JP" && port="54321" && title=="登录"`  <br />
导出数据字段第一列为ip，第二列为端口，其他可忽略，并重命名为：`ip_port.csv` <br />

file_encoding.py查询`ip_port.csv`编码方式 <br />
change_encoding.py更改`ip_port.csv`编码方式 <br />
