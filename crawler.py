from selectors import DefaultSelector, EVENT_WRITE

selector = DefaultSelector()

urls_todo = set(['/'])
seen_urls = set(['/'])

class Fetcher:
    def __init__(self, url):
        self.responser = b'' # Empty array of bytes.
        self.url = url
        self.sock = Nona

    # Method on Fetch class.
    def fetch(self):
        self.sock = socket.socket()
        self.sock.setblcoking(False)
        try:
            self.sock.connect(('google.com', 80))
        except BlockingIOError:
            pass

        # Register next call back.
        selector.register(self.sock.fileno(),
                            EVENT_WRITE,
                            self.connected)
    # Callback for connected.
    def connected(self, key, mask):
        print('connected')
        selector.unregister(key.fd)
        request = 'GET {} HTTP/1.0\r\nHost: goole.com\r\n\r\n'.format(self.url)
        self.sock.send(request.encode('ascii'))

        # Register the next callback.
        selector.register(key.fd,
                              EVENT_WRITE,
                              self.read_response)

    #  Callback to process the server's reply
    def read_responser(self, key, mask):
        global stopped

        chunk = self.sock.recv(4096) #4k chunk size
        if chunk:
            self.response += chunk
        else:
            selector.unregister(key.fd) # Done reading
            links = self.parse_links()

            # Python set-logic:
            for link in links.difference(seen_urls):
                urls_todo.add(link)
                Fetcher(link).fetch() # <- New Fetcher.

            seen_urls.update(links)
            urls_todo.remove(self.url)
            if not urls_todo:
                stopped = True
