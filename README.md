# Online Course Visualizer
The following takes data about edX courses (or other inputs via JSON) and produces a web-based
visualization of the course. This is an effort to help demonstrate how online courses are designed
and to highlight if courses are taking advantage of online assessment techniques and providing
variety.

![alt text](https://raw.githubusercontent.com/powersj/ocv/master/img/final.jpg "Initial draft")

## Background
With the continual blending of education together with technology there is a trend of taking traditional methods and placing them online with no changes. The general experience involves students watching lectures and then students take a multiple choice test, which if they pass they move on to the next set of lectures. If they do not pass, they are forced to go back and review the lectures with little to no guidance as to what the student failed or missed.

This type of online education however does not take full advantage of new technologies that may exist or have been enabled by an online platform. As an example, consider methods for providing intelligent feedback to students during assessments. Taking a multiple choice quiz and making it accessible via online tools ignores the fact that educators could provide realtime feedback, use additional methods of assessment, or analyze student inputs to determine where places in lectures may need to be refined.

In addition, writing good well thought out assessments is incredibly difficult. A teacher needs to spend time refining and crafting an assessment to help guide a student’s learning. As such enabling teachers to take advantage of the tools and processes available to them enables them to be more effective teachers.

## Objective
The goal of this project is to create visualizations of components of an online education course, such as lectures and assessments, to help educators understand the methods they are using to teach and assess students and students to understand how the course is structured. This project is specifically targeted at students and teachers using MOOC platforms, like edX.

## Technologies Used
* **edX**
  * Used as the open source online course platform that the visualizations are based off of
  * Find more information at: https://www.edx.org/
* **Python**
  * Used as the primary coding language of choice
  * The author's favorite
* **d3 and d3-tip**
  * Used to create the visualizations themselves
  * Find more information at: http://d3js.org/ and https://github.com/Caged/d3-tip
* **Font-Awesome**
  * Used throughout the visualizations for icon sets.
  * Learn more about Font-Awesome at: https://fortawesome.github.io/Font-Awesome/
* **Hugo**
  * Used to generate the GitHub page for this project in combination with the Hugo "creative" theme
  * Get both at: https://gohugo.io/ and http://themes.gohugo.io/creative/

## Development Examples
Here was the initial prototype image that was hand-built to demonstrate how the visualizations could look like:
![alt text](https://raw.githubusercontent.com/powersj/ocv/master/img/proto.png "Initial draft")

After getting in, extracting data, and starting to manipulate the data this is the state of the visualizations (think alpha stage):
![alt text](https://raw.githubusercontent.com/powersj/ocv/master/img/alpha.png "Initial working code")

Right before going to peer review for the course, this is what the visualizations looked like in a beta form:
![alt text](https://raw.githubusercontent.com/powersj/ocv/master/img/beta.png "After initial feedback")

## Tests
There are example edX course output in the src/data directory that can be used to build the
visualizations without the need for standing up the entire edX environment.

## Contributors
* [Joshua Powers](http://powersj.github.io/)
  * CS6440 Education Technology (Fall 2015)
  * Georgia Institute of Technology

# License
Apache 2.0 &copy; Joshua Powers
