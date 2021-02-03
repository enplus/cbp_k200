from pywinauto import application
import time
import os
import datetime

# pywinauto가 3.7.6, 3.8.1 등의 버전에서는 동작하지 않으므로 3.7.4, 3.8.0, 3.8.2 등 사용
# 한글 깨질때 - Build, Execution, Deployment - Console - Python Console 하단 Starting script
# !chcp 65001


def conn_creon(pwd):
    os.system('taskkill /IM coStarter* /F /T')
    os.system('taskkill /IM CpStart* /F /T')
    os.system('wmic process where "name like \'%coStarter%\'" call terminate')
    os.system('wmic process where "name like \'%CpStart%\'" call terminate')
    time.sleep(5)

    app = application.Application()
    app.start('C:\DAISHIN\CREON\STARTER\coStarter.exe /prj:cp /id:dpdp /pwd:xxxx /pwdcert:xxxxx /autostart')
    time.sleep(60)


def check_intraday():
    t_now = datetime.now()
    t_9 = t_now.replace(hour=9, minute=0, second=0, microsecond=0)
    t_start = t_now.replace(hour=9, minute=5, second=0, microsecond=0)
    t_sell = t_now.replace(hour=15, minute=15, second=0, microsecond=0)
    t_exit = t_now.replace(hour=15, minute=20, second=0,microsecond=0)
    today = datetime.today().weekday()
    # if today == 5 or today == 6:  # 토요일이나 일요일이면 자동 종료
    #     printlog('Today is', 'Saturday.' if today == 5 else 'Sunday.')
    #     sys.exit(0)
    # if t_9 < t_now < t_start and soldout == False:
    #     soldout = True
    #     sell_all()
    # if t_start < t_now < t_sell :  # AM 09:05 ~ PM 03:15 : 매수
    #     for sym in symbol_list:
    #         if len(bought_list) < target_buy_count:
    #             buy_etf(sym)
    #             time.sleep(1)
    #     if t_now.minute == 30 and 0 <= t_now.second <= 5:
    #         get_stock_balance('ALL')
    #         time.sleep(5)
    # if t_sell < t_now < t_exit:  # PM 03:15 ~ PM 03:20 : 일괄 매도
    #     if sell_all() == True:
    #         dbgout('`sell_all() returned True -> self-destructed!`')
    #         sys.exit(0)
    # if t_exit < t_now:  # PM 03:20 ~ :프로그램 종료
    #     dbgout('`self-destructed!`')
    #     sys.exit(0)