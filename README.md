# Scribary
<p align="center">  
  <img src="https://raw.githubusercontent.com/mathewjhan/hackumass2020/master/images/logo.png" alt="">
</p>

[video](https://www.youtube.com/watch?v=V3)

[demo](https://ivyhacks-spotifind.herokua.com/)

## Inspiration
**A common struggle in this remote learning era of university is staying focused during lectures.** Issues with internet connections prevent students from watching lectures consistently. Issues with time zones prevent students from attending synchronous lectures. Even subtle issues such as the sound compression of a video lecture versus the engaging reverberations of a live lecture hall cause students to have difficulty paying attention to lecture. Through all the inconveniences of remote learning, **it is clear that the quality of learning has gone down.** During an in-person semester, students learn from classroom discussions, study groups, and office hours. But with no proper classroom environment, many students lose the motivation to stay engaged with course material, and as a result, take lower quality notes.

With time zones and the internet becoming a limiting factor of remote learning, **the BEST and most CONSISTENT way to learn is through the use of quality notes**, which are concise and small in size. However, with all the distractions and nuances of live lecture, it is also difficult to take good notes and sometimes professors don't share the best notes to study off of. Fortunately, over the years students accumulate great amounts of notes that simply end up rotting away on their hard drives. These notes can be especially useful during this time of stymied learning. As good notes are integral for learning the topic, we wanted to alleviate students’ stresses regarding this by creating a way for students to share notes with each other—that is, a library of notes for scribes—a Scribary!


## What it does
<p align="center">  
  <img src="https://raw.githubusercontent.com/mathewjhan/hackumass2020/master/images/upload.png">
</p>

With the importance of notes in mind, we created Scribary, an online platform to improve the note-taking experience. Students can upload notes with descriptors such as title course, affiliated university, and course description. 

<p align="center">  
  <img src="https://raw.githubusercontent.com/mathewjhan/hackumass2020/master/images/notes.png">
</p>

Each file upload is then parsed for context using Google Cloud's NLP machine learning API and assigned with relevant category tags, which can later be used by Scribary users to filter results. In the frontend, once a Scribary user finds notes that are relevant to what they want to learn, the file can be directly accessed with one click, allowing a streamlined experience to find the exact notes that they need.

## How we built it
We built the frontend with **React**, backend with **Python**, and connected the two through **Flask**. Files are stored in an **AWS S3 bucket** and relevant post information in a **Datastax Astra** database. With the help of **Google Cloud’s Natural Language API**, we predicted tags for each upload and determined relevant categories based on a confidence threshold.

<p align="center">  
  <img src="https://raw.githubusercontent.com/mathewjhan/hackumass2020/master/images/scribary.png">
</p>

## Documentation
To reproduce this project locally, first install the necessary libaries with `npm install` and `pip install -r requirements.txt`. You must also have Heroku and the Google Cloud SDK installed to run this project.


Make sure you have the environment variable `$GOOGLE_APPLICATION_CREDENTIALS` set up with the Google Cloud Natural Language API. In addition, make sure you set your AWS credentials and Datastax Astra in your environment.


You can start the project with the command `heroku local`, which runs `gunicorn` on our Flask app. Go to `localhost:5000` to view the web interface.

## Challenges we ran into
One of our greatest difficulties was working with Datastax Astra. Due to our lack of experience working with Cassandra, we had difficulty figuring how their REST query API worked. After hours of reading documentation, we were finally able to create functions that effectively searched the database. Another challenge we came across was linking the backend and frontend. Because some of the data sent over from the frontend was in a complex format, we had to figure out how to correctly serialize the data so that it would be interpreted correctly in the backend.

## Accomplishments that we're proud of
Michael: I’m proud of designing my first web application at a hackathon. Most of my past experience at past hackathons was in embedded systems, so it was a nice change to work on web development! 


Maggie: I’m proud of attending my first hackathon!


Mathew: I'm proud that we were able to complete a working product. When we first started, I thought there was little chance that we would actually create something functional, but we ended up grinding and finishing.


## What we learned
Mathew: I learned a lot about practices in fetching data. Since the data we needed to POST was relatively complex, I had to perform a lot of data manipulation to get it to work.


Maggie: This was my first hackathon, so I learned a lot about how hackathons work, and was also given a basic introduction to machine learning through Google Cloud’s Natural Language API.


Michael: I learned about how to build a full stack web application. Setting up communication between React, Flask, AWS, and Datastax Astra was one of the most difficult parts of the project for us, and I learned a lot from it. 

## What's next for Scribary
There is so much that can be improved with our idea. In the future, we hope to add search functionality, smarter context creation, and support for other file extensions. In addition, we would like to expand our product to not only notes, but learning resources with student crowdsourced categories to allow students to easily narrow down and share resources with each other.


