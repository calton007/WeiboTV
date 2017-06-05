from values import DATABASE_TV, COLLECTION_ITEM
from database_utils import ConnectDB
import random


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
        self.item_c = self.database.get_collection(COLLECTION_ITEM)
        collection = 'WeiboGroup_' + cut
        self.group_c = self.database.get_collection(collection)
        self.similar = similar

    def pick_user(self, num=20):
        length = self.users_c.count()
        result = self.users_c.find({})
        for i in range(num):
            self.users.append(result[random.randrange(length)]["usercard"])
        # print(self.users)

    def pick_a_video(self, user):
        self.video_set = self.item_c.find({"forwards.forward_usercard": user})
        ran = self.video_set.count()
        return self.video_set[random.randrange(ran)]["url"]

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

    def get_videos(self, group):
        recommend = []
        for item in self.group_c.find():
            recommend.append(item["url"])
        # print(recommend)
        return recommend

    def process(self):
        self.pick_user()
        rate = 0
        for user in self.users:
            url = self.pick_a_video(user)
            # print(url)
            item = self.group_c.find_one({"url": url})
            # print(item)
            group = self.get_group(item)
            recommend = self.get_videos(group)
            watched = self.get_watched(user)
            # print(watched)
            correct = 0
            total = len(watched)
            for video in recommend:
                if video in watched and video != url:
                    correct += 1
            rate += correct/total
            print(user,correct/total)
        print("average:%lf" % (rate/20))

pro = Recommend('search', 4)
pro.process()