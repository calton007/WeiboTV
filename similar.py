import time
import numpy
from numpy import *
from copy import deepcopy
from database_utils import ConnectDB
from values import DATE_FORMAT, DATABASE_TV, COLLECTION_ITEM


class Similar:
    client = None
    database = None
    collection = None

    def __init__(self):
        self.client = ConnectDB(DATABASE_TV, COLLECTION_ITEM)
        self.database, self.collection = self.client.get_handler()

    @staticmethod
    def cosine(a, b):
        return a.dot(b)/sqrt(a.dot(a))/sqrt(b.dot(b))

    def add_tags(self, item, tag_set):
        for t in item["tags"]:
            tag_set.add(t["tag"])
        return tag_set

    def cut_split(self, item):
        comment = item["comments"]
        cut = comment.split('/')
        comment = comment.replace('/','')
        length = len(comment.replace('/',''))
        return comment, cut, length

    def init_vec(self, tags):
        vec = {}
        for i in tags:
            vec[i] = 0
        return vec

    def frequence(self, cut, len, tags):
        vec = self.init_vec(tags)
        for word in cut:
            if word in tags:
                vec[word] += 1.0 / len
        li = list(map(lambda x:x, vec.values()))
        ar = numpy.array(li)
        return ar

    def process(self):
        links = 0
        var = 0
        for item_a in self.collection.find():
            # all = 0
            # pos = 0
            tag = self.add_tags(item_a, set())
            relative = []
            comments_a, cut_a, len_a = self.cut_split(item_a)
            for item_b in self.collection.find():
                if item_a != item_b:
                    tags = self.add_tags(item_b, deepcopy(tag))
                    comments_b, cut_b, len_b = self.cut_split(item_b)
                    vec_a = self.frequence(cut_a, len_a, tags)
                    vec_b = self.frequence(cut_b, len_b, tags)
                    cos = self.cosine(vec_a, vec_b)
                    # all += 1
                    if cos > 0.4:
                        links += 1
                        # pos += 1
                        relative.append({"url":item_b["url"], "value":cos})

                        # print("item_a", end='')
                        # for item in item_a["tags"]:
                        #     print(item["tag"], end='/')
                        # print('\nitem_b',end='')
                        # for item in item_b["tags"]:
                        #     print(item["tag"], end='/')
                        # print('\n')
            self.collection.update({"url":item_a["url"]},{"$set":{"relative":relative}})
            var += 1
            value = time.localtime(int(time.time()))
            dt = time.strftime(DATE_FORMAT, value)
            print("%s\t\tprocesse %d\t\titems:%d" % (dt, var, len(relative)))
pro = Similar()
pro.process()
