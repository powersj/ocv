# Online Course Visualizer

## Objective
The goal of this project is to create visualizations of online educational courses. This will help educators understand the methods they are using to teach and assess students. The project helps students understand the course and how it is structured. It is specifically targeted for students and teachers using MOOC platforms, like edX.

![Img of visualization](https://raw.githubusercontent.com/powersj/ocv/master/img/final.jpg "Initial draft")

## Demo, Video, and Paper
 * Check out live demos and examples at the [GitHub Pages here](http://powersj.github.io/ocv)
 * Watch a demonstration of the tool via [a YouTube video!](https://www.youtube.com/watch?v=JN5GK_NYm68)
 * Read the [paper](http://powersj.github.io/ocv/online_course_visualizer.pdf)

## How to Use
### Getting Data
There are three methods for getting the data required to generate the visualizations: 1) use a JSON export (Usually a single file) 2) use an exported course via the XML format (Usually a full directory of files) or 3) connect to an edX instance database and export the course directly.

#### JSON Export
If you already have an export of an edX course via JSON you can use the `edx_course_json.py` script to generate the data. Run the following:

```bash
./edx_course_json.py <path to JSON file>
# an example where the course JSON export is in your downloads folder
./edx_course_json.py ~/Downloads/mycourse.json
```

This will put the data into a single JSON file, containing the correct format to parse, into the 'input' directory.

#### XML Export
If you already have an export of an edX course via XML you can use the `edx_course_xml.py` script to generate the data. Run the following:

```bash
./edx_course_xml.py <path to directory>
# an example where the course export is in your downloads folder
./edx_course_xml.py ~/Downloads/mycourse
```

This will put the data into a single JSON file into the 'input' directory. If the XML export is in an archive (e.g. zip) it needs to be extracted before running the above script.

#### Export directly from edX Database
To automatically connect to an edX database you only need to know the IP address of the backend database and be able to establish a connect to the Mongo database.

**NOTE** This method requires direct access to the MongoDB database used by the edX instance. Unless you are the one setting up the edX instance, you will probably not be granted access to a course in this manner by any network admin. Therefore, one of the above methods is suggested!


To use this method use the `edx_course_db.py` script to generate the data. Run the following:

```bash
./edx_course_db.py <ip address of server>
# an example pointing to localhost
./edx_course_db.py 127.0.0.1
# an example pointing to a remote IP
./edx_course_db.py 192.168.1.100
```

This will put exports of ALL courses on that server, one JSON file per course, into the 'input' directory.

### Generating the Visualization
Now that there is data in the input directory it is time to generate the visualizations themselves. This is accomplished by running the 'edx_course_html.py' script as such:

```bash
./edx_course_html.py <filename>
# Using the mycourse.json file found in the input directory
./edx_course_html.py ../input/mycourse.json
# Same file, but will make all tooltips print the id of the course
./edx_course_html.py ../input/mycourse.json --id-only
```

This will automatically output all the data to the output folder. The output folder has been pre-populated with all the required CSS and Javascript files.

## Background
The continual blending of education together with technology has led to a trend of taking traditional educational experiences and placing courses online with no changes. Prior to the massive open online course (MOOC) revolution, the general online course experience involved students watching lectures, normally recorded in-classroom lectures, and then taking a multiple choice test. If the student passes he moves on to the next set of lectures, but if student does not pass, he is forced to go back and review lectures with little to no guidance or feedback.

The type of online education described above does not take full advantage of new technologies that may exist or that have been enabled by online platforms like MOOCs. As an example, consider methods for providing intelligent feedback to students during assessments. Taking a traditional multiple choice quiz and only making it accessible online ignores the fact that educators could instead be providing real time feedback by mixing and matching additional assessment methods, or analyzing student inputs to determine where there are places in lectures that may need to be refined. Only recently have advances in online education begun to utilize the technologies available to enrich the online experience.

In addition, writing well thought out assessments is incredibly difficult. A teacher needs to spend a considerable time refining and crafting an assessment to help guide a student’s learning. Therefore, enabling teachers to take advantage of the tools and processes available to them in online learning will enable them to be more effective.

Here I present a visualization to enable both teachers and students to view course structure and features.  The goal of this is to assist educators in understanding the methods they are using, or not using, to teach and assess students and to demonstrate to students the course layout and set expectations on how the course is structured.

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

## Contributors
* [Joshua Powers](http://powersj.github.io/)
  * CS6440 Education Technology (Fall 2015)
  * Georgia Institute of Technology

## Reviewers
A huge thank you to the following for their feedback, evaluation, and support:
 * Dr. David A. Joyner
 * Dr. Watler & Marjie Powers
 * Olga Martyusheva
 * Alex Balderson
 * Aaron Anderson
 * Daniel Davis

# License
Apache 2.0 &copy; 2015 Joshua Powers
