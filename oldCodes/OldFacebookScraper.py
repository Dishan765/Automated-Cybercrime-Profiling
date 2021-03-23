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

# driver for Firefox browser
driver = webdriver.Firefox()

# Dataset file name
file_name = "Dataset1.csv"

# Login to Facebook


def login():
    # Opens link to facebook login page
    driver.get("https://en-gb.facebook.com/")

    # print("Enter Login Details for Facebook")
    # email = input("Enter your email: ")
    # pwd = getpass.getpass(prompt="Enter your password: ")
    email = "tom310359@gmail.com"
    pwd = "12345qwerty!"
    # target username and password
    username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
    password = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

    # enter username and password
    username.clear()
    username.send_keys(email)
    password.clear()
    password.send_keys(pwd)

    # target the login button and click it
    button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[type='submit']"))).click()


def get_url():
    print('Enter URL of post-replace "www" with "m" (format:"https://m.facebook.com/....")')
    url = input("Enter URL: ")
    return url


# Check if button "more comments..." has attribute "data-store-id"
# if it has this attribute return true (all comments has been loaded)
def checkAttribute():
    try:
        moreComments = driver.find_element_by_class_name("_108_")
        #print(moreComments.get_attribute("data-store-id"))
        if moreComments.get_attribute("data-store-id") == None:
            return False
        else:
            return True
    except NoSuchElementException:
        return False


def scrap_comments(url):
    # post_url = "https://m.facebook.com/story.php?story_fbid=4088181671244825&id=108299339233098&refid=17&_ft_=mf_story_key.4088181671244825%3Atop_level_post_id.4088181671244825%3Atl_objid.4088181671244825%3Acontent_owner_id_new.108299339233098%3Athrowback_story_fbid.4088181671244825%3Apage_id.108299339233098%3Astory_location.4%3Astory_attachment_style.share%3Atds_flgs.3%3Aott.AX8NNxEzaT19-qeJ%3Athid.108299339233098%3A306061129499414%3A2%3A0%3A1617260399%3A-6738461169857371028&__tn__=*W-R"
    # post_url = "https://m.facebook.com/story.php?story_fbid=4134741799922145&id=108299339233098&anchor_composer=false&__tn__=*W-R"
    post_url = url

    # Open link
    driver.get(post_url)
    # Wait for the page to load
    time.sleep(10)

    commentsText = []
    # Find post content
    # try:
    #     post = driver.find_element_by_class_name("_1-sh")
    #     # Write post title to RawDataset.txt
    #     commentsText.append(post.text)
    # except:
    #     print("Post Content is not text.")

    while True:
        # if true, all comments has been loaded
        # no need to click on "more comments" button
        # needed since "more comments" never disappears
        # even when all comments has been loaded
        if checkAttribute():
            break
        else:
            #e = driver.find_element_by_class_name("_108_")
            #e.click()
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, "_108_"))).click()
            time.sleep(5)

        
     
        # if checkAttribute():
        #     break
        # else:
        #     #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "_108_"))).click()
        #     try:
        #         WebDriverWait(driver, 10).until(
        #             EC.element_to_be_clickable((By.CLASS_NAME, "_108_"))).click()
        #     except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
        #         break

    # Wait for all previous comments/view more comments to load
    time.sleep(10)

    # _2a_m to click
    replyLinks = driver.find_elements_by_css_selector(
        "a[data-sigil='ajaxify']")
    for link in replyLinks:
        link.click()

    # wait for all replies to loead
    time.sleep(10)

    # _2b06
    # normal comments
    # comments = driver.find_elements_by_css_selector(
    #     "div[data-sigil='comment-body']")
    # for comment in comments:
    #     commentsText.append(comment.text)

    return commentsText


def writeToFile(comments):
    labels = []
    for comment in comments:
        labels.append(0)

    dict = {'Comments': comments, 'Labels': labels}
    df = pd.DataFrame(dict)

    # Check if file exists
    hdr = False if os.path.isfile('filename.csv') else True

    # Write dataframe to file
    df.to_csv(file_name, mode='a', header=hdr, index=False)



def main():
    url_list = []
    comment_list = []
    commentsCount = [0, 0, 0, 0]

    # while True:
    #   print("Enter stop or STOP to stop entering post url.")
    #   print('Enter URL of post-replace "www" with "m" (format:"https://m.facebook.com/....")')
    #   url = input("Enter URL: ")

    #   if url == "STOP" or url == "stop":
    #     break
    #   else:
    #     url_list.append(url)

    # fileName = input("Enter file name to store comments: ")
    datasetFile = "Dataset1.csv"
    # urlFile = input("Enter filename containing links of the posts.")
    urlFile = "links2.txt"
    url_list.append("https://m.facebook.com/story.php?story_fbid=4134741799922145&id=108299339233098&anchor_composer=false&__tn__=*W-R")

    
    # print(url_list)

    login()
    for index, urls in enumerate(url_list):
        # urls = urls.rstrip("\n")
        print(f".................PROCESSING URL NO {index}.............")
        comments = scrap_comments(urls)
        if index == 0:
            commentsCount[0] = commentsCount[0]+ len(comments)
        elif index == 1:
            commentsCount[1] = commentsCount[1]+len(comments)
        elif index == 2:
            commentsCount[2] = commentsCount[2]+len(comments)
        elif index == 3:
            commentsCount[3] = commentsCount[3]+len(comments)

        comment_list.extend(comments)

    # print("......................WRITING TO FILE................................")
    writeToFile(comment_list)

    # driver.quit()
    print("..............FINSHED SCRAPING ALL THE POSTS........")
    print(commentsCount)
    # print("No of comments from defimdia page's posts")

   


if __name__ == "__main__":
    main()
