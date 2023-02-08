# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 10:49:49 2022

@author: Gridery
"""
import datetime
import pandas as pd
import requests
from lxml.html import etree
import numpy as np

"""
首页格式 http://quotes.money.163.com/[市][股票代码].html#01a02 用于获取所属板块、股票名称、股票代码 深圳1 上海0
历史交易数据格式 http://quotes.money.163.com/trade/lsjysj_[股票代码].html?year=[年份]&season=[季度] 用于获取历史股价
（年度）主要财务指标格式 http://quotes.money.163.com/f10/zycwzb_[股票代码],year.html 用于获取每股收益、总负债、总资产
（年度）财务报表摘要 http://quotes.money.163.com/f10/cwbbzy_[股票代码].html?type=year 用于获取股东权益
内部持股格式 http://quotes.money.163.com/f10/nbcg_[股票代码].html#01d04
分红配股格式 http://quotes.money.163.com/f10/fhpg_[股票代码].html#01d05 用于获支付与否、支付方式、每股股利
公司资料格式 http://quotes.money.163.com/f10/gszl_[股票代码].html#01f02 用于获取上市日期
"""

"""
输出格式：
# 股票名
# 股票代码
# 所属板块
# 年份
# 当期每股收益
# 当期股价
# 当期市盈率
# 内部持股变化
# 股利支付与否 （0：未支付 1：已支付）
# 股利支付方式 （0：股票股利 1：现金股利）
# 每股现金股利
# 每股股票股利
# 股利支付率 （每股股利/每股收益）
# CAR
# ROE （净利润/股东权益）
# 负债率 （总负债/总资产）
# 周转率（营业收入/总资产）
# 保值增值率（期末股东权益/期初股东权益）
# 总资产
"""

"""
沪市主板代码 600、601、603、605
深市主板代码 000
"""

# 获取所有2005年前上市的公司股票代码
"""
使用网站 https://s.askci.com/stock/a/0-0?reportTime=2022-09-30&endTime=2005-01-01&pageNum=[页数]#QueryCondition

stock_code = []
for i in range(1,3):
    URL = f'https://s.askci.com/stock/a/0-0?reportTime=2022-09-30&endTime=2005-01-01&pageNum={i}#QueryCondition'
    tmp_stock_code = pd.read_html(URL)[3].iloc[:,1].to_list()
    temp = []
    for j in tmp_stock_code:
        temp_j = str(j)
        if len(temp_j)!=6:
            temp_j = '0'*(6-len(temp_j))+temp_j
        temp.append(temp_j)
    stock_code.extend(temp)
"""

session = requests.Session()
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35'}
def stock_exist(stc:str):
    # 检查公司所属市场+是否存在
    if stc[0] == '0':
        stock_market = 1 #深市
    elif stc[0] == '6':
        stock_market = 0 #沪市
    else:
        return False
    URL = f'http://quotes.money.163.com/{stock_market}{stc}.html#01a02'
    stock_profile = session.get(URL, headers = headers)
    stock_status = stock_profile.status_code
    if stock_status != 404:
        return True, stock_market, stock_profile
    else:
        return False


def stock_data(stc:str,Y:int):
    stc=str(stc)
    exist = stock_exist(stc)
    if exist:
        stock_profile = exist[2]
        stock_xml = etree.HTML(stock_profile.content.decode('UTF-8'))
        stock_name = stock_xml.xpath('/html/body/div[2]/div[2]/ul/li[1]/a/strong/text()') #股票名称
        stock_code = stc #股票代码
        stock_type = stock_xml.xpath('/html/body/div[2]/div[5]/div[5]/ul/li[1]/a/text()') #股票板块
        stock_zycwzb_title = pd.read_html(f'http://quotes.money.163.com/f10/zycwzb_{stc},year.html')[3] #主要财务指标表头
        stock_zycwzb = pd.read_html(f'http://quotes.money.163.com/f10/zycwzb_{stc},year.html')[4] #主要财务指标
        stock_cwbbzy_title = pd.read_html(f'http://quotes.money.163.com/f10/cwbbzy_{stc}.html?type=year')[3] #财务报表摘要表头
        stock_cwbbzy = pd.read_html(f'http://quotes.money.163.com/f10/cwbbzy_{stc}.html?type=year')[4] #财务报表摘要
        
        stock_nbcg = pd.read_html(f'http://quotes.money.163.com/f10/nbcg_{stc}.html#01d04')[4] #高管持股变动
        stock_nbcg['变动日期'] = pd.to_datetime(stock_nbcg['变动日期'])
        stock_fhpg = pd.read_html(f'http://quotes.money.163.com/f10/fhpg_{stc}.html#01d05')[3] # 分红配股
        stock_fhpg['公告日期'] = pd.to_datetime(stock_fhpg['公告日期']['公告日期'])                
        stock_pgyl = pd.read_html(f'http://quotes.money.163.com/f10/fhpg_{stc}.html#01d05')[4] # 配股一览
        for year in [Y]:
            """
            计算当期市盈率
            """
            ave_stock_price = pd.read_html(f'http://quotes.money.163.com/trade/lsjysj_{stc}.html?year={year}&season=4')[3]['开盘价'].mean() #当期股价
            eps = stock_zycwzb.iloc[0,:][f'{year}-12-31'] #每股收益
            if eps != '--':
                eps = float(eps)
                pe = eps/ave_stock_price #市盈率
            else:
                eps = np.nan
                pe = np.nan #市盈率
            
            """
            计算该年内部持股变动
            """
            s_date = datetime.datetime.strptime(f'{year}-01-01', '%Y-%m-%d').date()
            e_date = datetime.datetime.strptime(f'{year}-12-31', '%Y-%m-%d').date()
            
            stock_nbcg_year = stock_nbcg[(stock_nbcg['变动日期'].dt.date >= s_date) & (stock_nbcg['变动日期'].dt.date <= e_date)]
            stock_nbcg_change = stock_nbcg_year.iloc[:,4].sum() #内部持股变化
            
            """
            该年分红方案、计算分红比例
            """
            
            stock_fhpg_year = stock_fhpg[(stock_fhpg['公告日期']['公告日期'].dt.date >= s_date) & (stock_fhpg['公告日期']['公告日期'].dt.date <= e_date)]
            stock_fhpgfa = stock_fhpg_year['分红方案（每10股）'].sum()
            stock_if_div = 1
            stock_cash_div = np.nan
            stock_share_div = np.nan
            stock_div_method = np.nan
            stock_cash_div_rate = np.nan
            if stock_fhpgfa.sum().sum() == 0.0:
                stock_if_div = 0 #未分红
            else:
                stock_cash_div = stock_fhpgfa['派息']/10 #每股派息
                stock_if_cash = bool(stock_cash_div)
                stock_share_div = stock_fhpgfa['送股']/10 #每股配股
                stock_if_share = bool(stock_share_div)
                if stock_if_cash==True and stock_if_share==False:
                    stock_div_method = 1
                    stock_cash_div_rate = stock_cash_div/eps #现金股利支付率
                elif stock_if_cash==False and stock_if_share==True:
                    stock_div_method = 2
                elif stock_if_cash and stock_if_share:
                    stock_div_method = 3 #分红方法
                    stock_cash_div_rate = stock_cash_div/float(eps) #现金股利支付率
            
            """
            计算累计超额收益率CAR
            """
            stock_price = pd.read_html(f'http://quotes.money.163.com/trade/lsjysj_{stc}.html?year={year}&season=4')[3][['开盘价']].iloc[:10,:].values
            real_rate=[]
            for i in range(len(stock_price)-1): #开盘价=i[0]
                real_rate.append((stock_price[i]-stock_price[i+1])/stock_price[i+1])
                
            """
            计算ROE
            """
            stock_cwbbzy_year = stock_cwbbzy[f'{year}-12-31']
            stock_ROE = float(stock_cwbbzy_year.iloc[6])/float(stock_cwbbzy_year.iloc[18])
            
            """
            计算负债率
            """
            stock_zycwzb_year = stock_zycwzb[f'{year}-12-31']
            stock_LEV = float(stock_zycwzb_year.iloc[15])/float(stock_zycwzb_year.iloc[13])
            
            """
            计算周转率
            """
            stock_T = float(stock_zycwzb_year.iloc[3])/float(stock_zycwzb_year.iloc[13])
            
            stock_info={'股票名':[str(stock_name.pop())],
                    '股票代码':[stock_code],
                    '所属板块':[str(stock_type.pop())],
                    '年份':[year],
                    '当期市盈率':[pe],
                    '内部持股变化':[stock_nbcg_change],
                    '股利支付与否 （0：未支付 1：已支付）':[stock_if_div],
                    '股利支付方式 （0：股票股利 1：现金股利）':[stock_div_method],
                    '每股现金股利':[stock_cash_div],
                    '每股股票股利':[stock_share_div],
                    '股利支付率 （每股股利/每股收益）':[stock_cash_div_rate],
                    '实际收益率':[np.sum(real_rate)],
                    'ROE （净利润/股东权益）':[stock_ROE],
                    '负债率 （总负债/总资产）':[stock_LEV],
                    '周转率（营业收入/总资产）':[stock_T]}
            return stock_info
                   
    else:
        pass


# a=pd.concat([pd.DataFrame(stock_data(i,2008))  for i in [2008]])