# coding=utf-8
from CpUtil import *
from cep_stk import *
from cep_futopt import *
from cep_processor import *

from k200_config import *

import pythoncom
import time

# 이벤트 처리기, 이 모듈이 실행될시 할당됨

evntproc = None
g_sbcnt = 0   # 최대 400건 제한

# global var
g_mmcd = 'R2'
g_cpcybos = CpCybos()
g_cpStk = CpStockCode()

###################################################
# Observers : 자신의 키 패턴에 매칭되는 이벤트를 처리함
###################################################
# 체결시 출력
# def cls_echo(serieses, key, dat):
#     print('key:%s, dat:%s'% (key, dat))

if __name__ == "__main__":

    g_cpcybos.get_is_connect()

    evntproc = gen_eproc()
    evntproc.start()

    StkFutList = ['1' + x[0] + g_mmcd + '000' for x in SFO_INFO]

    etfList = ['A252670', 'A005930']
    undrList = [x[2] for x in SFO_INFO]  # 3번째필드 = 기초자산

    stkList = etfList + undrList

    # 행사가코드 추가 필요
    # optList = ['2' + x[0] + g_mmcd for x in SFO_INFO if x[1] == 1]

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
    stkBid = StkBid()
    stkBid.setInitData(stkList, evntproc)

    stkBid.subscribe()

    # # Sbpb
    # futBid = FutureJpbid()
    # futBid.setInitData(StkFutList, evntproc)
    # futBid.subscribe()

    # futCur = FutureJpbid()

    stkCur = StkCur()
    stkCur.setInitData(stkList, evntproc)
    stkCur.subscribe()

    # eurex = EurexJpbid()
    # eurex.setInitData('105R2', evntproc)

    # g_cpStk.code2name('A005930')

    ##############################################
    # WinCOM32 이벤트 생성,
    # sleep time으로 메세지를 펌핑시키므로 비효율적이다.
    # 따라서 이벤트 처리기는 자식 프로세스에서 동작
    ##############################################

    while True:
        pythoncom.PumpWaitingMessages()
        time.sleep(0.0001) # 최소시간간격 (실질환경은 0.015초에 가까울것)