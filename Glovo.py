from selenium import webdriver
def deliver():
    browser = webdriver.Chrome()
    browser.get("https://glovoapp.com/ua/uk/kiyiv-praviy-bereg/")
    time.sleep(5)
    #speak("Что вы хотите заказать? Давайте по одному.")
    dish = input()
    while(True):
        if("всё" in dish or "все" in dish):
            break
        elif("я сам" in dish or "сам" in dish):
            return
        else:
            first_pole = browser.find_element_by_css_selector(".el-input__inner")
            first_pole.send_keys(f"{dish}")

deliver()




