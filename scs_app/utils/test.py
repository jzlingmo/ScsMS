# -*- coding: utf-8 -*-
__author__ = 'jz'



from snownlp import SnowNLP


if __name__ == "__main__":
    a = u'this is test for something you dont know,my name is zhouwenjie,you should tell me your name right now'
    b = u'我去，这个能不能分词啊，毕业设计就靠你了'
    c = u'Natalegawa.Ảnh: dvbTỉnh Hải Nam, Trung Quốc gần đây tuyên bố sẽ cho phép cảnh sát biển kiểm tra thậm chí là chiếm giữ tàu lạ ở khu'
    s_a = SnowNLP(c)
    print(s_a.keywords(3))
    print(s_a.summary())
    print('end')
