Mongo commands to get course data
###
'''
> mongo
> use edxapp
'''

Go find all the published classes
###
'''
> db.modulestore.active_versions.find( {}, { "versions.published-branch":1, _id:0 }).pretty()
{ "versions" : { "published-branch" : ObjectId("55c3e2db56c02c317615a894") } }
{ "versions" : { "published-branch" : ObjectId("561c649756c02c484b1bb5ec") } }
'''

Get Course Structure
###
* Then foreach of the classes go get the structure
* http://jsonviewer.stack.hu/
'''
> db.modulestore.structures.find( { "_id" : ObjectId('561c649756c02c484b1bb5ec') } ).pretty()
{ "_id" : ObjectId("561c649756c02c484b1bb5ec"), "edited_by" : NumberLong(4), ... }
'''

Build course structure from JSON
###
* Get JSON
* Look at children field to build map
* TODO: Create more complex example or use the example course
