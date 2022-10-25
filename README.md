## Table of contents

* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info

Vimeo app validator enable you to comment on any videos on [Vimeo](https://vimeo.com/)
and verifying that your comment was added.  
The commenting step is done by using VimeoClient object which use
[vimeo developer API](https://developer.vimeo.com/api/guides/start).  
The verification step is done by using VimeoCommentValidator object which use
[selenium](https://www.geeksforgeeks.org/selenium-python-tutorial/).

## Technologies

Project is created with:

* Selenium
* Pyvimeo
* pytest

## Setup

To run this project, please follow next steps:

```
# clone project from github
$ git clone https://github.com/kobi305/vimeo_comment_validator

# enter project directory  
$ cd .\vimeo_comment_validator\

# install all project's pakcges and dependencies
$ pip install -r requirements.txt

# For running the Vimeo validator app
$ python .\vimeo_comment_validator.py  

# For running the Vimeo tests 
$ python -m pytest -s .\test_vimeo_validator.py
```





