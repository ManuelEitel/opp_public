Published at 75% of being at v1.0
This application does still need some hours of work. Beware!

This is a software that is freely usable for anyone - I've written every line of code myself and intend to further this tool over the time to come.
It is not ready by any means. The finished V1.0 is to be expected within the next few weeks. 

What's this?
* A tool for a company of mid size, that produces non standart products of any kind, that helps organizing the work steps for the Operations Manager, or whoever makes the ToDos for the production colleagues.
* It's name is operator production process, or short: opp

What does it do and how does it work?
* OPP needs to be feeded the workflows that are attached to products.
* The products come in as requests from customers.
* OPP works with a sqlite3 database, since most companies, who are smaller and midsized would not need more speciality. Also, a bigger company can just rewrite the functions that interact with the database.
* OPP has a main window, that shows the currently produced products of the company in a table with all its important information.
* The buttons next to the table are for the controlling of the tasks, that are linked to a product.
* The operator distributes tasks according to the respective workflows onto the colleagues of the production team.
* The production team member then can login themselves, but only see their work schedule and click through it to book work hours and reports. This task is very quick and can be directly linked to any companies main organisation program.
* It can be accessed from multiple PCs, if the databases are being correctly placed at a common direction.
* Each user has one of the roles and permissions, that are involved into the process of a production chain. Starting from the member of the production team, up to the CEO of the company. The sales department has some insight, aswell as the management. That's how they are supposed to be able to make good decisions in the company.

So the idea is, that through distributing the tasks via a individually programmable workflow inside the UI the shift supervisor created automatically the data needed to track the production process and maintain ist, aswell as develop it.

What is V1.0 going to have?
V1.0 OPP is going to have a fully functioning work schedule with replanning.

ToDo's: In the code. 
- A main one is the rescheduling of tasks of production members.
- Drag and Drop feature in the rescheduling process needs to be more slick.
