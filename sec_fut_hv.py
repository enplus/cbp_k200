import time
from pprint import pprint
import win32com.client
import numpy as np
from scipy import stats

g_objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
g_stdev = 22
# g_stdev = 18
# g_stdev = 22  # default) 영업일기준
g_sqrt = 252/1.5  # 168
g_scrcnt = 150  # 출력 일자갯수

rqdatacnt = 180

underlying_list = [
    'U141',
    'U148',
    'U146',
    'U132',
    'U147',
    'U144',
    'U145',
    'U142',
    'U143',
    'U133',
    'U192',
    'U193',
    # 'U565',
    # 'U545',
]

# underlying_list = ['A005930']


# usage
# implied_vol('c', 0.3, 3, 3, 0.032, 30.0/365, 0.01)

def bsm_price(option_type, sigma, s, k, r, T, q):
    # calculate the bsm price of European call and put options
    sigma = float(sigma)
    d1 = (np.log(s / k) + (r - q + sigma ** 2 * 0.5) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'c':
        price = np.exp(-r*T) * (s * np.exp((r - q)*T) * stats.norm.cdf(d1) - k *  stats.norm.cdf(d2))
        return price
    elif option_type == 'p':
        price = np.exp(-r*T) * (k * stats.norm.cdf(-d2) - s * np.exp((r - q)*T) *  stats.norm.cdf(-d1))
        return price
    else:
        print('No such option type %s') % option_type


def implied_vol(option_type, option_price, s, k, r, T, q):
    # apply bisection method to get the implied volatility by solving the BSM function
    precision = 0.00001
    upper_vol = 500.0
    max_vol = 500.0
    min_vol = 0.0001
    lower_vol = 0.0001
    iteration = 0

    while 1:
        iteration += 1
        mid_vol = (upper_vol + lower_vol)/2.0
        price = bsm_price(option_type, mid_vol, s, k, r, T, q)
        if option_type == 'c':

            lower_price = bsm_price(option_type, lower_vol, s, k, r, T, q)
            if (lower_price - option_price) * (price - option_price) > 0:
                lower_vol = mid_vol
            else:
                upper_vol = mid_vol
            if abs(price - option_price) < precision:
                break
            if mid_vol > max_vol - 5 :
                mid_vol = 0.000001
                break

        elif option_type == 'p':
            upper_price = bsm_price(option_type, upper_vol, s, k, r, T, q)

            if (upper_price - option_price) * (price - option_price) > 0:
                upper_vol = mid_vol
            else:
                lower_vol = mid_vol
            if abs(price - option_price) < precision:
                break
            if iteration > 50:
                break

    return mid_vol


def Request(objStkWeek):
    # 연결 여부 체크

    # 값
    obj.BlockRequest()

    # 현재가 통신 및 통신 에러 처리
    rqStatus = obj.GetDibStatus()
    rqRet = obj.GetDibMsg1()

    if rqStatus != 0:
        print("Err! 통신상태:", rqStatus, rqRet)
        return False

    cnt = objStkWeek.GetHeaderValue(3)  # Cnt

    # *. code
    # *. date
    # *. clpr?
    # *. ln_val?
    # *. hv_val?

    data = []

    for x in range(cnt):
        tmp = {}
        tmp['date'] = objStkWeek.GetDataValue(0, x)  # date
        tmp['clpr'] = objStkWeek.GetDataValue(4, x)  # clpr

        # print(objStkWeek.GetHeaderValue(0), tmp)

        data.append(tmp)
    return data


if __name__ == "__main__":
    objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
    bConnect = objCpCybos.IsConnect

    if bConnect == 0:
        print("PLUS가 정상적으로 연결되지 않음. ")
        exit()

    result = {}
    result_hv = []

    for uCode in underlying_list:
        cnt = 0

        obj = win32com.client.Dispatch("dscbo1.CbGraph1")
        obj.SetInputValue(0, uCode)
        obj.SetInputValue(1, ord('D'))
        obj.SetInputValue(3, rqdatacnt)
        # obj.SetInputValue(4, ord('0'))
        data = Request(obj)
        rslt1 = []
        rslt1.extend(data)

        name = g_objCodeMgr.CodeToName(uCode)

        while obj.Continue:
            cnt += 1
            rslt1.extend(Request(obj))

            if cnt > 5:
                break

        result[name] = rslt1

    for nm in result.keys():
        lst_ln = []
        for inx, data in enumerate(result[nm][:-1]):
            ln_val = np.log(result[nm][inx]['clpr'] / result[nm][inx+1]['clpr'])
            result[nm][inx]['ln'] = ln_val

            lst_ln.append(ln_val)

        for jnx in range(len(lst_ln)):
            if jnx + g_stdev > len(lst_ln):
                break
            hv = np.std(lst_ln[jnx:jnx+g_stdev]) * np.sqrt(g_sqrt)
            hv = round(hv * 100, 3)
            result[nm][jnx]['hv'] = hv
            # result_hv[nm][jnx]['hv'] = hv
            # pprint(result_hv[nm][:5])

    # 결과 출력.
    ttt = list(result.keys())

    print('         %-5s %-5s %-5s %-7s %-5s %-6s %-5s %-5s %-5s %-9s %-4s %-4s'
          % (ttt[0], ttt[1], ttt[2], ttt[3], ttt[4], ttt[5], ttt[6], ttt[7],
             ttt[8], ttt[9], ttt[10], ttt[11]))

    for inx in range(g_scrcnt):
        print('%s)  %.2f%%     %.2f%%    %.2f%%     %.2f%%     %.2f%%     %.2f%%     %.2f%%   %.2f%%     %.2f%%     %.2f%%     %.2f%%    %.2f%%' % (
            result[ttt[0]][inx]['date'],
            result[ttt[0]][inx]['hv'], result[ttt[1]][inx]['hv'],
            result[ttt[2]][inx]['hv'], result[ttt[3]][inx]['hv'],
            result[ttt[4]][inx]['hv'], result[ttt[5]][inx]['hv'],
            result[ttt[6]][inx]['hv'], result[ttt[7]][inx]['hv'],
            result[ttt[8]][inx]['hv'], result[ttt[9]][inx]['hv'],
            result[ttt[10]][inx]['hv'], result[ttt[11]][inx]['hv']))
