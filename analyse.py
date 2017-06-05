from database_utils import ConnectDB
from values import DATABASE_TV, COLLECTION_ITEM, NUM


class Analyse:
    client = None
    database = None
    collection = None

    def __init__(self):
        self.client = ConnectDB(DATABASE_TV, COLLECTION_ITEM)
        self.database, self.collection = self.client.get_handler()

    def average(self):
        result = {}
        for i in range(10):
            var = 0
            total = 0
            for item in self.collection.find():
                var += len(item["relative"][NUM[i]])
                total +=1
            result[NUM[i]] = var/total
        print(result)

    def export(self, num):
        file = open('result_%s.csv' % str(num), 'w', encoding='utf-8')
        for item in self.collection.find():
            for url in item["relative"][NUM[num]]:
                file.writelines([item["url"],',',url["url"],',',str(url["value"])[0:5],'\n'])
        file.close()
pro = Analyse()
pro.export(9)