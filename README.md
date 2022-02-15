# Portfolio-project

## Run to config
```
docker-compose config
```
## Run to build
```
docker-compose build
```
## Run to rebuild
```
docker-compose up --build
docker-compose up -d  
```
## Run to stop 
```
docker-compose stop
```
## Run to remove
```
docker-compose rm
docker-compose down
```

@startuml System_Application
scale 1.5 
!define DARKBLUE
!includeurl https://raw.githubusercontent.com/Drakemor/RedDress-PlantUML/master/style.puml
package System_Application{ 
package Errors_Blueprint {
class Errors {
 # forbidden()
 # Page_Not_found()
 # server_errors()
  }
}

package Admin_Blueprint {
class Admin {
  + index()
  + About() 
  + Contact()
  + Project()
  + Resume()
  }
}

Errors -- Admin
Errors -- User

package User_Models {
class User{
    + UserID: integer
    + Email: string
    + Profile: string
    # Password: string
    + Posts: relationship()
    # Get_reset_token()
    # Verify_reset_token()
}
class Post{
    + PostID:string
    + Title: string
    + Published: date
    + conten: string
}
User "1" *-- "n" Post
}

package Posts_Plueprint{
class PostForm{
 + Title:  String
 + Content: String
 + Submit: Submit
  }
  class SearchForm{
 + Title: String
 + Conten: TextArea
 + Submit: Submit
 }
class Posts {
  + Create_posts()
  + Post(post_id)
  + Update_posts(post_id)
  + Delete_posts(post_id)
}
PostForm -* Posts 
Posts -* SearchForm
User -* SearchForm

}

package Users_Plueprint{
class RegistrationForm{
  + Username: String
  + Email: String
  # Password: Password
  # Confirm: Password
  + Submit: Submit
  # Validate_username()
  # Validate_email()
}

class LoginForm{
  + Email: Stringfield
  # Password: PasswordField
  + Remember: BooleanField
  + Submit: SubmitField
}

class UpdateAccountForm {
 + Username: String
 + Email: String
 + Picture: File
 + Submit: Submit
 # Validate_username()
 # Validate_email()
}

class RequestResetForm{
 + Email: String
 + Submit: Submit
 # Validate_email()
}
class ResetPasswordForm{
  # Password: Password
  # Confirm: Password
  + Submit: Submit
}

 RegistrationForm -* LoginForm
 LoginForm -* UpdateAccountForm
 UpdateAccountForm -*  ResetPasswordForm
 ResetPasswordForm -* RequestResetForm 
 PostForm *- RequestResetForm
}
@enduml
