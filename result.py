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
        self.returnResult()

    def Processing(self):
        self.url_RSS = self.url_RSS.replace('%title%', self.show_name.replace(' ', '+').replace(':', '%3A').replace(';', '%3B'))
        offset = 1
        tracker_feed = feedparser.parse(self.url_RSS)
        navigable = bool(re.search('%pagenumber%', self.url_RSS))
        while tracker_feed.entries:
            self.url_RSS = self.url_RSS.split()[0] + str(offset) + self.url_RSS.split()[1]
            tracker_feed = feedparser.parse(self.url_RSS)
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
            if not navigable:
                break

    def returnResult(self):
        returnList = dict()
        for i,j in enumerate(self.result):
            infoResult = trackma.AnimeInfoExtractor.AnimeInfoExtractor(j[0])
            returnList[i+1] = [infoResult.name, str(infoResult.episodeStart) + ''.join(
                    "-" + str(infoResult.episodeEnd) if infoResult.episodeEnd != None else ''), str(infoResult.resolution), str(infoResult.subberTag)]
        return returnList

    def getlink(self, choice):
        return self.result[choice][1]
