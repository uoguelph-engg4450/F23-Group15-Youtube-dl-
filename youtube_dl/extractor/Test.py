from __future__ import unicode_literals
import os
import shutil
import unittest
import youtube_dl

class TestCBSNewsIE(unittest.TestCase):
    def setUp(self):
        self.ydl_opts = {
            'format': 'best',
            'quiet': True,
        }
        self.temp_dir = 'temp'
        os.makedirs(self.temp_dir, exist_ok=True)

    def test_download_video(self):
        url = 'https://www.cbsnews.com/video/your-video-url'  # Replace with a valid CBS News video URL
        ydl = youtube_dl.YoutubeDL(self.ydl_opts)
        result = ydl.extract_info(url, download=True)

        self.assertTrue(result)
        self.assertIn('entries', result)
        self.assertEqual(len(result['entries']), 1)

        video_info = result['entries'][0]
        self.assertIn('id', video_info)
        self.assertIn('title', video_info)
        self.assertIn('url', video_info)
        self.assertTrue(video_info['url'].endswith('.mp4'))

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

if __name__ == '_main_':
    unittest.main()
