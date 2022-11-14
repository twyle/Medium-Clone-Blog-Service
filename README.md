# Medium Clone Blog Service

> A standalone service for managing blog articles. This includes the creation, update, viewing and deletetion of articles.  

<p align="center">
  <img title="Bandit badge" alt="Bandit badge" src="https://github.com/twyle/user-management-service/actions/workflows/feature-development-workflow.yml/badge.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://github.com/twyle/user-management-service/actions/workflows/development-workflow.yml/badge.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://github.com/twyle/user-management-service/actions/workflows/staging-workflow.yml/badge.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://github.com/twyle/user-management-service/actions/workflows/release-workflow.yml/badge.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://github.com/twyle/user-management-service/actions/workflows/production-workflow.yml/badge.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/security-bandit-yellow.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/Made%20with- Python-1f425f.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/github/license/Naereen/StrapDown.js.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/Medium-12100E?style=flat&logo=medium&logoColor=white" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/github%20actions-%232671E5.svg?style=flat&logo=githubactions&logoColor=white" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/flask-%23000.svg?style=flat&logo=flask&logoColor=white" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=flat&logo=visual-studio-code&logoColor=white" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/Ubuntu-E95420?style=flat&logo=ubuntu&logoColor=white" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/gunicorn-%298729.svg?style=flat&logo=gunicorn&logoColor=white" />
</p>

<img src="assets/images/medium_clone_user_management_system.png" class="img-responsive" alt="">

## Project Overview
This is a web application that enables an author to create, view, uupdate and delete blog posts. Other functionalities include:
1. Commenting on posts
2. Liking posts
3. Bookmarking posts
4. Reporting posts
5. Stats for a given post and author.

## Working 

It's pretty easy to use the application. On the home page (http://localhost:5000/apidocs):

 1. Create an account (post details through register route)
 2. Log in with the createdcredentials to receive an authorization token.
 3. Use that token to authorize yourself.
 4. You can then access the apps functionality.

## Local Setup

Here is how to set up the application locally:

  1. Clone the application repo:</br>

      ```sh
      git clone https://github.com/twyle/Medium-Clone-Blog-Service.git
      ```

  2. Navigate into the cloned repo:

      ```sh
      cd Medium-Clone-Blog-Service
      ```

  3. Create a Virtual environment:

      ```sh
      python3 -m venv venv
      ```

  4. Activate the virtual environmnet:

      ```sh
      source venv/bin/activate
      ```

  5. Install the project dependancies:

      ```sh
      pip install --upgrade pip # update the package manager
      pip install -r requirements.txt  
      ```

  6. Create the environment variables for the service:

      ```sh
      touch .env
      ```

      Then paste the following into the file:

      ```sh

        FLASK_DEBUG=True
        FLASK_ENV=development
        FLASK_APP=manage.py

        SECRET_KEY=secret-key

        POSTGRES_HOST=localhost
        POSTGRES_USER=lyle
        POSTGRES_PASSWORD=lyle
        POSTGRES_DB=lyle
        POSTGRES_PORT=5432

        MAIL_USERNAME=<mail-user-name>
        MAIL_PASSWORD=<mail-password>
        MAIL_SERVER=<mail-server>
        MAIL_PORT=465
        MAIL_USE_SSL=True
        MAIL_DEFAULT_SENDER=<default-email>

        S3_BUCKET=<s3-bucket-name>
        AWS_ACCESS_KEY=<aws-access-key>
        AWS_ACCESS_SECRET=<aws-secret-key>

      ```

      Then create the database secrets:

      ```sh
      cd services/database
      touch .env
      ```

      Then paste the following into the file:

      ```sh
        POSTGRES_DB=lyle
        POSTGRES_PORT=5432
        POSTGRES_USER=postgres
        POSTGRES_PASSWORD=lyle
      ```

  7. Start the database containers:

      ```sh
      docker-compose -f database/docker-compose.yml up --build -d
      ```

  8. Create the database migrations:

      ```sh
      flask db migrate -m "Initial migration."
      flask db upgrade
      ```

  9. Start the services:

      ```sh
      python manage.py run
      ```

  10. View the running application

      Head over to http://0.0.0.0:5000/apidocs 

 <p align=center>
  <img src="assets/videos/user-management-service-v3.gif" />
</p>

## Development

 #### 1. Application Design

  1. **Services**

      The application consists of a single service.

      1. Blog Service 
        
        This services enables the creation, update, deletion and viewing of articles. The routes include:

        | Route                   | Method  | Description                 |
        | ------------------------| ------- |---------------------------- |
        | 'api/v1/author'           | DELETE  | Delete a author.              |
        | 'api/v1/author'           | PUT     | Update author info.           |
        | 'api/v1/author'           | GET     | Get a author's info.          |
        | 'api/v1/authors'          | GET     | List all authors.             |
        | 'api/v1/author/articles_published'           | GET     | Get all articles published by this author.         |
        | 'api/v1/author/articles_read'           | GET     | Get all articles read by this author.         |
        | 'api/v1/author/bookmarks'           | GET     | Get all articles bookmarked by this author.         |
        | 'api/v1/author/comments'           | GET     | Get all comments written by this author.         |
        | 'api/v1/author/likes'           | GET     | Get all likes by this author.         |
        | 'api/v1/author/stats'           | GET     | Get this authors stats.         |
        | 'api/v1/article'           | DELETE  | Delete a article.              |
        | 'api/v1/article'           | PUT     | Update article info.           |
        | 'api/v1/article'           | GET     | Get a article's info.          |
        | 'api/v1/articles'          | GET     | List all articles.             |
        | 'api/v1/article/articles_views'           | GET     | Get the views for this article.         |
        | 'api/v1/article/bookmark'           | GET     | Bookmark this article.         |
        | 'api/v1/article/bookmarks'           | GET     | Get this articles bookmarks.         |
        | 'api/v1/article/comment'           | POST     | Comment on this article.         |
        | 'api/v1/aarticle/comments'           | GET     | Get all comments on this article.         |
        | 'api/v1/article/like'           | GET     | Like this article.         |
        | 'api/v1/article/likes'           | GET     | Get all of this articles likes.         |
        | 'api/v1/article/report'           | POST     | Report this article.         |
        | 'api/v1/article/stats'           | GET     | Get this articles stats.         |
        | 'api/v1/article/tag'           | GET     | Tag this article.         |
        | 'api/v1/article/tags'           | GET     | Get this article's tags.         |
        | 'api/v1/article/unbookmark'           | GET     | Unbookmark this article.         |
        | 'api/v1/article/uncomment'           | POST     | Delete a comment on this article.         |
        | 'api/v1/article/unlike'           | GET     | Unlike this article.         |
        | 'api/v1/article/untag'           | GET     | Untag this article.         |

        This service uses Postgres to store the user info, AWS S3 to store the images, AWS SES to send the emails and celery for the email sending and photo upload.


  2. **Database**

      The application uses Postgres and AWS S3. The postgres database is used to store user details. The AWS S3 bucket is used to store the profile pictures.

  3. **Security**

      The application uses JSON Web Tokens to authorize access to protected routes. The passwords are also encrypted.

  ## Contribution

1. Fork it https://github.com/twyle/repo-template/fork
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## Developer

Lyle Okoth – [@lylethedesigner](https://twitter.com/lylethedesigner) on twitter </br>

[lyle okoth](https://medium.com/@lyle-okoth) on medium </br>

My email is lyceokoth@gmail.com </br>

Here is my [GitHub Profile](https://github.com/twyle/)

You can also find me on [LinkedIN](https://www.linkedin.com/in/lyle-okoth/)

## License

Distributed under the MIT license. See ``LICENSE`` for more information.
