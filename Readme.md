Job Tracking Application 

High level functions :  add Job option (which will scrape )

Architecture: CLI (BECauae it is platform indenpendant and no need to Login)
Stack : Python 
Problem statement : how to scrape skills from a job post ?

Process Flow: 
Step 1: So user will choose the directory where he wants to save the Sheet 
	Either : Default (current directory )or custom path

Step 2 ; if file already exists edit that or create new one 

Step 3 : paste link of the naukri JOB Post

Step 4 : tool will extract the skills, company name , date time added, Location , Salary Range,  Job Title/ Role , Link of that Post (to read job description) into one excel , experience required
Hyper link for company name and Rolename to redirect it 

Step 5 : Prompt user to add new URL or CTRL C to exit
