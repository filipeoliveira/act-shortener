# ACT-SHORTENER

> URL Shortener built with flask & redis. 

### Tasks

Project was done in 3 hours, but it still have improvements to be done

- [x] Flask setup project
- [x] Redis integration
- [x] Allow client to short a URL
- [x] Same long URL always is shortened to the same unique short URL
- [x] Shortener algorithm (alphanumeric 8 digits, could be sha512)
- [x] Allow client to send shortened URL and obtain the original long URL
- [x] Redirection of the shortened URL to long URL
- [x] Counting visits mechanism
- [x] Swagger integration 
- [ ] Fix redirect endpoint (not working in Swagger integration) 
- [x] Counting visits mechanism
- [x] Better frontend with bootstrap UI + LOGO
- [ ] Workflow diagram
- [ ] Tests
- [ ] Deploy heroku

## 💻 Requirements

Before you start, check if your machine have the redis. If not you can pull redis through docker.
You should have python 3.6+ installed.

## 🚀 Installing & Running

To install the project, follow these steps:

1. Setup redis locally on docker. 
```
docker run -d -p 6379:6379 redis
```

If you have redis locally, this will conflict with. If you already have redis locally in your machine, please move to next step.

2. Install dependencies

```
 pip install -r requirements.txt
```

3. Run server

```
python runserver.py
```

or you can run manually at 

The server should be active on "localhost:5000"

### Endpoints

They are available at (localhost:5000/apidocs)[localhost:5000/apidocs] as well.

| Description  | Method | URL | Parameters |
| --- | --- | --- | --- |
| Shorten a long URL | GET | /shorten | url |
| Access a long URL from a short URL if exists | GET | /{short_id} | short_id |
| Access url details, long url, visits, etc | GET | /{short_id}/detail | short_id |

#### short url generation algorithm

1. Only alphanumeric characters are allowed when creating the short url, ie 62 characters. ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
2. A pseudorandom number between 0 and 61 (total length) is generated which is used to get a character from the valid characters in step 1.

For example:

| Random | Character |
| --- | --- |
| 5  | strings[5] = "f" |

Such algorithm is repeated 8 times. Resulting in possible (62 * 8) unique shorten URL. Resulting in 496 unique URL coexisting inside the db.


--


Observations:
- If a collision happens, the algorithm will try again. For the purpose of this challenge I have defined the length to be 8 characters, since I was not focused on collisions or performance here, but in a production environment we might use a different approach like a sha512 hash generatin for example.

- I definitily would add some tests if this would go to production.

- A health check endpoint would be nice too.

- In a production environment, probably would add a dockerfile for the application. I did not focused on adding this since it was not a requirement.

[⬆ Back to the top](#ACT-SHORTENER)<br>