# Git-Scrapper
This is a python based scrapper used to scrape top 30 repositories off all the topics on the GitHub

## Scrape the list of topics from Github

### Process.

- use requests to downlaod the page
- user BS4 to parse and extract information
- convert to a Pandas dataframe

#### Project Outline:
- We are going to scrape https://github.com/topics
- We will get a list of topics. For each topic, we'll get topic title, url, and description.
- For each topic we will get top 30 repositories.
- For each repository we will collect repo name, username, start, and url.
- For each topic we will create .csv in this format
- Format for csv file
```
 Repo Name,Username,Stars,Repo URL
 three.js,mrdoob,69700,https://github.com/mrdoob/three.js
```

### Problems Faced
- Initially able to scrape only top 30 topics present on the first page.
- Get connection issue after scraping few topics.

### Problems overcome
- All the issues faced are solved rigorously.
