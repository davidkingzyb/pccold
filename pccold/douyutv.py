import hashlib
import re
import time
import uuid

from requests.adapters import HTTPAdapter

from streamlink.plugin import Plugin
from streamlink.plugin.api import http, validate, useragents
from streamlink.stream import HTTPStream, HLSStream, RTMPStream

STREAM_WEIGHTS = {
    "low": 540,
    "medium": 720,
    "source": 1080
}

rtmp_url='<rtmp_url>'

_url_re = re.compile(r"""
    http(s)?://
    (?:
        (?P<subdomain>.+)
        \.
    )?
    douyu.com/
    (?:
        show/(?P<vid>[^/&?]+)|
        (?P<channel>[^/&?]+)
    )
""", re.VERBOSE)


class Douyutv(Plugin):
    @classmethod
    def can_handle_url(cls, url):
        return _url_re.match(url)

    @classmethod
    def stream_weight(cls, stream):
        if stream in STREAM_WEIGHTS:
            return STREAM_WEIGHTS[stream], "douyutv"
        return Plugin.stream_weight(stream)

    def _get_streams(self):
        quality = ['source', 'medium', 'low']
        for i in range(0, 3, 1):
            
            if 'rtmp:' in rtmp_url:
                stream = RTMPStream(self.session, {
                        "rtmp": rtmp_url,
                        "live": True
                        })
                yield quality[i], stream
            else:
                yield quality[i], HTTPStream(self.session, rtmp_url)

__plugin__ = Douyutv