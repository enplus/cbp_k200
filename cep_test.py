# coding=utf-8
from cep_adaptor import CpSubPubClass
from cep_adaptor import CpRqRpClass

from CpUtil import *

from cep_processor import *
import pythoncom
import time

# 이벤트 처리기, 이 모듈이 실행될시 할당됨
evntproc = None

###################################################
# Adaptors : 발생한 이벤트를 처리기에 전달하는 역할
#
###################################################
# 주식 호가잔량
@CpSubPubClass('dscbo1.StockJpBid')
class StkBid:
    def __init__(self):
        self.itm_cod = None
        # self.cod_list = None

    def setCodList(self, itm_cod=None):
        self.itm_cod = itm_cod
        print('# STKBID Init: %s' % self.itm_cod)

    def subscribe(self, com_obj):
        if self.itm_cod is None:
            print('itmCode is None')
        else:
            com_obj.Unsubscribe()
            # print('ComObj: %s' % com_obj)
            # print('# STKBID Subc: %s' % self.itm_cod)

            for x in self.itm_cod:
                com_obj.SetInputValue(0, x)
                com_obj.Subscribe()

    def publish(self, com_obj):
        tlist = []
        itm_cod = com_obj.GetHeaderValue(0)
        for i in range(3, 23, 4):
            itm = (
                com_obj.GetHeaderValue(i+0),
                com_obj.GetHeaderValue(i+1),
                com_obj.GetHeaderValue(i+2),
                com_obj.GetHeaderValue(i+3)
            )
            tlist.append(itm)

        # 이벤트 처리기에 전달
        evntproc.push('stkbid_%s' % itm_cod, tlist)


# 주식 현재가
@CpSubPubClass('dscbo1.StockCur')
class StkCur:
    def __init__(self, itm_cod='A005930'):
        print('# STKCUR itm_cod: %s' % itm_cod)
        self.itm_cod = itm_cod

    def subscribe(self, com_obj):
        com_obj.Unsubscribe()
        com_obj.SetInputValue(0, self.itm_cod)
        com_obj.Subscribe()

    def publish(self, com_obj):
        nowpr    = com_obj.GetHeaderValue(13) # 현재가
        sellbuy  = com_obj.GetHeaderValue(14) # 매수매도구분(체결시)
        clsqty   = com_obj.GetHeaderValue(17) # 순간체결수량

        # 이벤트처리기에 전달
        evntproc.push('cls_%s'%(self.itm_cod),(nowpr, chr(sellbuy), clsqty))

###################################################
# Observers : 자신의 키 패턴에 매칭되는 이벤트를 처리함
###################################################
# 체결시 출력
# def cls_echo(serieses, key, dat):
#     print('key:%s, dat:%s'% (key, dat))


if __name__ == "__main__":

    cpCybos = CpCybos()

    print(cpCybos.GetIsConnect())

    # 이벤트 처리기 세팅
    evntproc = EventProcessor()
    # evntproc.add_observer(['cls_*'], cls_echo)
    # evntproc.add_observer(['ord_*'], ord_echo)
    evntproc.add_observer(['stk*_A*'], stk_echo)
    evntproc.add_observer(['fut*_*'], fut_echo)
    evntproc.add_observer(['opt*_*'], opt_echo)
    evntproc.start()

    # 현재가, 매수매도구분, 순간체결량을 생산
    # stkcur1 = StkCur('A252670')
    # stkcur1.subscribe()

    # stkcur2 = StkCur('A114800')
    # stkcur2.subscribe()
    #
    # # 호가잔량 생산
    stkbid = StkBid()
    stkbid.setCodList(['A252670', 'A005930'])
    stkbid.subscribe()

    ##############################################
    # WinCOM32 이벤트 생성,
    # sleep time으로 메세지를 펌핑시키므로 비효율적이다.
    # 따라서 이벤트 처리기는 자식 프로세스에서 동작
    ##############################################

    while True:
        pythoncom.PumpWaitingMessages()
        time.sleep(0.0001) # 최소시간간격 (실질환경은 0.015초에 가까울것)