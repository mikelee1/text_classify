#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cnn_model import *
from data.cnews_loader import *
import tensorflow.contrib.keras as kr
import sys
import pandas as pd
import time
from datetime import timedelta

try:
    bool(type(unicode))
except NameError:
    unicode = str

base_dir = 'data/cnews'
vocab_dir = os.path.join(base_dir, 'cnews.vocab.txt')

save_dir = 'checkpoints/textcnn'
save_path = os.path.join(save_dir, 'best_validation')  # 最佳验证结果保存路径


class CnnModel:
    def __init__(self):
        self.config = TCNNConfig()
        self.categories, self.cat_to_id = read_category()
        self.words, self.word_to_id = read_vocab(vocab_dir)
        self.config.vocab_size = len(self.words)
        self.model = TextCNN(self.config)

        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        saver.restore(sess=self.session, save_path=save_path)  # 读取保存的模型

    def predict(self, message):
        # 支持不论在python2还是python3下训练的模型都可以在2后者3的环境下运行
        content = unicode(message)
        data = [self.word_to_id[x] for x in content if x in self.word_to_id]

        feed_dict = {
            self.model.input_x: kr.preprocessing.sequence.pad_sequences([data], self.config.seq_length),
            self.model.keep_prob: 1.0
        }

        y_pred_cls = self.session.run(self.model.y_pred_cls, feed_dict=feed_dict)
        y_pred_cls_list = self.session.run(self.model.logits, feed_dict=feed_dict).tolist()[0]
        # return self.categories[y_pred_cls[0]]
        lis = {}
        for i in range(len(y_pred_cls_list)):
            lis[self.categories[i]] = y_pred_cls_list[i]
        res = self.categories[y_pred_cls[0]]
        return res, lis


if __name__ == '__main__':
    arg = sys.argv

    if len(arg) == 4 and arg[1] == 'file':
        mode = 'file'
    elif len(arg) == 2 and arg[1] == 'inter':
        mode = 'inter'
    elif len(arg) == 4 and arg[1] == 'split':
        mode = 'split'
    else:
        raise ValueError('usage: python predict.py [inter] | [file sourfilename desfilename]')

    cnn_model = CnnModel()

    if mode == 'inter':
        while True:
            test_demo = input('input name:')
            res, lis = cnn_model.predict(test_demo)
            print(res)
            print(lis)
    if mode == 'file':
        filename = arg[2]
        desfilename = arg[3]
        with open(filename, 'r') as f:
            with open(desfilename,'w') as des:
                tmp = f.read().strip().split('\n')
                for i in tmp:
                    res, lis = cnn_model.predict(i)
                    #print(i,res)
                    data = str(res)+'    '+str(i)+'\n'
                    des.write(data)
    if mode == 'split':
        filename = arg[2]
        desfilename = arg[3]
        df = pd.read_table(filename,sep=',')

        for index in range(len(df.values)):
            cont=df.values[index]
            res,lis=cnn_model.predict(cont[2])
            df.iloc[index,3]=res
        df.to_csv(desfilename,index=False)
