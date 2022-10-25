import os
import sys
import vimeo
import colorama
from colorama import Fore, Back, Style


from comment import Comment, InvalidCommentException
from dotenv import load_dotenv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, InvalidSelectorException

load_dotenv()
colorama.init(autoreset=True)

ACCOUNT_EMAIL = os.getenv('ACCOUNT_EMAIL')
ACCOUNT_PSW = os.getenv('ACCOUNT_PSW')
ACCOUNT_NAME = os.getenv('ACCOUNT_NAME')
VIMEO_API_URI = 'https://api.vimeo.com'
VIMEO_URL = 'https://vimeo.com/'
VIMEO_COMMENT_URL = 'https://api.vimeo.com/videos/videoID/comments'
VIDEO_ID = '759557880'

SELECTOR = dict(
    login_btn='//*[@id="__next"]/div[1]/header/div/div[2]/div/div[2]/div/div[1]/button[1]',
    login_form='//*[@id="modal-root"]/div[2]/div[2]/form[1]',
    email='login_email',
    password='password',
    login_submit='//*[@id="modal-root"]/div[2]/div[2]/form[1]/button/div',
    search='topnav-search',

    comment_username='//*[@id="comment_COMMENT_ID"]/div[1]/div[2]/div/span/a',
    comment_text='//*[@id="comment_COMMENT_ID"]/div[1]/div[2]/div/div/p',
    comments='//*[@id="comments"]/div[1]',
    comment_id='comment_'
)


class VimeoClient:
    def __init__(self, vimeo_client: str, vimeo_secret: str, vimeo_access: str):
        self.client = vimeo.VimeoClient(
            token=vimeo_access,
            key=vimeo_client,
            secret=vimeo_secret
        )
        self.__validate_client()

    def __validate_client(self):
        response = self.client.get(VIMEO_API_URI)
        response_json = response.json()

        if response_json.get('error_code', None):
            print(f"{Fore.RED}{response_json['developer_message']}")
            self.client = None
        else:
            print(f'{Fore.GREEN}Start vimeo client')

    def add_comment(self, comment: Comment) -> Comment:
        if not self.client:
            print(f'{Fore.RED}Vimeo client is not defined yet, please init it with valid credentials')

        comment_url = VIMEO_COMMENT_URL.replace('videoID', comment.video)
        response = self.client.post(comment_url, data={'text': comment.text})

        if response.json().get('error', None):
            print(f"{Fore.RED}{response.json()['error']}")
        else:
            comment.id = self.__get_comment_id(response)
            print(f'{Fore.GREEN}Comment added to video {comment.video} successfully')

        return comment

    @staticmethod
    def __get_comment_id(response):
        json_info = response.json()
        comment_uri = json_info['uri']
        return comment_uri.rsplit('/', 1)[-1]


class VimeoCommentValidator:

    def __init__(self, comment: Comment = None, timeout=10) -> None:
        self.comment = comment
        self.timeout = timeout
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()

    def validate_comment(self) -> None:
        try:
            self.__validate_comment_fields()
            self._goto_site()
            self.__login()
            self.__navigate_to_source()
            self.__validate_comment()
        except Exception as e:
            print(f"{Fore.RED}{e}")
            print(f'{Fore.RED}Validator stopped')
        finally:
            self.driver.close()
            sys.exit()

    def __validate_comment_fields(self):
        if not self.comment or not all(self.comment.__dict__.values()):
            raise InvalidCommentException(self.comment.__dict__)

    def _goto_site(self, url: str = VIMEO_URL):
        try:
            self.driver.get(url)
        except Exception as e:
            raise Exception(f'{Fore.RED}Opening chrome at {url} failed')

    def _wait_for_selector(self, attribute, selector: str) -> WebElement:
        try:
            element: WebElement = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((attribute, selector))
            )
            return element
        except TimeoutException as e:
            raise Exception(f'Timeout: Selector {attribute}={selector} not found, '
                            f'please validate selector is valid')

    def __login(self):
        try:
            login_btn = self._wait_for_selector(By.XPATH, SELECTOR['login_btn'])
            login_btn.click()

            email = self._wait_for_selector(By.ID, SELECTOR['email'])
            password = self.driver.find_element(By.ID, SELECTOR['password'])

            email.send_keys(ACCOUNT_EMAIL)
            password.send_keys(ACCOUNT_PSW)

            self.driver.find_element(By.XPATH, SELECTOR['login_submit']).click()
        except Exception as e:
            raise Exception(f'{e} \nLogin failed')

    def __navigate_to_source(self) -> None:
        try:
            search = self._wait_for_selector(By.ID, SELECTOR['search'])
            search.send_keys(self.comment.video)
            search.send_keys(Keys.ENTER)

            video_link = self._wait_for_selector(By.XPATH, '//a[@href="' + VIMEO_URL + self.comment.video + '"]')
            video_link.click()
        except Exception as e:
            raise Exception(f'{e} \nNavigation failed')

    def __highlight_element(self, element: WebElement):
        self.driver.execute_script("arguments[0].style.backgroundColor = 'lightblue';", element)

    def __validate_comment(self) -> None:
        try:
            comments = self._wait_for_selector(By.XPATH, SELECTOR['comments'])
            my_comment = comments.find_element(By.ID, SELECTOR['comment_id'] + self.comment.id)
            self.__highlight_element(my_comment)

            name_selector = SELECTOR['comment_username'].replace('COMMENT_ID', self.comment.id)
            text_selector = SELECTOR['comment_text'].replace('COMMENT_ID', self.comment.id)

            username = self.driver.find_element(By.XPATH, name_selector).text
            text = self.driver.find_element(By.XPATH, text_selector).text

            if username != ACCOUNT_NAME or text != self.comment.text:
                print(f'{Fore.RED}Validation failed: one or more of the details is different'
                      f' username={username} text={text}')

            print(f'{Fore.GREEN}Validation passed successfully')
        except Exception as e:
            raise Exception(f'{e} \nValidation failed')


if __name__ == '__main__':
    video_comment = Comment(video=VIDEO_ID, text='Nice Video')
    vimeo_app = VimeoClient(
        vimeo_client=os.getenv('VIMEO_CLIENT'),
        vimeo_secret=os.getenv('VIMEO_SECRET'),
        vimeo_access=os.getenv('VIMEO_ACCESS'),
    )
    video_comment = vimeo_app.add_comment(comment=video_comment)
    vimeo_validator = VimeoCommentValidator(comment=video_comment)
    vimeo_validator.validate_comment()
