#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

from collections import Counter

import numpy as np
import tensorflow.contrib.keras as kr

if sys.version_info[0] > 2:
    is_py3 = True
else:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    is_py3 = False


def native_word(word, encoding='utf-8'):
    """如果在oython2下面使用python3训练的模型，可考虑调用此函数转化一下字符编码"""
    if not is_py3:
        return word.encode(encoding)
    else:
        return word


def native_content(content):
    if not is_py3:
        return unicode(content)
    else:
        return content


def open_file(filename, mode='r'):
    """
    Commonly used file reader, change this to switch between python2 and python3.
    mode: 'r' or 'w' for read or write
    """
    if is_py3:
        return open(filename, mode, encoding='utf-8', errors='ignore')
    else:
        return open(filename, mode)


def read_file(filename):
    """读取文件数据"""

    contents, intros, labels = [], [], []
    with open_file(filename) as f:
        for line in f:
            try:
                label, content, intro = line.strip().split('\t')
                if content:
                    contents.append(list(native_content(content)))
                    labels.append(native_content(label))
                    intros.append(list(native_content(intro)))
            except:
                pass
    return contents, labels, intros


def build_vocab(train_dir, vocab_dir, vocab_size=5000):
    """根据训练集构建词汇表，存储"""
    data_train, _ ,intros= read_file(train_dir)

    all_data = []
    intros = intros[0]#todo
    data_train = data_train+intros
    print(intros)
    for content in data_train:
        all_data.extend(content)
    counter = Counter(all_data)
    count_pairs = counter.most_common(vocab_size - 1)
    words, _ = list(zip(*count_pairs))
    # 添加一个 <PAD> 来将所有文本pad为同一长度
    words = ['<PAD>'] + list(words)
    open_file(vocab_dir, mode='w').write('\n'.join(words) + '\n')


def read_vocab(vocab_dir):
    """读取词汇表"""
    # words = open_file(vocab_dir).read().strip().split('\n')
    with open_file(vocab_dir) as fp:
        # 如果是py2 则每个值都转化为unicode
        words = [native_content(_.strip()) for _ in fp.readlines()]
    word_to_id = dict(zip(words, range(len(words))))
    return words, word_to_id


def read_category():
    """读取分类目录，固定"""
    #categories = [u'体育', u'财经', u'房产', u'家居',u'教育', u'科技', u'时尚', u'时政', u'游戏', u'娱乐']
    categories = [u'悬疑', u'言情', u'幻想', u'文学', u'武侠', u'都市', u'社科', u'历史', u'官场商战', u'经管', u'人文',u'生活',u'童书',u'经典',u'教材']
    cat_to_id = dict(zip(categories, range(len(categories))))

    return categories, cat_to_id


def to_words(content, words):
    """将id表示的内容转换为文字"""
    return ''.join(words[x] for x in content)


def process_file(filename, word_to_id, cat_to_id, max_length=600):
    """将文件转换为id表示"""
    contents, labels, intros = read_file(filename)

    data_id, label_id, intro_id = [], [], []
    for i in range(len(contents)):
        data_id.append(
            [word_to_id[x] for x in contents[i] if x in word_to_id])
        label_id.append(cat_to_id[labels[i]])
        intro_id.append(
            [word_to_id[x] for x in intros[i] if x in word_to_id])

    # 使用keras提供的pad_sequences来将文本pad为固定长度
    x_pad = kr.preprocessing.sequence.pad_sequences(data_id, max_length)
    y_pad = kr.utils.to_categorical(label_id)  # 将标签转换为one-hot表示，且按照label_id最大值来设置
    intro_pad = kr.preprocessing.sequence.pad_sequences(intro_id, max_length)

    return x_pad, y_pad, intro_pad


def batch_iter(x, y, batch_size=64):
    """生成批次数据"""
    data_len = len(x)
    num_batch = int((data_len - 1) / batch_size) + 1

    indices = np.random.permutation(np.arange(data_len))
    x_shuffle = x[indices]
    y_shuffle = y[indices]

    for i in range(num_batch):
        start_id = i * batch_size
        end_id = min((i + 1) * batch_size, data_len)
        yield x_shuffle[start_id:end_id], y_shuffle[start_id:end_id]
