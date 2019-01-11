# NYTMarriageAnnouncements
This parser extracts marriage announcements from the New York Times online database that were published in 2018. Note: this only works for 2018 and beyond as NYT started publishing all announcements on Sundays from 2018 onwards. Furthermore, the 'articleParser2018' function extracts identifiable information, such as the couple's name, when they got married, how they met and when they met, and stores in the form of a list of dictionaries. This information about how and when the couple met is not entirely accurate due to the use of simple string matching, I am developing a way of doing this using Machine Learning. All announcements can then be output into a CSV using the last function.
