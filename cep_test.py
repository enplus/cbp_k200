# coding=utf-8
from CpUtil import *
from cep_stk import *
from cep_futopt import *
from cep_processor import *

import pythoncom
import time

# 이벤트 처리기, 이 모듈이 실행될시 할당됨
evntproc = None

###################################################
# Observers : 자신의 키 패턴에 매칭되는 이벤트를 처리함
###################################################
# 체결시 출력
# def cls_echo(serieses, key, dat):
#     print('key:%s, dat:%s'% (key, dat))

if __name__ == "__main__":
    cpUtil = CpCybos()
    cpStk = CpStockCode()

    cpUtil.get_is_connect()

    evntproc = gen_eproc()
    evntproc.start()

    stkList = ['A252670', 'A005930']
    foList = ['101R3', '105R2', '111R2', '120R2']

    # 이벤트 처리기 세팅
    # evntproc = EventProcessor()
    # evntproc.add_observer(['cls_*'], cls_echo)
    # evntproc.add_observer(['ord_*'], ord_echo)
    # evntproc.add_observer(['stk*_A*'], stk_echo)
    # evntproc.add_observer(['fut*_*'], fut_echo)
    # evntproc.add_observer(['opt*_*'], opt_echo)

    # 현재가, 매수매도구분, 순간체결량을 생산
    # stkcur = StkCur('A252670')
    # stkcur.subscribe()

    # Sbpb
    stkbid = StkBid()
    stkbid.setInitData(stkList, evntproc)
    stkbid.subscribe()

    # RqRp
    foMst = FutOptMst()
    foMst.setInitData(foList, evntproc)
    foMst.request()

    # eurex = EurexJpbid()
    # eurex.setInitData('105R2', evntproc)

    # cpStk.code2name('A005930')

    ##############################################
    # WinCOM32 이벤트 생성,
    # sleep time으로 메세지를 펌핑시키므로 비효율적이다.
    # 따라서 이벤트 처리기는 자식 프로세스에서 동작
    ##############################################

    while True:
        pythoncom.PumpWaitingMessages()
        time.sleep(0.0001) # 최소시간간격 (실질환경은 0.015초에 가까울것)