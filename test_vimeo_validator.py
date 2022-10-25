import pytest
import os

from dotenv import load_dotenv
from vimeo_comment_validator import VimeoClient, VimeoCommentValidator
from comment import Comment, InvalidCommentException
from selenium.common.exceptions import TimeoutException, InvalidSelectorException, NoSuchElementException

load_dotenv()


@pytest.fixture
def vimeo_client():
    return VimeoClient(
        vimeo_client=os.getenv('VIMEO_CLIENT'),
        vimeo_secret=os.getenv('VIMEO_SECRET'),
        vimeo_access=os.getenv('VIMEO_ACCESS'),
    )


@pytest.fixture
def vimeo_validator():
    return VimeoCommentValidator()


class TestVimeoClient:
    def test_invalid_vimeo_credential(self):
        vimeo = VimeoClient(
            vimeo_client=os.getenv('VIMEO_CLIENT'),
            vimeo_secret=os.getenv('VIMEO_SECRET'),
            vimeo_access='invalid token',
        )
        assert vimeo.client is None

    def test_valid_video_id(self, vimeo_client: VimeoClient):
        valid_comment = Comment(video='759557880', text='Nice video')
        comment = vimeo_client.add_comment(comment=valid_comment)
        assert comment.id is not None and comment.id.isdigit()

    def test_invalid_video_id(self, vimeo_client: VimeoClient):
        invalid_comment = Comment(video='invalid_video_id', text='Nice video')
        comment = vimeo_client.add_comment(comment=invalid_comment)
        assert comment.id is None


class TestVimeoValidator:

    def test_invalid_element_selector(self):
        comment = Comment(video='1', text='2', id='3')
        vimeo_validator = VimeoCommentValidator(comment=comment)
        vimeo_validator._goto_site()

        with pytest.raises(TimeoutException):
            vimeo_validator._wait_for_selector('xpath', "//button[@type='bad_selector']")
        vimeo_validator.driver.close()

    def test_invalid_comment_fields(self):
        bad_comment = Comment(video='1', text='a')

        with pytest.raises(InvalidCommentException):
            bad_comment.validate()

    def test_verify_invalid_video_id(self):
        """
        bad video id is video id who not exist or the user not comment on it
        """
        bad_video = Comment(video='11111111', text='Nice Video', id='1111111111')
        vimeo_validator = VimeoCommentValidator(comment=bad_video)

        with pytest.raises(NoSuchElementException):
            vimeo_validator._goto_site()
            vimeo_validator._login()
            vimeo_validator._search_video()
            vimeo_validator._pick_comment_video()
        vimeo_validator.driver.close()

    def test_valid_comment(self, vimeo_client):
        valid_comment = Comment(video='759557880', text='I like this video')
        comment = vimeo_client.add_comment(comment=valid_comment)
        vimeo_validator = VimeoCommentValidator(comment=comment)

        vimeo_validator.validate_comment()
        assert vimeo_validator.comment.is_verified is True
