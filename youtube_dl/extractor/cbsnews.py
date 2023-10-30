
# coding: utf-8
from __future__ import unicode_literals

import re
import zlib
from youtube_dl.utils import ExtractorError
from .common import InfoExtractor
from .cbs import CBSIE
from ..compat import (
    compat_b64decode,
    compat_urllib_parse_unquote,
)
from ..utils import parse_duration

class CBSNewsEmbedIE(CBSIE):
    IE_NAME = 'cbsnews:embed'

    def _real_extract(self, url):
        video_id = self._match_id(url)

        # Download the webpage
        webpage = self._download_webpage(url, video_id)

        # Extract the embed URL
        embed_url = self._search_regex(
            r'data-src=["\'](https?://www\.cbsnews\.com/embed/video/[^#]+#[^"\']+)["\']',
            webpage, 'embed URL')

        if embed_url:
            return self.url_result(embed_url)

        self.to_screen('No embed URL found, trying alternative method')

        # Extract the JSON payload
        item_id = self._search_regex(
            r'CBSNEWS\.defaultPayload\s*=\s*({.+?});', webpage, 'JSON payload')

        if item_id:
            item_data = self._parse_json(item_id, video_id)
            mpxRefId = item_data.get('mpxRefId')

            if mpxRefId:
                return self._extract_video_info(mpxRefId, 'cbsnews')

        raise ExtractorError('No embed URL or valid video info found')

class CBSNewsEmbedIE(CBSIE):
    IE_NAME = 'cbsnews:embed'
    _VALID_URL = r'https?://(?:www\.)?cbsnews\.com/embed/video[^#]*#(?P<id>.+)'

    def _real_extract(self, url):
        video_data = self._parse_json(zlib.decompress(compat_b64decode(
            compat_urllib_parse_unquote(self._match_id(url))),
            -zlib.MAX_WBITS).decode('utf-8'), None)['video']['items'][0]
        return self._extract_video_info(video_data['mpxRefId'], 'cbsnews')

class CBSNewsIE(CBSIE):
    IE_NAME = 'cbsnews'
    IE_DESC = 'CBS News'
    VALID_URL = r'https?://(?:www\.)?cbsnews\.com/(?:news|video)/(?P<id>[\da-z-]+)'

    def _real_extract(self, url):
        display_id = self._match_id(url)

        # Download the webpage
        webpage = self._download_webpage(url, display_id)

        entries = []
        for embed_url in re.findall(r'<iframe[^>]+data-src="(https?://(?:www\.)?cbsnews\.com/embed/video/[^#]*#[^"]+)"', webpage):
            entries.append(self.url_result(embed_url, CBSNewsEmbedIE.ie_key()))
        if entries:
            return self.playlist_result(
                entries, playlist_title=self._html_search_meta(['og:title', 'twitter:title'], webpage),
                playlist_description=self._html_search_meta(['og:description', 'twitter:description', 'description'], webpage))

        # Extract JSON data
        item_data = self._parse_json(self._html_search_regex(
            r'CBSNEWS\.defaultPayload\s*=\s*({.+})',
            webpage, 'video JSON info'), display_id)

        return self._extract_video_info(item_data['items'][0]['mpxRefId'], 'cbsnews')

class CBSNewsLiveVideoIE(InfoExtractor):
    IE_NAME = 'cbsnews:livevideo'
    IE_DESC = 'CBS News Live Videos'
    _VALID_URL = r'https?://(?:www\.)?cbsnews\.com/live/video/(?P<id>[^/?#]+)'

    def _real_extract(self, url):
        display_id = self._match_id(url)

        # Download video info JSON
        video_info = self._download_json(
            'http://feeds.cbsn.cbsnews.com/rundown/story', display_id, query={
                'device': 'desktop',
                'dvr_slug': display_id,
            })

        formats = self._extract_akamai_formats(video_info['url'], display_id)
        self._sort_formats(formats)

        return {
            'id': display_id,
            'display_id': display_id,
            'title': video_info['headline'],
            'thumbnail': video_info.get('thumbnail_url_hd') or video_info.get('thumbnail_url_sd'),
            'duration': parse_duration(video_info.get('segmentDur')),
            'formats': formats,
        }
