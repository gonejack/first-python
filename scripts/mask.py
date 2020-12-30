import time

from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
browser = webdriver.Chrome(options=option)
UA = 'Mozilla/5.0 (Linux; Android 4.1.1; GT-N7100 Build/JRO03C) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3'
mobileEmulation = {"deviceMetrics": {"width": 320, "height": 640, "pixelRatio": 3.0}, "userAgent": UA}
options = webdriver.ChromeOptions()
options.add_experimental_option('mobileEmulation', mobileEmulation)
mobile = webdriver.Chrome(options=options)
times = 0


def monphone(url):
    global times
    mobile.get(url)
    state = mobile.find_element_by_xpath('//*[@id="s-actionBar-container"]/div/div[2]/a[3]').text
    print(state)
    times = times + 1
    return state


def login():
    browser.get("https://www.taobao.com")
    time.sleep(3)
    if browser.find_element_by_link_text("亲，请登录"):
        browser.find_element_by_link_text("亲，请登录").click()
        print(f"请尽快扫码登录")
        time.sleep(10)


def mon(url):
    browser.get(url)
    global state
    js1 = '''Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) '''
    js2 = '''window.navigator.chrome = { runtime: {},  }; '''
    js3 = '''Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); '''
    js4 = '''Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); '''
    browser.execute_script(js1)
    browser.execute_script(js2)
    browser.execute_script(js3)
    browser.execute_script(js4)
    time.sleep(3)
    try:
        stock = browser.find_element_by_id("J_EmStock").text
        print(stock)
        state = 1
    except:
        print(f'没有找到库存信息')
        state = 0


def clear():
    mobile.delete_all_cookies()
    global times
    times = 0
    print("已清除缓冲区")


def choice(num):
    source = browser.page_source
    if "已选择" in source:
        print('已选择')
        return 1
    else:
        print('没有发现选中目标')
        browser.find_element_by_xpath(
            '//*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[4]/div/div/dl[1]/dd/ul/li[' + str(num) + ']').click()


def buy():
    num = 0
    while num < 15:
        try:
            print('类型寻找中 %s' % num)
            type = browser.find_element_by_xpath(
                '//*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[4]/div/div/dl[1]/dd/ul/li[' + str(num) + ']').text
            print('选择类型 %s' % type)
            browser.find_element_by_xpath(
                '//*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[4]/div/div/dl[1]/dd/ul/li[' + str(num) + ']').click()
            choice(num)
            stock = browser.find_element_by_id("J_EmStock").text
            print(stock)
            print(type)
            browser.find_element_by_id("J_LinkBuy").click()
            time.sleep(1)
            browser.find_element_by_class_name("go-btn").click()
            return 1
        except:
            num = num + 1
            print(num)


login()
url = input()
while True:
    state = monphone(url)
    if times >= 100:
        clear()
    if state == "立即购买":
        mon(url)
        if state == 1:
            success = buy()
            if success == 1:
                print('成功')
                break
