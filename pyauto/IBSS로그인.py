import pyautogui
import time
import webbrowser


# ret = pyautogui.confirm(text='로그인 방식을 선택하세요?\n  로그인 / url / image?',
#                         title='선택',buttons=['connected', 'url','image'])
ret='url'
#--일자입력 / 조회버튼
def f_query(imgStr,str_fr,str_to):
    time.sleep(0.5)
    pyautogui.press('tab',presses=10,interval=0.3) 
    time.sleep(0.5)
    pyautogui.press('delete') 
    pyautogui.typewrite(str_fr)
    pyautogui.press('tab') 
    pyautogui.typewrite(str_to)
    time.sleep(0.5)
    img_click(imgStr)

#엑셀다운
def f_excel():
    time.sleep(1)
    img_click('img/ibss_excel.png')
    time.sleep(2)
    img_click('img/ibss_save.png')

#이미지읽기 - 5회반복
def f_readImage(imgStr,waitCnt):
    retry_counter = 0
    while retry_counter < waitCnt:
        try:
            result = pyautogui.locateCenterOnScreen(imgStr,confidence=conf)
            if result:
                time.sleep(1)
                print('successful read = ',retry_counter, '- ', imgStr)
                retry_counter = 10  # to break the loop
                pyautogui.click(result)
                return result
            else:
                retry_counter += 1
        except:
            time.sleep(1)  # retry after some time, i.e. 1 sec
            retry_counter += 1
    print('fail to read image ', retry_counter, '- ', imgStr)
    return None

def img_click(imgStr,actn='click'):
    q=pyautogui.locateCenterOnScreen(imgStr,confidence=conf)
    if q==None:
        print('fail to click image ', imgStr)
    else:
        if actn=='dbl':
            pyautogui.doubleClick(q)    
        else: pyautogui.click(q)
    return q

pyautogui.PAUSE=0.3
conf=0.9
res =''
try:
    f=open("img/setup_ib.txt", "r") #로그인정보 파일 읽기 : ID,PWD,WAITTIME
    lines=f.readlines()
    gid = lines[0].rstrip()
    pwd = lines[1].rstrip()
    ss = lines[2].rstrip()
    waitTime =int(ss.split()[0])
    f.close()
  
    if  ret=='connected':
        res='OK'
    else:
        if ret=='url':
            ie = webbrowser.get('c:\\program files\\internet explorer\\iexplore.exe')
            ie.open('www.globalfm.co.kr')
        elif ret=='image':
            q=img_click('img/IE.png','dbl')#바탕화면 IE
            time.sleep(1)
            q=img_click('img/ie_1.png')#URL입력창
            if q==None:  raise Exception('url 이미지 오류')
            time.sleep(1) 
            pyautogui.typewrite(['delete'],interval=1) 
            pyautogui.typewrite(['enter'],interval=1) 
            pyautogui.typewrite('www.globalfm.co.kr') 
            time.sleep(1)
            pyautogui.typewrite(['enter'])
        else: raise Exception('err')
            
            
        time.sleep(2)    #새로운 화면이 뜨면 충분히 기다려야 인식함
        r=f_readImage('img/ibss_id.png',waitTime)#ibss ID입력창
        if r==None:
            ret= pyautogui.confirm(text='화면이 이미 실행중이면 yes-> ibss화면 활성화요망', title='오류', buttons=['yes','no'])
            if ret=='yes':
                time.sleep(2)
                r=f_readImage('img/ibss_id.png',waitTime) #ibss ID입력창
                if r==None:  
                    ret='err'
            if ret!='yes':
                raise Exception('로그인화면 인식 오류')
        
        pyautogui.typewrite(gid,interval=0.01) 
        pyautogui.typewrite(['tab']) 
        pyautogui.press('delete', presses=4)
        pyautogui.press('backspace', presses=4)
        pyautogui.typewrite(pwd)

        img_click('img/ibss_login.png')
        time.sleep(1)
        q=img_click('img/ibss_pinfo.png')
        if q==None:
            pyautogui.click(x=1070, y=602, clicks=1, interval=1, button='left')#비번안내
            print('fail to read info image')
        res='OK'

    if res=='OK':
        #x버튼누르면 exception발생하므로 취소버튼 만듬
        ret = pyautogui.confirm(text='어느 화면으로?',title='선택',buttons=['급여정산','생보','장기','생보→장기','취소'])
        time.sleep(1)
        cur=time.localtime()
        str_to= time.strftime("%Y%m%d",cur)
        str_fr= str_to[:-2]+'01'
        if ret=='급여정산':
             imgStr='img/ibss_msalary.png' 
        elif ret[:2]=='생보':
             imgStr='img/ibss_mlife.png' 
        elif ret=='장기':
             imgStr='img/ibss_mlong.png'
        else: raise Exception('Next Process Cancelled....')
        img_click(imgStr)
  
        if ret!='급여정산':
            imgStr='img/ibss_query.png'
            f_query(imgStr,str_fr,str_to)
            f_excel()
            if ret=='생보→장기':
                time.sleep(1)
                img_click('img/ibss_mlong.png')
                imgStr='img/ibss_query.png'
                f_query(imgStr,str_fr,str_to)
                f_excel()
             
        print('job succ')
        pyautogui.alert('  Completed...   ')
except  Exception as e: 
        print('error occured..',str(e))
        pyautogui.alert(str(e))
        pass
