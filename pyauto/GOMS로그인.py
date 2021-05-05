import pyautogui
import time
import webbrowser
conf=0.9
pyautogui.PAUSE=0.3

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


# ret = pyautogui.confirm(text='현재 로그인상태인가요?', title='선택',buttons=['connected', 'url','pos'])
ret='url'
try:
    f=open("img/setup.txt", "r") #로그인정보 파일 읽기
    lines=f.readlines()
    gid = lines[0].rstrip()
    pwd = lines[1].rstrip()
    yy = lines[2].rstrip()
    mm = lines[3].rstrip()
    dd = lines[4].rstrip()
    ss = lines[5].rstrip()
    waitTime =int(ss.split()[0])
    f.close()
    if ret=='connected':
        res='OK'
    else:
        if ret=='url':
            ie = webbrowser.get('c:\\program files\\internet explorer\\iexplore.exe')
            ie.open('https://www.globalfm.kr')
        else: 
            pyautogui.moveTo(101,142)
            pyautogui.doubleClick()
            time.sleep(1)
            pyautogui.moveTo(135,49,2)
            pyautogui.click()
            pyautogui.typewrite(['delete']) 
            pyautogui.typewrite(['enter']) 
            pyautogui.typewrite('www.globalfm.kr') 
            pyautogui.typewrite(['enter']) 

        time.sleep(2)
        img_click('img/goms_popup1.png')
        
        time.sleep(1)
        q=f_readImage('img/goms_login1.png',waitTime) #
        if q==None:  raise Exception('login1 이미지 오류')
     
        time.sleep(1)
        pyautogui.typewrite(gid) 
        pyautogui.typewrite(['tab']) 
        pyautogui.press('delete', presses=10)
        pyautogui.press('backspace', presses=10)
        pyautogui.typewrite(pwd)
#         q=pyautogui.locateCenterOnScreen('img/goms_login2.png')
#         if q==None:  raise Exception('login2 url 이미지 오류')
#         pyautogui.click(q)
        pyautogui.typewrite(['enter']) 

        time.sleep(0.5)
        pyautogui.typewrite(yy) 
        time.sleep(0.5)
        pyautogui.typewrite(['tab']) 
        pyautogui.typewrite(mm) 
        time.sleep(0.5)
        pyautogui.typewrite(['tab']) 
        pyautogui.typewrite(dd) 
        pyautogui.typewrite(['tab']) 
        pyautogui.typewrite(['enter']) 

        time.sleep(3)
        # pyautogui.click(x=1180, y=162, clicks=1, interval=2, button='left')# 팝업
        img_click('img/goms_popup1.png')
        time.sleep(1)    
        q=f_readImage('img/goms_login3.png',waitTime) #
        if q==None:  raise Exception('login3 url 이미지 오류')        

    #     res= pyautogui.confirm('로그인이 완료되면 ok.')
        time.sleep(16)
        res='OK'

    ##- -곰스 로그인 후 화면
    if res=='OK':
        q=f_readImage('img/goms_info.png',waitTime) #popup
        time.sleep(1)
        img_click('img/goms_info_yes.png')
        time.sleep(1)
        ret = pyautogui.confirm(text='어느 화면으로?',title='선택',buttons=['계약목록excel down','실적속보-인별','Stop'])
        if ret[:4]=='계약목록':
            time.sleep(1)
            img_click('img/goms_contmgmt.png') # 계약관리 버튼
            time.sleep(1)
            img_click('img/goms_contsrch.png')# 계약검색 버튼
            time.sleep(1)

            cur=time.localtime()
            str_to= time.strftime("%Y%m%d",cur)
            str_fr= str_to[:-2]+'01'
            img_click('img/goms_startdt.png')#  계약시기

            pyautogui.press('left',presses=6)  
            pyautogui.typewrite(str_fr) 
            time.sleep(1)
            img_click('img/goms_enddt.png')#  계약시기

            pyautogui.press('left',presses=6)  
            pyautogui.typewrite(str_to) 

            time.sleep(1)

            img_click('img/goms_query.png')# 조회버튼 

        #     res2=pyautogui.confirm('조회 완료 ?', title='선택',buttons=['Yes', 'No'])
            time.sleep(5)
            res2='Yes'
            if res2=='Yes': 
                img_click('img/goms_excel.png') #excel
            else: print('excel download cancelled')
        elif ret[:2]=='실적':
            img_click('img/goms_sales.png')
            time.sleep(1)
            img_click('img/goms_sales_person.png')
            time.sleep(1)
            img_click('img/goms_sales_person_q.png')
            time.sleep(1)


    else: 
        print('job cancelled')
        pyautogui.alert('  Completed...   ')
except  Exception as e: 
        print('error occured..',str(e))
        pyautogui.alert(str(e))
        pass