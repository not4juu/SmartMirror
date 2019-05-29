from smartmirror.api_settings import ApiSettings
import smartmirror.Logger as Logger
from tkinter import *
from PIL import Image, ImageTk
import feedparser

class News(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg=ApiSettings.Background)
        self.__news_label = Label(self, text='Wiadomości :', font=(ApiSettings.Font, ApiSettings.MediumTextSize),
                                  fg=ApiSettings.Foreground, bg=ApiSettings.Background)
        self.__news_label.pack(side=TOP, anchor=W)
        self.__news_list = None
        self.__news_url = "https://news.google.com/rss?hl=pl&gl=PL&ceid=PL:pl"

        self.__headlines_container = Frame(self, bg=ApiSettings.Background, highlightthickness=1,highlightbackground="yellow")
        self.__headlines_container.pack(side=TOP)

        self.__display_news_number = 5
        self.__headlines_iterator = 0
        self.__headlines_label_list = [NewsHeadline(self.__headlines_container) for i in range(self.__display_news_number)]

        for headline in self.__headlines_label_list:
            headline.pack(side=TOP, anchor=W)

        Logger.logging.debug("Initialization of News class")
        self.__get_headlines()
        self.__refresh_headlines()

    def __refresh_headlines(self):
        for headline in self.__headlines_label_list:
            headline.update_headline(self.__news_list.entries[self.__headlines_iterator].title)
            self.__headlines_iterator += 1
            if len(self.__news_list) < self.__headlines_iterator:
                self.__headlines_iterator = 0
        self.__headlines_iterator -= self.__display_news_number - 1
        self.after(10 * 1000, self.__refresh_headlines)

    def __get_headlines(self):
        try:
            self.__news_list = feedparser.parse(self.__news_url)
            Logger.logging.info("Get number of news: {0} from: {1}".format(len(self.__news_list), self.__news_url))
        except Exception as err:
            Logger.logging.critical("News exception: {0}".format(err))

        self.after(60 * 60 * 1000, self.__get_headlines)

class NewsHeadline(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg=ApiSettings.Background)

        image = Image.open("icons/news.png")
        image = image.resize((20, 20), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        self.__icon_label = Label(self, bg=ApiSettings.Background, image=photo)
        self.__icon_label.image = photo
        self.__icon_label.pack(side=LEFT, anchor=N)

        self.__headline_text = ""
        self.__headline_text_label = Label(self, text=self.__headline_text,
                                           font=(ApiSettings.Font, ApiSettings.SmallTextSize),
                                           fg=ApiSettings.Foreground, bg=ApiSettings.Background)
        self.__headline_text_label.pack(side=LEFT, anchor=N)

    def update_headline(self, headline_text=""):
        self.__headline_text = headline_text
        self.__headline_text_label.config(text=self.__headline_text)

if __name__ == '__main__':
    pass