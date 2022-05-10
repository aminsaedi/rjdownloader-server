#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json
import re
import requests


hostName = "0.0.0.0"
serverPort = 8080


def get_download_link(link):
    media_type = re.split(r"/", link)[3]
    file_name = re.split(r"/", link)[5]

    session = requests.Session()
    response = session.get(
        f"https://www.radiojavan.com/{media_type}/{media_type[:-1]}_host/?id={file_name}")
    base_url = str(json.loads(response.text)["host"])
    if media_type == "podcasts":
        return f"{base_url}/media/podcast/mp3-256/{file_name}.mp3"
    elif media_type == "mp3s":
        return f"{base_url}/media/mp3/{file_name}.mp3"
    elif media_type == "videos":
        return f"{base_url}/media/music_video/hq/{file_name}.mp4"
    else:
        return None


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):

        query = urlparse(self.path).query
        splittedQuery = query.split('=')
        if(len(splittedQuery) == 2):
            url = splittedQuery[1]
            if ("www.radiojavan.com" in url):
                download_link = get_download_link(url)
                self.send_response(302)
                self.send_header('Location', download_link)
                self.end_headers()
            if ("rj.app" in url):
                headers = requests.head(url).headers
                long_url = headers.get('Location')
                download_link = get_download_link(long_url)
                self.send_response(302)
                self.send_header('Location', download_link)
                self.end_headers()

        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
            self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(
                bytes("<p>This is an example web server.</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
