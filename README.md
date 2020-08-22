# extractFeaturesFromICMPPcap
混淆矩阵：
![image](https://github.com/parahaoer/extractFeaturesFromICMPPcap/blob/master/images/%E6%B7%B7%E6%B7%86%E7%9F%A9%E9%98%B5%E7%AC%94%E8%AE%B0.jpg)


K折交叉验证：
 使用cross_val_predict()函数进行K折交叉验证，它会返回在每一个测试折（fold）上的预测值，这意味着可以得到训练集中的每个样本的预测值。
![image](https://github.com/parahaoer/extractFeaturesFromICMPPcap/blob/master/images/confusion_matrix.bmp)
如上图所示，label代表真实值，pred代表预测值，从label和pred的比较中，可以得到TP=7, TN=7, FP=2, FN=1 来构造混淆矩阵。
