import unittest
from myclass.BLfunction import bilibili_search
from myclass.BLClass import bilibili
bv=["BV1T8411B7P4","BV1rz4y1L737","BV1t8411B7fg","BV1sm4y1u71F","BV17z4y1M76T",
    "BV1sj411276y","BV1Wu4y1D7ww","BV1bz4y1r7Ug","BV1FE411A7Xd","BV1Xs411X7wh"]
cid = ["1260165760", "1258984819", "1258332435", "1249861606", "1249834679",
       "1251331073", "1249185138", "1165117331", "267307677", "6051409"]

class MyTestCase(unittest.TestCase):
    def test_something_get_cid(self):
        my_bilibili=bilibili()
        testcid=[]
        for i in bv:
            my_bilibili.bvid=i
            my_bilibili.get_cid()
            testcid.append(str(my_bilibili.cid))
        self.assertEqual(cid, testcid)  # add assertion here

    def test_something_get_source(self):
        my_bilibili = bilibili()
        for i in cid:
            my_bilibili.data=[]
            my_bilibili.cid=i
            my_bilibili.get_source()
            if my_bilibili.data:
                judge=True
            else:
                judge=False
            self.assertEqual(True,judge)

class FunTestCase(unittest.TestCase):
    def test_something_search(self):
        my_bilibili = bilibili()
        for i in range(10):
            bvid = []
            bvid=bilibili_search(my_bilibili.headers, i + 1, "日本核污染水排海")
            if bvid:
                judge=True
            else:
                judge=False
            self.assertEqual(True,judge)

if __name__ == '__main__':
    unittest.main()
