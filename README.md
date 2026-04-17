# Information_project
# Idea 

the main idea of the project is about the carrer guide dashboard which it will show the how amny jobs are present in the present and the salary ranges and prediction where we can choose by no.of jobs and salaries are good means that domain as main scope in the future 

# Features implenmented

I implemented this project by collecting the real time data from api's
api's like jooble , adzuna 
fetches the jobs based on the domain keywords
supports the multiple domains and the backgrounds
stores the jobs in the postgressql database

# Implementation 
# frontend

starting i done with the frontend by creating the pages like:
home.html,domain.html,result.html and there js files like:
domain.js,home.js and result.js 

# database creation

then i created the database with the name of the job_dashboard
inside that job_dashboard i created the tables like :
jobs,locatin,salary 
all jobs are stored in database filter by the background and domain

# calling api 

using the fast api i call the api where api can store the data in the database
it will only the attributes which requires like jobs, comapny names, location 
salaries i just filterd with the code and just taking what ever i need for the 
project

# prediction 
it will filter the locatons ,no.f jobs ,job count and top companies


# Backend (FastAPI)

Key Endpoints
POST /fetch-all
→ Fetch jobs for all domains
POST /predict
→ Get filtered jobs + analytics
POST /add-job
→ Add new job manually
DELETE /delete-job/{id}
→ Delete job
edit job
edit-job{id}
# execution
the user can log on using the credentials and then he will navigate to the
homepage there backgrounds willbe there like:
computer science , mechanical,finance, marketing
then if he select then he will navigate to the domain page
there some doamins will there choose one then the job dashboard will seen 
where all the charts and the jobs are shown its fetched from apis 


# main core of project curd operations 
In the dashboard there will be BUTTONS:
1 : add (we can add the job and display )
2 : update/edit (we can edit or update the job by using that)
3 : view ( we can view the job by using the view button)
4 : delete ( we can delete the job by using that button)
these all opereations are connected with the fastapi with backend

# project structure :

frontend/
│
├── login.html
├── home.html
├── domain.html
├── result.html
├── dashboard.html
│
├── css/
│ └── style.css
│
├── js/
│ ├── result.js
│ ├── home.js
│ ├── domain.js
│ └── dashboard.js
│
└── components/
├── navbar.html
└── sidebar.html

backend/
│
├── main.py
├── fetch_jobs.py
├── models.py
├── db.py

# Final Outcome

The final system:

Fetches real-time jobs
Stores them in database
Displays them in dashboard
Provides analytics through charts
Allows full CRUD operations
Has clean and responsive UI


## Commit References

Here’s a bullet-style mapping of commits to files and references:

- **CSS**
  - `Add style.css for frontend styling using W3Schools` → W3Schools CSS tutorials  

- **Frontend Components**
  - `Add sidebar.html component for dashboard navigation` → Project UI design patterns  
  - `Add navbar.html component for site navigation using some chatgpt` → ChatGPT guidance  

- **Frontend Pages**
  - `Add dashboard.html for page layout and better UI (reference: W3Schools)` → W3Schools HTML/CSS tutorials  
  - `Add result.js to handle job results page logic by fastapi and documentation of fast api` → FastAPI docs  
  - `Add login.js to handle login form validation and authentication by js tutorials from w3schools` → W3Schools JS tutorials  
  - 'Add home.js to manage home page interactions using the w3schools` → W3Schools JS tutorials  
  - `Add domain.js to manage domain page interactions by javascript tutorials` → JS tutorials  
  - `Add dashboard.js to handle dashboard page functionality by w3 schools` → W3Schools JS tutorials  

- **Backend**
  - `Create login page` → Own design  
  - `Design home page UI` → Own design  
  - `Implement job fetching logic` → FastAPI docs  
  - `Create API schemas using Pydantic` → Pydantic documentation  
  - `Add database models` → SQLAlchemy / FastAPI guides  
  - `Refactor main FastAPI application and improve API flow` → FastAPI docs  
  - `Update database connection logic using the chatgpt` → ChatGPT guidance  
  - `adding the database connection db.py by taking the reference from chatgpt` → ChatGPT guidance  

- **Domain Pages / JS**
  - `Add HTML for domain selection page using the w3 schools` → W3Schools HTML  
  - `Add JS for home page background selection functionality using chatgpt` → ChatGPT guidance  

- **Cleanup**
  - `Remove old JS and CSS files after restructuring the folders for safe and clean` → Project refactoring  
**Execution Flow**
User logs in with credentials
Selects background (e.g., Computer Science)
Selects domain (e.g., Data Science)
System fetches job data from APIs
Data is stored in PostgreSQL
Dashboard displays:
Job listings
Analytics charts
Salary distribution
Company trends
curd functions
**Backend Base URL**:http://54.211.124.103:8000/docs
**Frontend**:http://54.211.124.103:8000/static/home.html
http://54.211.124.103:8000/docs