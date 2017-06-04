# WeiboSpider
### 使用说明
#### 开发环境
ubuntu 16.04 LTS</br>
Python 3.6.1</br>
Miniconda 4.3.17</br>
Scrapy 1.3.3</br>
Flask 0.12.1</br>
BeautifulSoup4 </br>
MongoDb 2.6.10</br>


### 使用方法
ubuntu:
<pre><code>~$cd weibo</code></pre>
从热门视频抓取url
<pre><code>~/weibo$ scrapy crawl links </code></pre>
完整获取转发、评论、赞
<pre><code>~/weibo$ scrapy crawl weibotv </code></pre>
只获取转发和300条评论
<pre><code>~/weibo$ scrapy crawl wbtv </code></pre>
