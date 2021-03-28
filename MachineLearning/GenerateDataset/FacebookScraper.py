# Scrape comment from specific Facebook Post
# Used to generate dataset

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import getpass
import pandas as pd
import os


class Scraper:
    # driver for Firefox browser
    #driver = webdriver.Firefox()

    # data_fileName -> dataset file
    # constructor
    def __init__(self, data_fileName, url_fileName):
        self.driver = webdriver.Firefox()
        self.data_fileName = data_fileName
        self.url_fileName = url_fileName

    # destructor
    def __del__(self):
        self.driver.quit()

    # Login to Facebook
    def login(self):
        # Opens link to facebook login page
        self.driver.get("https://en-gb.facebook.com/")

        #print("Enter Login Details for Facebook")
        #email = input("Enter your email: ")
        #pwd = getpass.getpass(prompt="Enter your password: ")
        email = "tom310359@gmail.com"
        pwd = "12345qwerty!"
        # target username and password
        username = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
        password = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

        # enter username and password
        username.clear()
        username.send_keys(email)
        password.clear()
        password.send_keys(pwd)

        # target the login button and click it
        button = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[type='submit']"))).click()

    def readURL_file(self):
        fr = open(self.url_fileName, "r")
        lines = fr.readlines()
        return lines

    def scrap_comments(self, url):
        #post_url = "https://m.facebook.com/story.php?story_fbid=4088181671244825&id=108299339233098&refid=17&_ft_=mf_story_key.4088181671244825%3Atop_level_post_id.4088181671244825%3Atl_objid.4088181671244825%3Acontent_owner_id_new.108299339233098%3Athrowback_story_fbid.4088181671244825%3Apage_id.108299339233098%3Astory_location.4%3Astory_attachment_style.share%3Atds_flgs.3%3Aott.AX8NNxEzaT19-qeJ%3Athid.108299339233098%3A306061129499414%3A2%3A0%3A1617260399%3A-6738461169857371028&__tn__=*W-R"
        post_url = url

        # Open link
        self.driver.get(post_url)
        # Wait for the page to load
        time.sleep(10)

        commentsText = []
        # Find post content
        try:
            post = self.driver.find_element_by_class_name("_1-sh")
            # Write post title to RawDataset.txt
            commentsText.append(post.text)
        except:
            print("Post Content is not text.")

        while True:
            # if true, all comments has been loaded
            # no need to click on "more comments" button
            # needed since "more comments" never disappears
            # even when all comments has been loaded
            if self.checkAttribute():
                break
            else:
                try:
                    WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "_108_"))).click()
                    # Wait for page to load
                    time.sleep(5)
                except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                    break


        # Wait for all previous posts to load
        time.sleep(10)

        # _2a_m to click
        #try..catch: try to click on reply links
        #if fail, retry again since the old links may be stale
        try:
            replyLinks = self.driver.find_elements_by_css_selector(
                "a[data-sigil='ajaxify']")
            
            for link in replyLinks:
                link.click()
                time.sleep(5)
        except (StaleElementReferenceException):
            replyLinks = self.driver.find_elements_by_css_selector("a[data-sigil='ajaxify']")
            
            for link in replyLinks:
                link.click()
                time.sleep(5)


        # wait for all replies to loead
        time.sleep(10)

        # _2b06
        # normal comments
        comments = self.driver.find_elements_by_css_selector(
            "div[data-sigil='comment-body']")
        for comment in comments:
            commentsText.append(comment.text)

        return commentsText

    # Check if button "more comments..." has attribute "data-store-id"
    # if it has this attribute return true (all comments has been loaded)
    def checkAttribute(self):
        try:
            moreComments = self.driver.find_element_by_class_name("_108_")
            # moreComments.get_attribute("data-store-id")
            if moreComments.get_attribute("data-store-id") == None:
                return False
            else:
                return True
        except NoSuchElementException:
            return False

    def writeToFile(self, comments,source,links):
        labels = []
        for comment in comments:
            labels.append(0)

        dict = {"Link to Post": links,'Source':source, 'Comments': comments, 'Labels': labels}
        df = pd.DataFrame(dict,columns=[ 'Link to Post','Source','Comments','Labels'])

        # Check if file exists
        hdr = False if os.path.isfile(self.data_fileName) else True

        # Write dataframe to file
        df.to_csv(self.data_fileName, mode='a', header=hdr, index=False)


def main():
    url_list = []
    
    # while True:
    #   print("Enter stop or STOP to stop entering post url.")
    #   print('Enter URL of post-replace "www" with "m" (format:"https://m.facebook.com/....")')
    #   url = input("Enter URL: ")

    #   if url == "STOP" or url == "stop":
    #     break
    #   else:
    #     url_list.append(url)

    #fileName = input("Enter file name to store comments: ")
    datasetFile = "Datasets/Dataset1.csv"
    #urlFile = input("Enter filename containing links of the posts.")
    urlFile = "links.txt"
    scraper = Scraper(datasetFile, urlFile)

    url_list = scraper.readURL_file()

    scraper.login()


    source = []
    links = []
    comment_list = []
    for index, urls in enumerate(url_list):
        urls = urls.rstrip("\n")
        print(f".................PROCESSING URL NO {index}.............")
        comments = scraper.scrap_comments(urls)

        if index>=0 and index <=7 :#radio plus group
            for comment in comments:
                source.append("RadioPlusMauritiusIleMauriceFanGroupUnofficial")
                links.append(urls)
        elif index>=8 and index <=15:#prend compte lepep
            for comment in comments:
                source.append("PRENDCOMPTELEPEP")
                links.append(urls)
        elif index>=16 and index <=18:#defimedia
            for comment in comments:
                source.append("Defimedia")
                links.append(urls)
        elif index>=19 and index <=21:#lexpress
            for comment in comments:
                source.append("Lexpress")
                links.append(urls)

        comment_list.extend(comments)
        print(len(comment_list))
        print(len(links))
        print(len(source))

    # print("......................WRITING TO FILE................................")
    scraper.writeToFile(comment_list,source,links)

    del scraper
    print("..............FINSHED SCRAPING ALL THE POSTS........")


if __name__ == "__main__":
    main()
