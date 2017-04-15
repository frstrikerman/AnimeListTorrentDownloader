import sys, distutils.spawn, re, subprocess

class Download:
    client = None
    workingClient = ['transmission-qt', 'transmission-gtk', 'transmission-cli', 'deluge']
    result = None
    def __init__(self, client, choice, result):
        if result:
            if client == '' or client not in self.workingClient:
                if client == 'transmission':
                    self.workingClient = self.workingClient[:3]
                self.availableClient()
                for i, j in enumerate(self.client):
                    print(str(i + 1) + ":" + j)
                try:
                    trchoice = int(input("Which client do you want to use : "))
                except ValueError:
                    trchoice = int(input("enter a number : "))
                self.client = self.client[trchoice - 1]
                self.useClient(result, choice)

            elif client in self.workingClient:
                self.client = client
                self.useClient(result, choice)
        else:
            print("Do a research before downloading")

    def availableClient(self):
        self.client = []
        for i in self.workingClient:
            if distutils.spawn.find_executable(i) is not None:
                self.client.append(i)

        if not self.client:
            print("error no client found")
            sys.exit(-1)

    def useClient(self, result, choice):
        devnull = open('/dev/null', 'w')
        if self.client == 'deluge':
            torrent = subprocess.Popen(["deluge-gtk add" + " '" + result.getlink(choice) + "'"], shell=True, stdout=devnull)
        elif re.match("transmission-.*", self.client):
            torrent = subprocess.Popen(["%s" % self.client + " '" + result.getlink(choice) + "'"], shell=True, stdout=devnull)
