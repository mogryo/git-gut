# Git-gut
## Description
This is Project in progress and for fun. Idea is - application will analyze is there a technical debt in project. </br>
Many "random" patterns are used here, as a playground, to see them in action and understand if they are applicable in real production applications later. </br>
Right now only shows most active users (contributors), add/delete code ratios in files (and similar info) - so to be short, just statistics. </br>
And yes, this "technical debt level" will be super opinionated. Again, this project is for fun, and try out using patterns all other the place.

## Installation

```bash
Will add this section after Poetry is added.
```

## Running the app
```bash
Will add this section after Poetry is added.
```

## Examples and all options
```bash
Will add this section after Poetry is added.
```

## Rough path to lunch
While I had no time to add Poetry (oh no, 30 mins of my time :D). </br>
In theory you can launch application using Python 3.12 <br/>
Install all packages from requirements.txt (hopefully I have there everything)</br>
Aaaand try for example following 
```bash
--columns=filename,commitcount,mfauthor,daratio,linecount --sort=daratio-desc --filters="linecount>50" ./ --query="SHOW linecount, daratio FROM ./ WHERE linecount > 10 and daratio > 0.1 ORDERBY daratio DESCK and linecount DESC"
```

Note! I have a feeling, if you launch this on an old and active repo, everything will freeze :) Task(issue) for optimization will be done later.