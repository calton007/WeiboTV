import igraph
from igraph import *
from database_utils import ConnectDB
from values import DATABASE_TV, COLLECTION_URL, DATE_FORMAT
import time

client = ConnectDB(DATABASE_TV, COLLECTION_URL)
database, collection = client.get_handler()
# def remove_duplicate():
#     all, find, delete = 0, 0, 0
#     a = collection.distinct('url')
#     for i in range(collection.count(), 0, -1):
#         all += 1
#         url = collection.find()[i - 1]["url"]
#         if url in a:
#             a.remove(url)
#             find += 1
#         elif url not in a:
#             collection.remove(collection.find()[i - 1])
#             delete += 1
#         print("Unique:%d\t\tDelete:%d\t\tProcess:%d\t\t" % (find, delete, all))
g = Graph(directed = False)
urls = set()
urls.add('index')
re = collection.find()
for url in collection.find():
    urls.add(url["from_url"])
    urls.add(url["url"])
dic = {}
var = 0
for i in urls:
    dic[i] = var
    var += 1
g.add_vertices(len(dic))
for url in collection.find():
    a = dic[url["url"]]
    b = dic[url["from_url"]]
    g.add_edge(b, a)
value = time.localtime(int(time.time()))
dt = time.strftime(DATE_FORMAT, value)
print(dt)
# layout = g.layout_fruchterman_reingold()
visual_style = {}
visual_style["vertex_size"] = 1
visual_style["edge_width"] = 0.3
visual_style["vertex_color"] = 'white'
visual_style["layout"] = g.layout_fruchterman_reingold()
plot(g, **visual_style)
value = time.localtime(int(time.time()))
dt = time.strftime(DATE_FORMAT, value)
print(dt)