from .DBConnection import DBConnection
from .CountWords import CountWords

class tf2:

    def calc(topic):
        res=dict({})
        database = DBConnection.getConnection()
        cursor = database.cursor()
        cursor.execute("select * from webapp_dataset")
        row = cursor.fetchall()
        topic=topic.lower()
        topic=topic.split()
        for r in row:
            id = r[0]
            q_n = r[1]
            print(q_n)
            matched=0
            for word in topic:
                matched=matched+CountWords.countOccurences(q_n,word)
            tf=matched/len(q_n.split())
            print(tf)

            if tf>0.5:
                res[id]=tf



        sorted_dict = dict( sorted(res.items(),
                           key=lambda item: item[1],
                           reverse=True))
        print(sorted_dict)
        if(len(sorted_dict)>0):
            val = [elem[0] for elem in sorted_dict.items()]
            return val[0]
        else:
            return -1





            

if __name__ == '__main__':
    print(tf2.calc('Did Wilson support the committee system?'))