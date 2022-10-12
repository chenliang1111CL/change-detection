source activate solaris
train_data_path=$1

rm -r /wdata/saved_model/hrnet/best_model/

rm -r /wdata/train
cp -r $train_data_path /wdata/train
rm /wdata/train/*

python tools.py /wdata/train train 2>err.log