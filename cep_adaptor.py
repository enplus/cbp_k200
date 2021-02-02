# coding: utf-8
#############################################################
import win32com
import win32com.client
import pythoncom
# import new
# import threading
import time


#############################################################
#  CybosPlus  (Request/Response ) 통신 클래스 데코레이터
#
#  사용자 클래스에 com 문자열을 넣어 rq/rp 가 가능한 클래스로
#  만들어준다.
#############################################################

def CpRqRpClass(com_str):
    def ret_decoclass(usr_cls):
        def usrcls_wrap(*args, **kwargs):
            # request , response 메서드를 반드시 만들도록 한다.

            if hasattr(usr_cls, 'request') == False:
                raise Exception('"request" method is not exist in your class')

            if hasattr(usr_cls, 'response') == False:
                raise Exception('"response" method is not exist in your class')

            # 사이보스 플러스의 Req/Res 통신을 사용하기 위한 이벤트 핸들러
            class CpRqRpEventHandler:
                def OnReceived(self):
                    #연결된 유저객체의 response 메서드를 재호출한다.
                    self.usr_obj.response(self.cpobj)

            # 유저클래스를 상속하는 자식클래스를 생성
            class DecoratedCpRqRpClass(usr_cls):
                def __init__(self, itm_cod=None):
                    # 사이보스 Rq/Rp 새로운 이벤트 핸들러를 생성한다.
                    handler = type('CpRqRpEventHandler_%s'%id(self), (CpRqRpEventHandler,), {})

                    # 핸들러에 유저객체와 com객체 연결
                    handler.usr_obj = self
                    handler.cpobj = win32com.client.Dispatch(com_str)
                    win32com.client.WithEvents(handler.cpobj, handler)
                    # 핸들러를 유저객체에 연결
                    self.handler = handler

                    super(self.__class__, self).__init__()

                def request(self):
                    # 유저클래스에서는 request를 정의하여야하며
                    # cpobj 를 인자로 받도록 하여야 한다.
                    super(self.__class__, self).request(self.handler.cpobj)

            return DecoratedCpRqRpClass(*args, **kwargs)
        return usrcls_wrap
    return ret_decoclass

#############################################################
#  CybosPlus  (Subscribe/Publish) 통신 클래스 데코레이터
#
#  사용자 클래스에 com 문자열을 넣어 sub/pub 가 가능한 클래스로
#  만들어준다.
#  Rq/Rp 와 똑같은 처리를 하나 단지 메소드명이 다르다.
#  사용자가 의도적으로 구분을 지어 사용하면 좋을것이다.
#############################################################

def CpSubPubClass(com_str):
    def ret_decoclass(usr_cls):
        def usrcls_wrap(*args, **kwargs):
            # subscribe , publish 메서드를 반드시 만들도록 한다.
            if hasattr(usr_cls, 'subscribe') == False:
                raise Exception('"subscribe" method is not exist in your class')

            if hasattr(usr_cls, 'publish') == False:
                raise Exception('"publish" method is not exist in your class')


            # 사이보스 플러스의 sub/pub 통신을 사용하기 위한 이벤트 핸들러
            class CpSubPubEventHandler:
                def OnReceived(self):
                    #연결된 유저객체의 response 메서드를 재호출한다.
                    self.usr_obj.publish(self.cpobj)

            # 유저클래스를 상속하는 자식클래스를 생성
            # class DecoratedCpSubPubClass(usr_cls):
            class DecoratedCpSubPubClass(usr_cls):
                def __init__(self):

                    # 사이보스 sub/pub 새로운 이벤트 핸들러를 생성한다.
                    handler = type('CpSubPubEventHandler_%s'%id(self), (CpSubPubEventHandler,), {})

                    # 핸들러에 유저객체와 com객체 연결
                    handler.usr_obj = self
                    handler.cpobj = win32com.client.Dispatch(com_str)
                    win32com.client.WithEvents(handler.cpobj, handler)
                    # 핸들러를 유저객체에 연결
                    self.handler = handler

                    super(self.__class__, self).__init__()

                def subscribe(self):
                    # 유저클래스에서는 subscribe 정의하여야하며
                    # cpobj 를 인자로 받도록 하여야 한다.
                    super(self.__class__, self).subscribe(self.handler.cpobj)

                # def __call__(self, *args):
                #     print('in deco)', *args)
                # print(*args, )
                # usr_cls(*args)

            return DecoratedCpSubPubClass(*args, **kwargs)
        return usrcls_wrap
    return ret_decoclass


#############################################################
#
#  Useage:
#      1. request, response 메소드를 지닌 사용자 클래스를 정의 (반드시 object상속할 것)
#      2. 해당 클래스를 CpRqRpClass 데코레이터로 Wrapping
#      3. 데코레이터의 인자는 COM객체 문자열을 넣어준다.
#
#############################################################
if __name__ == '__main__':
    # @CpRqRpClass('dscbo1.StockMst')
    # class DummyClass(object):
    #     def request(self, cpobj):
    #         cpobj.SetInputValue(0, 'A122630')
    #         cpobj.Request()
    #
    #     def response(self, cpobj):
    #         print(cpobj.GetHeaderValue(1))
    #         time.sleep(2)
    #         self.request()
    #
    # @CpRqRpClass('dscbo1.StockMst')
    # class CloneClass(object):
    #     def request(self, cpobj):
    #         cpobj.SetInputValue(0, 'A252670')
    #         cpobj.Request()
    #
    #     def response(self, cpobj):
    #         print(cpobj.GetHeaderValue(1))
    #         time.sleep(2)
    #         self.request()
    #
    # @CpSubPubClass('dscbo1.StockCur')
    # class StkCur:
    #     def __init__(self, itm_cod='A005930'):
    #         self.itm_cod = itm_cod
    #
    #     def subscribe(self, cpobj):
    #         cpobj.SetInputValue(0, self.itm_cod)
    #         cpobj.Subscribe()
    #
    #     def publish(self, cpobj):
    #         print('%s) %s 현재가:%s %s %6s주  '% (
    #             cpobj.GetHeaderValue(18),
    #             cpobj.GetHeaderValue(0),
    #             cpobj.GetHeaderValue(13),
    #             ('매수', '매도')[cpobj.GetHeaderValue(14) - 49],
    #             cpobj.GetHeaderValue(17),
    #         ))
    #
    #
    # a = DummyClass()
    # print(a.__class__)
    # b = CloneClass()
    # print(b.__class__)
    # c = StkCur()
    # print(c.__class__)
    #
    # a.request()
    # time.sleep(0.5)
    # b.request()
    #
    # c.subscribe()

    while True:
        pythoncom.PumpWaitingMessages()
        # time.sleep(0.01)


#########################
# 실행결과
"""
<class '__main__.DecoratedCpRqRpClass'>
<class '__main__.DecoratedCpRqRpClass'>
<class '__main__.DecoratedCpSubPubClass'>
KODEX 레버리지
KODEX 인버스
KODEX 레버리지

Process finished with exit code -1
"""



