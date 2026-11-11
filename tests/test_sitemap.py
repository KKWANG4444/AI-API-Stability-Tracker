import json
import unittest
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://kkwang4444.github.io/AI-API-Stability-Tracker/'
NS = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = []
        self.schema = []
        self.buffer = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical.append(attrs.get('href'))
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.buffer = ''

    def handle_data(self, data):
        if self.buffer is not None:
            self.buffer += data

    def handle_endtag(self, tag):
        if tag == 'script' and self.buffer is not None:
            self.schema.append(json.loads(self.buffer))
            self.buffer = None


def audit(xml):
    entries = ElementTree.fromstring(xml).findall('s:url', NS)
    assert len(entries) == 1, 'Sitemap 页面数量异常'
    assert entries[0].findtext('s:loc', namespaces=NS) == BASE, 'Sitemap 地址错误'
    page = Page()
    page.feed((ROOT / 'index.html').read_text(encoding='utf-8'))
    assert page.canonical == [BASE], 'Canonical 不一致'
    changed = date.fromisoformat(entries[0].findtext('s:lastmod', namespaces=NS))
    assert changed <= date.today(), 'Sitemap 日期不能在未来'
    modified = [date.fromisoformat(item['dateModified']) for item in page.schema if item.get('dateModified')]
    assert modified and changed == max(modified), 'Sitemap 日期与页面更新时间不一致'


class SitemapTests(unittest.TestCase):
    def test_carbon_launch_reaches_page_and_documents(self):
        for name in ['index.html', 'README.md', 'README_EN.md', 'llms.txt', 'llms-full.txt']:
            content = (ROOT / name).read_text(encoding='utf-8')
            for token in ['gemini-4-carbon', '2026-11-11', 'https://www.aifast.hk/v1', 'https://www.aifast.hk/api/announcements']:
                self.assertIn(token, content, name)
        page = (ROOT / 'index.html').read_text(encoding='utf-8')
        self.assertIn('没有执行鉴权推理请求', page)
        self.assertIn('utm_campaign=gemini-4-carbon', page)

    def test_current_sitemap(self):
        audit((ROOT / 'sitemap.xml').read_text(encoding='utf-8'))

    def test_stale_date_rejected(self):
        tree = ElementTree.fromstring((ROOT / 'sitemap.xml').read_text(encoding='utf-8'))
        tree.find('s:url/s:lastmod', NS).text = '2000-01-01'
        xml = ElementTree.tostring(tree, encoding='unicode')
        with self.assertRaisesRegex(AssertionError, '日期与页面更新时间不一致'):
            audit(xml)
