from tkinter import *
import feedparser
from smartmirror.api_settings import ApiSettings
from smartmirror.window.news_headline import NewsHeadline
import smartmirror.Logger as Logger
"""
    News Class
"""


class News(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg=ApiSettings.Background)
        self.news_label = Label(self, text='Wiadomości :', font=(ApiSettings.Font, ApiSettings.MediumTextSize),
                                fg=ApiSettings.Foreground, bg=ApiSettings.Background)
        self.news_label.pack(side=TOP, anchor=W)
        self.news_list = None
        self.news_url = "https://news.google.com/rss?hl=pl&gl=PL&ceid=PL:pl"

        self.headlines_container = Frame(self, bg=ApiSettings.Background)
        self.headlines_container.pack(side=TOP)

        self.display_news_number = 5
        self.headlines_iterator = 0
        self.headlines_label_list = [
            NewsHeadline(self.headlines_container) for i in range(self.display_news_number)]

        for headline in self.headlines_label_list:
            headline.pack(side=TOP, anchor=W)

        Logger.logging.debug("Initialization of News class")
        self.get_headlines()
        self.refresh_headlines()

    def refresh_headlines(self):
        for headline in self.headlines_label_list:
            headline.update_headline(self.news_list.entries[self.headlines_iterator].title)
            self.headlines_iterator += 1
            if len(self.news_list) < self.headlines_iterator:
                self.headlines_iterator = 0
        self.headlines_iterator -= self.display_news_number - 1
        # updates every 10s
        self.after(10 * 1000, self.refresh_headlines)

    def get_headlines(self):
        try:
            self.news_list = feedparser.parse(self.news_url)
            Logger.logging.info("Get number of news: {0} from: {1}".format(len(self.news_list), self.news_url))
        except Exception as err:
            Logger.logging.critical("News exception: {0}".format(err))
        # updates every hour
        self.after(60 * 60 * 1000, self.get_headlines)


if __name__ == '__main__':
    pass
