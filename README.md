google calendar events
======================

How to create api credential file:

1. go to https://console.developers.google.com/
2. click dashboard
3. create project
4. name the project something
5. leave org option and save
6. at the top of the next page search for `calendar`
7. select `Google Calendar API`
8. click `enable`
9. click `API's & Services` small text in the top left corner
10. click `credentials` and `Create credentals`, then `Oauth client id`
11. set app type to `Other`
12. click on `OAuth consent screen`
13. make up an app name
14. under scope, select option: `View events on all your calendars` with readonly lock icon
13. save
14. click on `credentails` again and there will be a download option beside your credentail. Download the `.json` file and save to the same directory as the script and rename to `api_secrets.json`
15. run the script and a browser should popup prompting to allow the application.
16. once you have provided consent, the script should now work.

Install script dependencies (Python 3.x)
`pip install -r requirements.txt`
