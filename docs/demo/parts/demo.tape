# atxp's demo, both themes: an empty repository takes the rust bundle, each of devset's questions
# answered with its default, then shows the files it gained, the features still off, and that every
# file matches its profile. `just release` moves the tag to each release.
Require devset
Require git

Hide
Type "cd $(mktemp -d) && mkdir hello && cd hello && git init -q && clear"
Enter
Sleep 500ms
Show

Type "devset add atxp/rust --git https://github.com/atomix-labs/atxp --tag v0.9.0 --var repository=you/hello"
Sleep 600ms
Enter

# Each question, its default taken; the prompt comes back once every file is written.
Wait+Screen@30s /GitHub logins/
Sleep 800ms
Enter@350ms 11
Wait@30s
Sleep 2s

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
