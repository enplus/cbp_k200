from pywinauto import application
import time
import os

os.system('taskkill /IM coStarter* /F /T')
os.system('taskkill /IM CpStart* /F /T')
os.system('wmic process where "name like \'%coStarter%\'" call terminate')
os.system('wmic process where "name like \'%CpStart%\'" call terminate')
time.sleep(5)

app = application.Application()
app.start('C:\DAISHIN\CREON\STARTER\coStarter.exe /prj:cp /id:dpdp /pwd:xxxx /pwdcert:xxxxx /autostart')
time.sleep(60)

# pywinauto가 3.7.6, 3.8.1 등의 버전에서는 동작하지 않으므로 3.7.4, 3.8.0, 3.8.2 등 사용
# 한글 깨질때 - Build, Execution, Deployment - Console - Python Console 하단 Starting script
# !chcp 65001
