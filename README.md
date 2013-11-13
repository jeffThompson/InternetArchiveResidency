Internet Archive Residency
========================

Working files and documentation for [a curatorial residency](http://jeff-thompson-iatr.tumblr.com/) with the [Internet Archive](http://www.archive.org), algorithmically-curating a series from the archive's collection.

Using the 250-most-frequent unique words in the oldest text in [Project Gutenberg](http://archive.org/details/gutenberg), ["Old Mortality, Volume 2"](http://archive.org/details/mrt2w10) by Sir Walter Scott*, each word is used as a seed for a new search into the Archive. The Most common word in the resulting text is used as a new search term. The process is repeated until the search returns no results.

_*While likely not the oldest text, "Old Mortality" is the oldest text with a date listed._

####Most Frequent Word Search  
The main code used to create this project; loads the text, does the searching, and posts to Tumblr.

####Tumblr Theme  
Source code for the Tumblr theme; will be expanded and released shortly as 'Clustr'.

####Experiments And Other Tests  
Misc and early experiments for the project. Includes a mass downloader, PDF brightness search, random usenet excerpt, and theme tests.

\- \- \-  
All code released under a [Creative Commons BY-NC-SA License](http://creativecommons.org/licenses/by-nc-sa/3.0/) - feel free to use, but [please let me know](mailto:mail@jeffreythompson.org). All other content via the [Internet Archive](http://www.archive.org).