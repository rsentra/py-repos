#직영, 지사구분 리스트
GROUP1= ('글래드송내',     '글래드', '글래드성공', '글래드의정부',
         '글래드여주',     '글래드레전드', '글래드라온',
         '글래드HL'
        )
GROUP2= ('글래드조은',     '글래드상동',  '글래드피스토스', '글래드가온',
         '글래드프라임',   '글래드방이',  '글래드경기',     '글래드아이리치',
         '글래드제이엔제이', '글래드씨티엠','글래드시흥'
        )


import pandas as pd
def Metro(brh,j_brh,team):
    """ 메트로 코드 오류 보정 """
  
    if pd.isnull(team): team='00'
    if pd.isnull(j_brh): j_brh='00'
    if '시흥' in (j_brh):          return '글래드시흥'
    elif '시흥' in (team):         return '글래드시흥'
    elif '씨티엠' in (j_brh):      return '글래드씨티엠'
    elif '씨티엠' in (team):       return '글래드씨티엠'
    elif '제이엔제이' in (j_brh):  return '글래드제이엔제이'
    else: return brh


def BrhConv(dfC,colNm):
    """ 메트로 코드 분리.  2. 직영,지사구분값 (colNm에 생성) """
  
    dfC.loc[:,'지점'].fillna('글래드', inplace=True)  #결측치 보정
    dfC.loc[:,'지점'] = dfC.apply(lambda x: fcConv(x['지점'], x['사원번호'], x['계약일자']), axis=1)	
    dfC.loc[:,'변환지점'] = dfC.apply(lambda x: Metro(x['지점'], x['직할지점'], x['팀']), axis=1)
    dfC.rename(columns = {'지점':'원지점','변환지점':'지점'},inplace=True)
    #---직영,지사 구분  => 속도느리면 df만들어 join할 것
    dfC.loc[:, colNm] = dfC.지점.map(lambda x: '지사'  if x in GROUP2 else ('직영' if x in GROUP1 else '오류'))
    return dfC

def grpConv(dfC,colNm):
    '''  직영/지사 구분 '''
    dfC.loc[:,'지점'].fillna('글래드', inplace=True)  #결측치 보정
    # mp,엠피로 된 명칭을 글래드로 변경
    dfC.loc[:,'지점'] = dfC['지점'].str.replace('MP|엠피','글래드')
    dfC.loc[:,'지점'] = dfC.apply(lambda x: fcConv(x['지점'], x['사원번호'], x['계약일자']), axis=1)	
    dfC.loc[:,colNm] = dfC.지점.map(lambda x: '지사'  if x in GROUP2 else ('직영' if x in GROUP1 else '오류'))
    return dfC

def grpConv2(dfC,colNm):
    '''  직영/지사 구분 '''
    dfC.loc[:,'지점'].fillna('글래드', inplace=True)  #결측치 보정
    # mp,엠피로 된 명칭을 글래드로 변경
    dfC.loc[:,'지점'] = dfC['지점'].str.replace('MP|엠피','글래드')
    dfC.loc[:, colNm] = dfC.지점.map(lambda x: '지사'  if x in GROUP2 else ('직영' if x in GROUP1 else '오류'))
    return dfC


def fcConv(brh,fcCode,cDate):
    ''' 김묘정 송내,메트로 구분 '''
    res = brh
    if fcCode in (['GLD806143004','MPK806143004']):
        if  cDate < '20200701':
              res = '글래드송내'
        else: res = '글래드'
    return res

    '''
    str='글래드아이리치'
    if str in GROUP1: print('직영')
    elif str in GROUP2: print('직사')
    else: print('err')
    '''

def convertByVal(val, conv_dict):
   """ 
   val에 해당하는 key가 dict에 있으면 변환하여 return 
   """
   if val in conv_dict.keys():
       return conv_dict[val]
   else:
       return val