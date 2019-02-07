from time import sleep
import pandas as pd
from collections import OrderedDict
from time import sleep
import pandas as pd
try:
    from jqdatasdk import *
except ImportError:
    pass
import baostock as bs
from DyCommon.DyCommon import *
from ...Common.DyStockCommon import *


class DyStockDataJQData(object):
    """ JQData数据接口 """

    def __init__(self, info):
        self._info = info

    def getDays(self, code, startDate, endDate, fields, name=None):
        """
            @return: df['datetime', indicators]
                     None - errors
                     [] - no data
        """
        JQcode = normalize_code(code)
        # 默认取所有字段
        fields_ = ['open', 'close', 'low', 'high', 'volume', 'money', 'factor', 'high_limit','low_limit', 'avg', 'pre_close', 'paused']
        fields__ = 'date,turn,tradestatus,pctChg,isST'
        retry = 3
        for _ in range(retry):
            try:
                # JQ日数据
                JQDf = get_price(JQcode, start_date=startDate, end_date=endDate, frequency='daily', fields=fields_, fq='post')

                # 从baosotck获取turn等数据
                rs = bs.query_history_k_data_plus(code, fields__, start_date=startDate, end_date=endDate, frequency="d",
                                                  adjustflag="3")
                data_list = []
                while (rs.error_code == '0') & rs.next():
                    # 获取一条记录，将记录合并在一起
                    data_list.append(rs.get_row_data())
                bsDf = pd.DataFrame(data_list, columns=rs.fields)
                bsDf = bsDf.set_index('date')
                break
            except Exception as ex:
                lastEx = ex
                print("{}({})JQ或者baostock异常[{}, {}]: {}, retrying...".format(code, name, startDate, endDate, ex))
                sleep(1)
        else:
            self._info.print(
                "{}({})JQ或者baostock异常[{}, {}]: {}, retried {} times".format(code, name, startDate, endDate, lastEx,
                                                                          retry), DyLogData.error)
            return None

        # 清洗数据
        JQDf = JQDf.dropna(axis=0) #去掉空行
        df = JQDf.join(bsDf)
        df = df.dropna(axis=0)
        if df.isnull().sum().sum() > 0:
            print("{}({})JQ有些数据缺失[{}, {}]".format(code, name, startDate, endDate))
            print(df[df.isnull().any(axis=1)])

            self._info.print("{}({})JQ有些数据缺失[{}, {}]".format(code, name, startDate, endDate),
                                 DyLogData.warning)
            return None

        # change to Wind's indicators
        df = df.sort_index()
        df.index.name = 'datetime'
        df.reset_index(inplace=True)  # 把时间索引转成列
        df.rename(columns={'money': 'amt', 'factor': 'adjfactor'},
                      inplace=True)

        # select according @fields
        #df = df[['datetime'] + fields]

        return df

    def _login(self):
        self._info.print("登录JQData...")

        try:
            auth('13701159730', '159730')
            self._info.print("登录JQData成功")
            lg = bs.login()
            # 显示登陆返回信息
            self._info.print('login respond error_code:' + lg.error_code)
            self._info.print('login respond  error_msg:' + lg.error_msg)
            return True

        except Exception as e:
            self._info.print("登录JQData失败: ErrorCode={}, Data={}".format('', e), DyLogData.error)
            return False


    def getTradeDays(self, startDate, endDate):
        if not self._login():
            return None

        self._info.print("开始从JQData获取交易日数据[{}, {}]...".format(startDate, endDate))

        data = get_trade_days(start_date=startDate, end_date=endDate)
        data = data.tolist()
        return [x.strftime('%Y-%m-%d') for x in data]

    def getStockCodes(self):
        if not self._login():
            return None

        self._info.print("开始从JQData获取股票代码表...")

        code = get_all_securities()

        code.index.name = 'code'
        code.reset_index(inplace=True)  # 把索引转成列
        code.rename(columns={'name': 'pinyin_name', 'display_name': 'name'},
                    inplace=True)
        code['code'] = code['code'].str.replace('XSHE', 'SZ')
        code['code'] = code['code'].str.replace('XSHG', 'SH')
        codes = {}
        for code, name in zip(code.code, code.name):
            codes[code] = name

        self._info.print("从JQData获取股票代码表成功")
        return codes

    def getSectorStockCodes(self, sectorCode, startDate, endDate):
        if not self._login():
            return None

        self._info.print("开始从JQData获取[{0}]股票代码表[{1}, {2}]...".format(DyStockCommon.sectors[sectorCode], startDate, endDate))

        dates = DyTime.getDates(startDate, endDate)

        progress = DyProgress(self._info)
        progress.init(len(dates))
        JQcode = normalize_code(sectorCode)

        codesDict = OrderedDict() # {date: {code: name}}
        for date_ in dates:
            date = date_.strftime("%Y%m%d")
            date_ = date_.strftime("%Y-%m-%d")

            data = get_index_weights(index_id=JQcode,date=date_)
            data.reset_index(inplace=True)  # 把时间索引转成列
            data['code'] = data['code'].str.replace('XSHE', 'SZ')
            data['code'] = data['code'].str.replace('XSHG', 'SH')
            data.rename(columns={'display_name': 'name'},
                        inplace=True)

            codes = {}
            for code, name in zip(data.code, data.name):
                codes[code] = name

            codesDict[date_] = codes

            progress.update()

        self._info.print("从JQData获取[{0}]股票代码表[{1}, {2}]完成".format(DyStockCommon.sectors[sectorCode], startDate, endDate))

        return codesDict

