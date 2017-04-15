import feedparser, re
import trackma.AnimeInfoExtractor


class Result:
    result = []
    url_RSS = None
    show_name = None
    show_ep = None
    quality = None
    def __init__(self, url_RSS, show_name, show_ep, quality):
        self.url_RSS = url_RSS
        self.show_name = show_name
        self.show_ep = show_ep
        self.quality = quality
        self.Processing()
        self.showResult()

    def Processing(self):
        #try:
            self.url_RSS += '&term=' + self.show_name.replace(' ', '+').replace(':', '%3A').replace(';', '%3B')
            offset = 1
            url = self.url_RSS + '&offset='
            tracker_feed = feedparser.parse(url)
            while tracker_feed.entries:
                tracker_feed = feedparser.parse(url + str(offset))
                offset += 1
                for i in tracker_feed.entries:
                    animeinfo = trackma.AnimeInfoExtractor.AnimeInfoExtractor(i.title)
                    if self.quality is None and self.show_ep is None:
                        self.result.append([i.title, i.links[0]['href']])
                    elif self.quality is None and animeinfo.getEpisodeNumbers() == (self.show_ep, None):
                        self.result.append([i.title, i.links[0]['href']])
                    elif self.show_ep is None and re.match('.*' + self.quality.replace('p', '') + '.*',
                                                           animeinfo.resolution):
                        self.result.append([i.title, i.links[0]['href']])
                    elif self.quality is not None and self.show_ep is not None and self.show_ep is None and re.match('.*' + self.quality.replace('p', '') + '.*',animeinfo.resolution) and animeinfo.getEpisodeNumbers() == (self.show_ep, None):
                            self.result.append([i.title, i.links[0]['href']])

    def showResult(self):
        if self.result:
            print(
                "| Index   show                                                        episode     resolution      Fansub        URL")
            for j, i in enumerate(self.result):
                infoResult = trackma.AnimeInfoExtractor.AnimeInfoExtractor(i[0])
                display = str(j + 1)
                while len(' ' + display + str(j + 1) + ' ') < 9:
                    display = " " + display + " "
                display = "|" + display + infoResult.name
                while len(display) < 70:
                    display += ' '
                episode = str(infoResult.episodeStart) + ''.join(
                    "-" + str(infoResult.episodeEnd) if infoResult.episodeEnd is not None else '')
                while len(' '+episode+' ') < 10:
                    episode = ' ' + episode + ' '
                display += episode
                resolution = infoResult.resolution
                while len (' ' + resolution + ' ') < 18:
                    resolution = ' ' + resolution + ' '
                fansub = infoResult.subberTag
                while len(' ' + fansub + ' ') < 15:
                    fansub = ' ' + fansub + ' '
                display += resolution
                display+= fansub
                display += "  " + i[1]
                print(display)
    def getlink(self, choice):
        return self.result[choice][1]
