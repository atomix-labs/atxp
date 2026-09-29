# atxp's demo, both themes: an empty repository takes the rust bundle, each variable its default
# but the repository's name, then shows the files it gained, the features still off, and that every
# file matches its profile. `just release` moves the tag to each release.
Require devset
Require git

Hide
Type "cd $(mktemp -d) && mkdir hello && cd hello && git init -q && clear"
Enter
Sleep 500ms
Show

Type "devset add atxp/rust --git https://github.com/atomix-labs/atxp --tag v0.16.0 --var repository=you/hello"
Sleep 600ms
Enter

# The prompt comes back once every file is written.
Wait@30s
Sleep 3s

Hide
Type "clear"
Enter
Show
Type "ls -A"
Sleep 400ms
Enter
Sleep 3s

Type "devset explain rust"
Sleep 400ms
Enter
Wait
Sleep 3s

Hide
Type "clear"
Enter
Show
Type "devset status"
Sleep 400ms
Enter
Wait
Sleep 4s
