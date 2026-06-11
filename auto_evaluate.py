#!/usr/bin/env python3
"""
超星学习通自动评教脚本
输入账号密码，自动完成所有评教问卷
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import (
    NoSuchElementException, UnexpectedAlertPresentException
)
from webdriver_manager.chrome import ChromeDriverManager

# 评语库
POSITIVE_TEXTS = [
    "老师教学认真负责，讲解清晰易懂，课堂氛围良好。",
    "老师专业知识扎实，教学方法得当，收获很大。",
    "老师上课很有激情，能够调动学生积极性，教学效果好。",
    "老师耐心细致，答疑解惑及时，对学习帮助很大。",
    "课程内容丰富，老师讲解生动，学到了很多知识。"
]


class ChaoxingEvaluator:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.evaluation_url = "https://i.chaoxing.com/base?ws=1&t=1781165810804"
        self.skipped_count = 0
        self.skipped_links = set()
        self.setup_driver()
        
    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        print("[1/4] Starting Chrome...")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        })
        print("      Browser ready!")
        
    def dismiss_alert(self):
        try:
            self.driver.switch_to.alert.accept()
            time.sleep(0.3)
            return True
        except:
            return False
        
    def login(self):
        print("\n[2/4] Logging in...")
        self.driver.get('https://i.chaoxing.com')
        time.sleep(2)
        
        try:
            u = self.driver.find_element(By.CSS_SELECTOR, '#phone, #accountName, input[name="username"]')
            p = self.driver.find_element(By.CSS_SELECTOR, '#pwd, #password, input[name="password"]')
            u.clear(); u.send_keys(self.username)
            p.clear(); p.send_keys(self.password)
            self.driver.find_element(By.CSS_SELECTOR, '#loginBtn, .login-btn').click()
            time.sleep(4)
            
            if 'passport' in self.driver.current_url or 'login' in self.driver.current_url:
                print("\n      *** VERIFICATION REQUIRED ***")
                input("      Please complete verification in browser, then press ENTER...")
        except NoSuchElementException:
            print("\n      *** MANUAL LOGIN NEEDED ***")
            input("      Please login in browser, then press ENTER...")
        
        print("      Login complete!")
        
    def navigate_to_evaluation(self):
        print("\n[3/4] Opening evaluation page...")
        self.driver.get(self.evaluation_url)
        time.sleep(2)
        
        if '暂时不能访问' in self.driver.page_source:
            print("      ERROR: Page cannot be accessed!")
            return False
        print("      Page loaded!")
        return True
        
    def enter_evaluation_section(self):
        print("\n[4/4] Entering evaluation section...")
        try:
            self.driver.find_element(By.XPATH, "//h3[contains(text(), '评价问卷')]").click()
            time.sleep(2)
            print("      Entered evaluation section")
        except NoSuchElementException:
            print("      ERROR: Cannot find evaluation section")
            return False
        return self.switch_to_iframe()
    
    def switch_to_iframe(self):
        try:
            self.driver.switch_to.default_content()
            iframe = self.driver.find_element(By.NAME, 'frame_content')
            self.driver.switch_to.frame(iframe)
            time.sleep(0.5)
            return True
        except:
            return False
    
    def refresh_iframe(self):
        try:
            self.driver.switch_to.default_content()
            self.driver.execute_script(
                "document.querySelector('iframe[name=\"frame_content\"]').src = "
                "document.querySelector('iframe[name=\"frame_content\"]').src;"
            )
            time.sleep(2)
            iframe = self.driver.find_element(By.NAME, 'frame_content')
            self.driver.switch_to.frame(iframe)
            time.sleep(0.5)
            return True
        except:
            return False
    
    def get_categories(self):
        categories = []
        try:
            tabs = self.driver.find_elements(By.XPATH, "//li[contains(text(), '评教') or contains(text(), '问卷')]")
            for tab in tabs:
                name = tab.text.strip()
                if name:
                    categories.append(name)
                    print(f"      Found: {name}")
        except:
            pass
        return categories
    
    def click_category(self, name):
        try:
            self.driver.find_element(By.XPATH, f"//li[contains(text(), '{name}')]").click()
            time.sleep(1)
            return True
        except:
            return False
    
    def get_pending_links(self):
        links_info = []
        try:
            rows = self.driver.find_elements(By.CSS_SELECTOR, 'tr')
            for row in rows:
                try:
                    link = row.find_element(By.XPATH, ".//a[contains(text(), '待评价')]")
                    links_info.append({
                        'link': link,
                        'id': row.text.strip()[:50]
                    })
                except:
                    pass
        except:
            pass
        return links_info
    
    def click_next_pending(self):
        links_info = self.get_pending_links()
        for info in links_info:
            if info['id'] not in self.skipped_links:
                try:
                    info['link'].click()
                    time.sleep(2)
                    return info['id']
                except:
                    continue
        return None
    
    def check_has_submit_button(self):
        js = """
        var all = document.querySelectorAll('button, input[type="submit"], a, div[onclick], span[onclick]');
        for (var i = 0; i < all.length; i++) {
            var text = (all[i].innerText || all[i].value || '').trim();
            if (text === '提交' || text === 'Submit' || text === '完成评教') {
                var r = all[i].getBoundingClientRect();
                if (r.width > 0 && r.height > 0) return true;
            }
        }
        return false;
        """
        try:
            return self.driver.execute_script(js)
        except:
            return False
    
    def answer_questions(self):
        answered = 0
        
        # 单选题
        try:
            radios = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="radio"]')
            groups = {}
            for r in radios:
                n = r.get_attribute('name')
                if n:
                    groups.setdefault(n, []).append(r)
            
            for group in groups.values():
                selected = False
                for r in group:
                    try:
                        if '无上述问题' in r.find_element(By.XPATH, './..').text:
                            r.click(); selected = True; break
                    except: pass
                if not selected:
                    try: group[0].click()
                    except: self.driver.execute_script("arguments[0].click()", group[0])
                answered += 1
        except: pass
        
        # 多选题
        try:
            cbs = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
            groups = {}
            for c in cbs:
                n = c.get_attribute('name')
                if n:
                    groups.setdefault(n, []).append(c)
            
            for group in groups.values():
                selected = False
                for c in group:
                    try:
                        if '无上述问题' in c.find_element(By.XPATH, './..').text:
                            c.click(); selected = True; break
                    except: pass
                if not selected:
                    try: group[0].click()
                    except: self.driver.execute_script("arguments[0].click()", group[0])
                answered += 1
        except: pass
        
        # 文本题
        try:
            for ta in self.driver.find_elements(By.TAG_NAME, 'textarea'):
                try:
                    if ta.is_displayed() and ta.is_enabled() and not ta.get_attribute('value'):
                        ta.clear()
                        ta.send_keys(random.choice(POSITIVE_TEXTS))
                        answered += 1
                except: pass
        except: pass
        
        return answered
    
    def submit_and_confirm(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(0.5)
        
        # 提交
        print("          Submitting...")
        js_submit = """
        var all = document.querySelectorAll('button, input[type="submit"], a, div[onclick], span[onclick]');
        for (var i = 0; i < all.length; i++) {
            var text = (all[i].innerText || all[i].value || '').trim();
            if (text === '提交' || text === 'Submit' || text === '完成评教') {
                var r = all[i].getBoundingClientRect();
                if (r.width > 0 && r.height > 0) {
                    all[i].scrollIntoView(); all[i].click();
                    return 'ok';
                }
            }
        }
        return 'not_found';
        """
        
        try:
            result = self.driver.execute_script(js_submit)
        except UnexpectedAlertPresentException:
            self.dismiss_alert()
            return True
        
        if result == 'not_found':
            print("          Submit button not found!")
            return False
        
        time.sleep(2)
        
        # 确认
        js_confirm = """
        var keywords = ['确认提交', '确定提交', '确认', '确定', '是'];
        var all = document.querySelectorAll('button, a, div, span, input');
        for (var i = 0; i < all.length; i++) {
            var text = (all[i].innerText || all[i].value || '').trim();
            for (var j = 0; j < keywords.length; j++) {
                if (text === keywords[j]) {
                    var r = all[i].getBoundingClientRect();
                    if (r.width > 0 && r.height > 0 && r.top >= 0) {
                        all[i].click(); return 'ok';
                    }
                }
            }
        }
        return 'not_found';
        """
        
        try:
            self.driver.execute_script(js_confirm)
        except UnexpectedAlertPresentException:
            self.dismiss_alert()
        
        time.sleep(0.5)
        self.dismiss_alert()
        return True
    
    def process_one_evaluation(self):
        print("        Processing...")
        
        identifier = self.click_next_pending()
        if not identifier:
            return "no_link"
        
        # 切换到新窗口
        original = self.driver.current_window_handle
        new_window = None
        if len(self.driver.window_handles) > 1:
            for h in self.driver.window_handles:
                if h != original:
                    new_window = h
                    self.driver.switch_to.window(h)
                    break
            time.sleep(1)
        
        # 检查是否有提交按钮
        if not self.check_has_submit_button():
            print("          Skipped (website bug)")
            self.skipped_count += 1
            self.skipped_links.add(identifier)
            if new_window and len(self.driver.window_handles) > 1:
                try: self.driver.close()
                except: pass
                self.driver.switch_to.window(original)
            self.refresh_iframe()
            return "skipped"
        
        # 回答问题
        answered = self.answer_questions()
        print(f"          Answered {answered} questions")
        
        # 提交
        try:
            success = self.submit_and_confirm()
            if success:
                print(f"          Submitted!")
            else:
                print(f"          Failed!")
        except UnexpectedAlertPresentException:
            self.dismiss_alert()
            success = True
            print(f"          Submitted!")
        
        # 关闭窗口
        time.sleep(1)
        if new_window and len(self.driver.window_handles) > 1:
            try: self.driver.close()
            except: pass
            self.driver.switch_to.window(original)
        
        if success:
            self.refresh_iframe()
        else:
            self.switch_to_iframe()
        
        return "success" if success else "failed"
    
    def process_category(self, name):
        print(f"\n    Category: {name}")
        
        if not self.click_category(name):
            print(f"      Failed to click category!")
            return 0
        
        time.sleep(1)
        completed = 0
        consecutive_failures = 0
        
        for _ in range(50):
            self.refresh_iframe()
            self.click_category(name)
            time.sleep(0.5)
            
            links = self.get_pending_links()
            pending = [l for l in links if l['id'] not in self.skipped_links]
            
            if not pending:
                print(f"      All done!")
                break
            
            print(f"      [{len(pending)} remaining]")
            
            result = self.process_one_evaluation()
            
            if result == "success":
                completed += 1
                consecutive_failures = 0
                time.sleep(1)
            elif result == "skipped":
                consecutive_failures = 0
            else:
                consecutive_failures += 1
                if consecutive_failures >= 3:
                    print(f"      Too many failures, skipping category")
                    break
                time.sleep(1)
        
        return completed
    
    def run(self):
        print("\n" + "="*60)
        print("  CHAOXING AUTO EVALUATION")
        print("="*60)
        
        self.login()
        
        if not self.navigate_to_evaluation():
            return
        if not self.enter_evaluation_section():
            return
        
        categories = self.get_categories()
        if not categories:
            print("      No categories found!")
            return
        
        total = 0
        for cat in categories:
            total += self.process_category(cat)
        
        print("\n" + "="*60)
        print(f"  COMPLETE!")
        print(f"  Submitted: {total}")
        if self.skipped_count:
            print(f"  Skipped (bug): {self.skipped_count}")
        print("="*60)
    
    def close(self):
        try:
            self.driver.quit()
        except:
            pass


def main():
    print("\n" + "="*60)
    print("  Chaoxing Auto Evaluation Script")
    print("="*60)
    
    username = input("\n  Username: ").strip()
    password = input("  Password: ").strip()
    
    if not username or not password:
        print("  Username and password required!")
        return
    
    evaluator = None
    try:
        evaluator = ChaoxingEvaluator(username, password)
        evaluator.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if evaluator:
            input("\nPress ENTER to close browser...")
            evaluator.close()


if __name__ == '__main__':
    main()