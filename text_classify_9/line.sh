python3 filter.py
cp result.txt data/cnews/cnews.val.txt
cp result.txt data/cnews/cnews.train.txt
cp result.txt data/cnews/cnews.test.txt
rm data/cnews/cnews.vocal.txt
python3 run_cnn.py train
