# django-url-shortener
This is a simple application to create short urls.

# Run & Configure
The best way to run this project is by using docker and docker compose.
First clone the project to your drive and enter the directory.
```
git clone https://github.com/co-mat/django-url-shortener.git
cd django-url-shortener
```

After entering the directory before running docker you have to define some enviromental variables.
Create .env file by `touch .env` and open it in any text editor.

Please fill those fields which are requested with your own values:
```
POSTGRES_DB=[your-database-name]
POSTGRES_USER=[your-database-user]
POSTGRES_PASSWORD=[your-database-password]

DJANGO_SECRET_KEY=[some-strong-secret-key]
DEBUG=True
DJANGO_LOGLEVEL=info
DJANGO_ALLOWED_HOSTS=localhost
DATABASE_ENGINGE=postgres_psycopg2

```

If you've created the .env now you may run the project:
```
docker compose -f docker-compose.yaml build
docker compose -f docker-compose.yaml up
```
You may access the project by going to http://localhost:8000/api/.

# Available endpoints
* http://localhost:8000/api/link/ - this endpoint is used to create a shortened link. Just pass a payload using POST method:
```
{
  "target_url": "https://example.com",
  "short_code": "test1"
}
```
* NOTE short_code parameter is optional - if you won't pass it, the server will generate short code for you. *
In response you'll receive 
```
{
"short_url": "http://localhost:8000/short/j4xj2ZpC4JrU"
}
```
This is a shortened url.

* http://localhost:8000/short/[A-Za-z0-9]{12} - This urls servers as RedirectView, it'll simply redirect you to the target_url

