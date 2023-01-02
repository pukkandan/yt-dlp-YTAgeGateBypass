import base64
from yt_dlp.utils import get_first, parse_qs
from yt_dlp.extractor.youtube import YoutubeIE


ACCOUNT_PROXY = 'https://youtube-proxy.zerody.one'
VIDEO_PROXY = 'https://phx.4everproxy.com'


class Youtube_AgeGateBypassIE(YoutubeIE, plugin_name='AGB'):
    _TESTS = [{
        'url': 'Cr381pDsSsA',
        'info_dict': {
            'id': 'Cr381pDsSsA',
            'ext': 'mp4',
            'playable_in_embed': False,
            'live_status': 'not_live',
            'channel_id': 'UCDhvbka47fW1vwOmU3ssGkQ',
            'channel_url': 'https://www.youtube.com/channel/UCDhvbka47fW1vwOmU3ssGkQ',
            'view_count': int,
            'thumbnail': 'https://i.ytimg.com/vi_webp/Cr381pDsSsA/sddefault.webp',
            'comment_count': int,
            'tags': 'count:14',
            'availability': 'needs_auth',
            'duration': 958,
            'uploader_id': 'multilazyazz',
            'categories': ['Film & Animation'],
            'title': 'Some Girls from Equestria have a Fall Formal Fuck-up',
            'uploader': 'Liquid Sky',
            'uploader_url': 'http://www.youtube.com/user/multilazyazz',
            'upload_date': '20150403',
            'channel_follower_count': int,
            'chapters': [{'start_time': 0, 'end_time': 522.0, 'title': '<Untitled Chapter 1>'}, {'start_time': 522.0, 'title': '8:43] Boards of Canada - 1969', 'end_time': 958}],
            'description': 'md5:3789850a3dc23cd55279131a82abcc84',
            'like_count': int,
            'channel': 'Liquid Sky',
            'age_limit': 18,
        }
    }]

    def _download_player_responses(self, url, smuggled_data, video_id, *args, **kwargs):
        AGB_CLIENT = 'web'

        ret = super()._download_player_responses(url, smuggled_data, video_id, *args, **kwargs)
        _, ytcfg, player_responses, player_url, *_ = ret

        is_agegated = any(map(self._is_agegated, player_responses)) \
            and all(self._is_agegated(pr) or self._is_unplayable(pr) for pr in player_responses)

        if is_agegated:
            pr = self._download_json(
                f'{ACCOUNT_PROXY}/getPlayer', video_id,
                'Downloading Zerody API JSON', fatal=False, query={
                    'videoId': video_id,
                    'clientName': self._extract_client_name(ytcfg, AGB_CLIENT),
                    'clientVersion': self._extract_client_version(ytcfg, AGB_CLIENT),
                    'signatureTimestamp': self._extract_signature_timestamp(video_id, player_url, ytcfg),
                    'reason': 'LOGIN_REQUIRED',
                    'startTimeSecs': 0,
                    'client': 'yt-dlp',
                })
            if pr:
                player_responses.append(pr)
                streaming_data = get_first(player_responses, 'streamingData') or {}
                if not self._configuration_arg('no_video_proxy'):
                    streaming_data['_use_proxy'] = True
        return ret

    def _extract_formats(self, streaming_data, *args, **kwargs):
        has_gcr = False
        for f in super()._extract_formats(streaming_data, *args, **kwargs):
            if get_first(streaming_data, '_use_proxy') and parse_qs(f.get('url')).get('gcr'):
                has_gcr = True
                f['url'] = f'{VIDEO_PROXY}/direct/' + base64.b64encode(f['url'].encode()).decode()
            yield f
        if has_gcr:
            self.to_screen('Video formats have GCR. Using proxy for download')


__all__ = []
