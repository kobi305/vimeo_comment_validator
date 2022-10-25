import pytest
import os
from dotenv import load_dotenv

from vimeo_comment_validator import VimeoClient, VimeoCommentValidator
from comment import Comment, InvalidCommentException
from selenium.common.exceptions import TimeoutException, InvalidSelectorException

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

    def test_invalid_element_selector(self, vimeo_validator):
        vimeo_validator._goto_site()

        with pytest.raises(TimeoutException):
            vimeo_validator._wait_for_selector('xpath', "//button[@type='bad_selector']")

    def test_verify_invalid_comment_fields(self, vimeo_validator):
        bad_comment = Comment(video='11111111', text='xxxxx')
        vimeo_validator.comment = bad_comment
        with pytest.raises(InvalidCommentException):
            vimeo_validator.validate_comment()

    # def test_verify_invalid_video_id(self, vimeo_validator):
    #     pass

    # def test_verify_invalid_comment_id(self):
    #     pass
