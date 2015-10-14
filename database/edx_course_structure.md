# edX Course Structure
The following are my findings of the database course structure.

# Overall Format
The course content is stored inside a MongoDB instance. Once the data has been retrieved from the
active versions collection it can then be operated on as a dictionary object in Python.

After a little work also discovered some of this is documented here:
http://edx.readthedocs.org/en/latest/internal_data_formats/course_structure.html

## Level 1 - Content
The first level of the dictionary has the following keys:

* original_version - Not interesting as do not care about version
* previous_version - Not interesting as do not care about version
* blocks - This is the important part where all the data exists
* schema_version - Only see '1', so going to ignore in an effort to get this going ASAP
* edited_on - Not interested in as a date do not need
* edited_by - Not interested in as a value do not care about
* _id - Not interested in, as already have this
* root - Not interested in, just says 'course'

## Level 2 - Blocks
The blocks element is a list of each of the building blocks of a course. Each list element is
another dictionary with the following elements:

* definition - id for each block element
* block_type - the type of element (e.g. problem, about, vertical, chapter, sequential, etc.)
* block_id - some are ids, others are predefined items (e.g. overview, course, short_description, etc.)
* fields - This is a dictionary of values like display name, or the actual assessment text with options. Of note is this dictionary also contains the children key that connections to other ids.
* defaults - My example did not have anything here, probably not needed.
* edit_info - Not interested in as info about edits only.

The block_type, block_id, and fields are the keys needed the most.

## Level 3
Break down what each of the fields above, that are of interest, need to pull in:

### block_type
Going to go ahead and create a white-list of types consisting of:
* chapter
* course
* html
* problem
* sequential
* vertical
* video

Not sure about discussion or html at this time.

### block_id
Simple id value that I will keep.

### fields
From here can get the English readable name and next item via:
* display_name
* children

If there are no children, then it means the the end of a particular unit.

#### Problem
For block types of problems, can get the text for the problems via:
* markdown

#### Video
For block types of video, can get the YouTube video ID via:
* youtube_id_1_0
This can then be used like to fill out a URL like:
https://www.youtube.com/watch?v=[VALUE]

Note that the 1_0 at the end stands for the speed of the video or 1.0 in this case.

Note that videos can have predefined start and end times via:
* start_time
* end_time
This is important in determining the video length as the whole video may not be watched.

#### HTML
These are text based pages that have specific XML files that get loaded.

#### discussion
Appear to have an empty display name, in favor of:
* discussion_category
* discussion_target
