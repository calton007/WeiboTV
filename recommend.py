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
        self.video_set = self.item_c.find({"forwards.forward_usercard": user})
        ran = self.video_set.count()
        return self.video_set[random.randrange(ran)]["url"]
        # return self.item_c.find_one({"forwards.forward_usercard": user})["url"]

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
        # print(sort)
        recommend = []
        for (u,v) in sort:
            if len(recommend) > 20:
                break
            else:
                if v >= self.similar * 0.1:
                    # print('yes')
                    recommend.append(u)
                else:
                    break
        # for i in range(40):
        #     try:
        #         if sort[i][0] > self.similar * 1.1:
        #             recommend.append(sort[i][0])
        #     except:
        #         break
        # print(recommend)
        # print(recommend)
        return recommend

    def process(self):
        global PICKED
        global USERS
        user_num = 30
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
            item = self.group_c.find_one({"url": url})
            group = self.get_group(item)
            recommend = self.get_videos(group, item)
            watched = self.get_watched(user)
            # print("watch:", watched)
            # print("recommend:", recommend)
            correct = 0
            total = len(recommend)
            t= len (watched)
            for video in recommend:
                if video in watched:
                    correct += 1
            try:
                rate += correct/total
                rate2 += correct/t
                file.write("%s\t\t%s\t\t%s\n" % (user, str(correct/total), str(correct/t)))
                print(user, correct/total, correct/t)
            except ZeroDivisionError:
                # print("no recommend")
                user_num -= 1
        p = rate/user_num
        r = rate2/user_num
        print("======================================")
        print("average:%lf\t\t%lf\t\tscore:%lf\n" % (p, r, 2 * p * r / (p + r)))
        file.write("average:%lf\t\t%lf\t\tscore:%lf\n" % (p, r, 2 * p * r / (p + r)))

# file = open('search.txt','w')
# for i in range(10):
#     file.write("===================================================================\n")
#     pro = Recommend('search', i)
#     pro.process()
# file.close()
# file = open('full.txt','w')
# for i in range(10):
#     file.write("===================================================================\n")
#     pro = Recommend('full', i)
#     pro.process()
# file.close()
file = open('accurate.txt','w')
for i in range(10):
    file.write("===================================================================\n")
    pro = Recommend('accurate', i)
    pro.process()
file.close()