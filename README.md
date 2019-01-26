**note: this project has been discontinued for now. there are far too many different cases and broken post files to even begin bothering attempting to fix how badly tumblr's exporter is. this current version can attempt to match referenced media in html files to files that are local in the media folder, but it cannot account for files that tumblr does not feel like exporting correctly.**

# localizr-lite
attempts to fix tumblr's terrible blog export archive, project 1/2

the intent is to localize a tumblr data backup. the current data backup that tumblr provides has an abysmal folder hierarchy and is very hard to use. there are two ways of viewing your posts:
- all at once via a 100MB (66,000 posts) XML file with no formatting
- one by one (~~66,000 posts results in 66,000 html files)

in addition to this, images for __photosets__ use tumblr image urls, so if tumblr removes the image from their servers, the .html with that post no longer functions properly. this photoset issue is the sole problem localizr-lite aims to fix.

install requirements file and run!

if it doesn't work right for you, i dunno!