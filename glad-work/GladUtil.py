#직영, 지사구분 리스트
GROUP1= ('글래드송내',     '글래드', '글래드성공', '글래드의정부',
         '글래드여주',     '글래드레전드', '글래드인천', '글래드라온', 
         '글래드HL'
        )
GROUP2= ('글래드조은',     '글래드상동',  '글래드피스토스', '글래드가온',
         '글래드프라임',   '글래드방이',  '글래드경기',     '글래드아이리치',
         '글래드제이엔제이', '글래드씨티엠','글래드시흥',   '글래드파주'
        )

씨티엠사원 = ['GLD809183018','GLD809183012','GLD809183029','GLD809183011','GLD809183035','GLD809183013']
시흥사원 = ['GLD101173004','GLD809193030']

공동지점 = ['글래드','글래드가온','글래드경기','글래드HL','글래드라온','글래드방이','글래드시흥',
          '글래드상동','글래드성공','글래드송내','글래드시흥','글래드아이리치','글래드조은',
          '글래드프라임','글래드피스토스']

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
    dfC.loc[:,'지점'] = dfC['지점'].str.replace('MP|엠피','글래드',regex=True)
    dfC.loc[:, colNm] = dfC.지점.map(lambda x: '지사'  if x in GROUP2 else ('직영' if x in GROUP1 else '오류'))
    return dfC


def fcConv(brh,fcCode,cDate):
    ''' 김묘정 송내,메트로 구분/ 글래드소속중 타 지점 사원, '''
    res = brh
    if fcCode in (['GLD806143004','MPK806143004']): #김묘정
        if  cDate < '20200701':
              res = '글래드송내'
        else: res = '글래드'
        
    if fcCode in (['GLD713223001']): #한명실
        if  cDate < '20230401':  
             res = '글래드성공'
                
    if fcCode in (['GLD809183012']):  #박윤희
        if  cDate < '20230101':  
             res = '글래드씨티엠'
                
    if res == '글래드':
        if fcCode in 씨티엠사원:
            res = '글래드씨티엠'
        elif fcCode in 시흥사원:    
            res = '글래드시흥'
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
#    if val in conv_dict.keys():
#        return conv_dict[val]
#    else:
#        return val
    return conv_dict.get(val, val)

def Share_Proc(df, gb, head_nm):
    ''' 본사시상 추출할때 사용하는 함수로서 mp와 공동정산 대상여부 판단
        head_nm에 포함된 keyword가 지점 컬럼에 있으면 무조건 포함
        사원명에 추가되거나 명칭이 변경되면 수정이 필요함
    '''
    chg = False
    if '담당' in df.columns and '사원' not in df.columns:
        df = df.rename(columns={"담당":"사원"})
        chg = True

    # 공동지점중 정산대상 사원
    include_sa = ["글래드프라임이상희","글래드프라임송승환","글래드프라임허윤경"]
    # 공동지점중 비정산대상 사원=>이순연 다시 포함
    exclude_sa = ['글래드송내황순정','글래드성공이순연XXX','글래드라온박종철','글래드라온이용진','글래드라온박종호']

    df['temp_xx'] =  df['지점']+df['사원']

    if gb == '공동':
        # 공동지점 = 공동지점.remove('글래드프라임')
        str_exp = ' (지점 in @공동지점 or 지점.str.contains(@head_nm)) '
        df = df.query(str_exp, engine='python')

        df = df[ (df['지점']!='글래드프라임') | (df['temp_xx'].isin(include_sa)) ]
        df = df[~df['temp_xx'].isin(exclude_sa)]
    else:
        str_exp = ' ( 지점 not in @공동지점 or 지점.str.contains(@head_nm) or \
            (지점=="글래드프라임" and temp_xx not in @include_sa) or temp_xx in @exclude_sa )'
        df = df.query(str_exp, engine='python')
    
    if chg:
        df = df.rename(columns={"사원":"담당"})

    return df.drop(columns='temp_xx')


