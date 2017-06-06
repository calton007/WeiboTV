from values import DATABASE_TV, COLLECTION_ITEM, NUM
from database_utils import ConnectDB
import random

PICKED = False
USERS = []

class Recommend:
    client = None
    database = None
    users_c = None
    users = None
    item_c = None
    group_c = None
    video_set = None
    similar = 0

    def __init__(self, cut='search', similar=2):
        self.client = ConnectDB(DATABASE_TV, 'users')
        self.database, self.users_c = self.client.get_handler()
        self.users = []
        self.item_c = self.database.get_collection('WeiboItem_similar_search')
        collection = 'WeiboGroup_' + cut
        self.group_c = self.database.get_collection(collection)
        self.similar = similar

    def pick_user(self, num=20):
        length = self.users_c.count()
        result = self.users_c.find()
        for i in range(num):
            self.users.append(result[random.randrange(length)]["usercard"])
        # print(self.users)

    def pick_a_video(self, user):
        # self.video_set = self.item_c.find({"forwards.forward_usercard": user})
        # ran = self.video_set.count()
        # return self.video_set[random.randrange(ran)]["url"]
        return self.item_c.find_one({"forwards.forward_usercard": user})["url"]

    def get_watched(self,  user):
        watched = []
        for video in self.item_c.find({"forwards.forward_usercard":user}):
            watched.append(video["url"])
        return watched

    def get_group(self, item):
        try:
            group = item[str(self.similar)]
        except:
            if self.similar == 0:
                raise ValueError("wrong similar!")
            else:
                self.similar -= 1
                group = self.get_group(item)
        return group

    def get_videos(self, group, source):
        temp = []
        source = self.item_c.find_one({"url":source["url"]})
        for item in self.group_c.find({str(self.similar):group}):
            temp.append(item["url"])
        all = {}
        for items in source["relative"]["zero"]:
            if items["url"] in temp:
                all[items["url"]] = items["value"]
        sort = sorted(all.items(), key=lambda item:item[1], reverse=True)
        # print("all", all)
        # print("length:",len(all))
        recommand = []
        # for (u,v) in sort:
        #     recommand.append(u)

        for i in range(20):
            try:
                recommand.append(sort[i][0])
            except:
                break
        # print(recommand)
        return recommand

    def process(self):
        global PICKED
        global USERS
        user_num = 100
        if not PICKED:
            self.pick_user(user_num)
            USERS = self.users
            PICKED = True
        else:
            self.users = USERS
        rate = 0
        rate2 = 0
        for user in self.users:
            url = self.pick_a_video(user)
            # print(url)
            item = self.group_c.find_one({"url": url})
            # print(item)
            group = self.get_group(item)
            recommand = self.get_videos(group, item)
            watched = self.get_watched(user)

            # print("watch:", watched)
            # print("recommand:", recommand)
            correct = 0
            total = len(recommand)
            t= len (watched)
            for video in recommand:
                if video in watched:
                    correct += 1
            rate += correct/total
            rate2 += correct/t
            file.write("%s\t\t%s\t\t%s\n" % (user, str(correct/total), str(correct/t)))
            print(user, correct/total, correct/t)
        p = rate/user_num
        r = rate2/user_num
        print("average:%lf\t\t%lf\t\tscore:%lf\n" % (p, r, 2 * p * r / (p + r)))
        file.write("average:%lf\t\t%lf\t\tscore:%lf\n" % (p, r, 2 * p * r / (p + r)))

file = open('search.txt','w')
for i in range(10):
    file.write("===================================================================\n")
    pro = Recommend('search', i)
    pro.process()
file.close()
file = open('full.txt','w')
for i in range(10):
    file.write("===================================================================\n")
    pro = Recommend('full', i)
    pro.process()
file.close()
file = open('accurate.txt','w')
for i in range(10):
    file.write("===================================================================\n")
    pro = Recommend('accurate', i)
    pro.process()
file.close()