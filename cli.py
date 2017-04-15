
import sys, getopt
import download, result

class Cli:
    help = {
        'search': 'Usage : search show <name> {ep} <number_episode> {res} <resolution>\n {} : not mandatory\n <> argument',
        'download': 'Usage : download <number> client <torrent_client>'}
    results=None
    def __init__(self, args):
        if len(args) == 1:
            self.prompt()
        elif args:
            self.args(args)

    def args(self, argv):
        show_ep = None
        quality = None
        torrent_client = str()
        show_name = None
        url_RSS = 'https://www.nyaa.se/?page=rss&cats=1_0'

        try:
            opts, args = getopt.getopt(argv, "hc:u:s:n:q:", ["help", "client=", "url=", "show=", "num=", "quality="])
        except getopt.GetoptError:
            print(help)
            sys.exit(2)
        for opt, arg in opts:
            if opt == "":
                self.prompt()
            elif opt in ("-h", "help"):
                print(help)
                sys.exit()
            elif opt in ("-c", "--client"):
                torrent_client = arg
            elif opt in ("-u", "--url"):
                url_RSS = str(arg)
            elif opt in ("-s", "--show"):
                show_name = arg
            elif opt in ("-n", "--num"):
                show_ep = int(arg)
            elif opt in ("-q", "--quality"):
                quality = arg
        if show_name == None:
            show_name = input('enter show name')

        self.results = result.Result(url_RSS, show_name, show_ep, quality)


    def prompt(self):
        show_ep = None
        quality = None
        torrent_client = str()
        show_name = []
        url_RSS = 'https://www.nyaa.se/?page=rss&cats=1_0'
        prompt = input("enter command >>> ").split(" ")
        while prompt[0] not in ['search', 'download', 'help', 'exit']:
            print('enter a proper command\n if you want the command list type help ')
            self.prompt()
        if prompt[0] == 'exit':
            exit(0)
        if prompt[0] == 'search':
            if len(prompt) == 1 or 'show' not in prompt[1:]:
                print(self.help['search'])
                self.prompt()
            else:
                try:
                    for show_result in prompt[prompt.index('show')+1:]:
                        if show_result == 'ep' or show_result == "res":
                            break
                        else:
                            show_name.append(show_result)
                    show_name = " ".join(show_name)
                except IndexError:
                    print('Missing name')
                    print(self.help[prompt[0]])
                    self.prompt()
                if 'res' in prompt[1:]:
                    try:
                        quality = prompt[prompt.index('res') + 1]
                    except IndexError:
                        print('Missing resolution')
                        print(self.help[prompt[0]])
                        self.prompt()
                if 'ep' in prompt[1:]:
                    try:
                        show_ep = int(prompt[prompt.index('ep') + 1])
                    except IndexError:
                        print('Missing number')
                        print(self.help[prompt[0]])
                        self.prompt()
            self.results = result.Result(url_RSS, show_name, show_ep, quality)
            self.prompt()
        if prompt[0] == 'help':
            if len(prompt) == 1 or prompt[1] not in self.help.keys():
                print('available help :')
                for help in self.help.keys():
                    print('help ' + str(help))
            elif prompt[1] in self.help.keys():
                print(prompt[1] + ' help : ' + self.help[prompt[1]])
            self.prompt()
        if prompt[0] == 'download':
            if len(prompt) == 1:
                print(self.help[prompt[0]])
            else:
                try:
                    if len(prompt) == 2 and self.results:
                        download.Download(None, int(prompt[1])-1, self.results)
                except UnboundLocalError:
                    print("do a research before downloading")
            self.prompt()


if __name__ == "__main__":
    i = Cli(sys.argv[1:])
