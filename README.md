
# BOOKWORLD

BookWorld is my first django+ postgress project,Where Customers can buy thier 
favorite books online. Fully coded from zero not used any templates, Using BootStrap used for fast developement and responsiveness.
## Admin Dashboard
<img width="1440" alt="Screenshot 2022-09-02 at 3 43 59 PM" src="https://user-images.githubusercontent.com/95117275/188118512-ee7ffe14-cbc6-4902-8729-26f91fe93989.png">


## Features

- Custom User Model
- Feature Rich Custom Admin Panel
- PostgreSQL as database
- Fully Responsive
- OTP Login
- Razor Pay ,PayPal Integration


## Run Locally

Clone the project

```bash
  git clone https://github.com/Aravindrajeev432/BOOKWORLD_OFFICIAL.git
```

Go to the project directory

```bash
  cd BOOKWORLD_OFFICIAL
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  cd bookworld
  python3 manage.py runserver - MAC OS,Linux OS
  py manage.py runserver - Windows OS
```


## Appendix

Before Running the project make sure that you are in virtual env


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SECRET_KEY` - Django Secret key

### PayPal
`ACCOUNT_SID`
`AUTH_TOKEN`
`SERVICE`
### Razorpay
`RAZOR_KEY_ID`
`RAZOR_KEY_SECRET`
`OPENEXCHANGEKEY`


### AWS S3 Static Files Configuration
`AWS_ACCESS_KEY_ID `
`AWS_SECRET_ACCESS_KEY `
`AWS_STORAGE_BUCKET_NAME `
