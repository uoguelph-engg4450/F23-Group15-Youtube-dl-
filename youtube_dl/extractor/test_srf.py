from __future__ import unicode_literals
import os
import shutil
import unittest
import youtube_dl

class Testsrf(unittest.TestCase):
    def setUp(self):
        self.ydl_opts = {
            'format': 'best',
            'quiet': True,
        }
        self.temp_dir = 'temp'
        os.makedirs(self.temp_dir, exist_ok=True)

    def test_download_video(self):
        url = 'https://www.srf.ch/audio/maloney/frohe-weihnachten?id=12304744'  # Replace with a valid srf News video URL
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

if __name__ == '__main__':
    unittest.main()