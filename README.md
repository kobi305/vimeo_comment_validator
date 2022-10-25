## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
Vimeo app validator enable you to comment on any videos on [Vimeo](https://vimeo.com/)
and verifying that your comment was added.  
The commenting step is done by using 
[vimeo developer API](https://developer.vimeo.com/api/guides/start).  
The verification step is done by using 
[selenium](https://www.geeksforgeeks.org/selenium-python-tutorial/).  

## Technologies
Project is created with:
* Selenium
* Pyvimeo
	
## Setup
To run this project, install it locally using pip:

```
$ git clone https://github.com/kobi305/vimeo_comment_validator
$ cd .\vimeo_comment_validator\
$ pip install -r requirements.txt

# For running the Vimeo app
$ python .\vimeo_comment_validator.py  

# For running the Vimeo tests 
$ python -m pytest -s .\test_vimeo_validator.py
```





