# edX MongoDB Structure
Below outlines the steps required to connect to the edX MongoDB course back end and collect the
course structure. Eventually these steps will be converted to being done automatically via a
Python script.

## Connect to MongoDB
First, connect to the Mongo database command line and use the edxapp database.
```
> mongo
> use edxapp
```

## Find Course IDs
Next, need to determine what the published course IDs are. Each course has 3 ID values:
 * id - general id for the course, not referenced elsewhere
 * draft-branch - used for drafts as they are created, may not be the same as the published course
 * published-branch - the actual published course and where we want to target

Therefore, capture the published-branch ids:
```
> db.modulestore.active_versions.find( {}, { "versions.published-branch":1, _id:0 }).pretty()
{ "versions" : { "published-branch" : ObjectId("55c3e2db56c02c317615a894") } }
{ "versions" : { "published-branch" : ObjectId("561c649756c02c484b1bb5ec") } }
```

## Get Course Structure
Finally, pull out the course structures from the database using the course IDs found above.
```
> db.modulestore.structures.find( { "_id" : ObjectId('561c649756c02c484b1bb5ec') } ).pretty()
{ "_id" : ObjectId("561c649756c02c484b1bb5ec"), "edited_by" : NumberLong(4), ... }
```

## Reference
A great online JSON formatter to help review the output: http://jsonviewer.stack.hu/

Can also use the .pretty() option
