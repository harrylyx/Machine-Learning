#### 决策树

---

本函数是利用决策树C4.5算法对数据进行训练并测试

训练集`bank-full.train`与测试集`bank-full.test`均已经给出

使用的环境为Python 2.7.11



**思路：**

数据集特征有16列，既有标称型又有数值型，所以选择使用[C4.5](https://en.wikipedia.org/wiki/C4.5_algorithm)算法，使用树的数据结构为字典类型`myTree = {bestFeatLabel:{}}`便于递归生成树，对于数值型处理方法为3000为步长选择最佳阈值进行，在将最佳阈值`labelType[name]`以`myTree[bestFeatLabel]['high'+str(labelType[name])]`or`myTree[bestFeatLabel]['low'+str(labelType[name])]`保存下来，以便后期测试处理，具体详细请参考程序，如有不足请指出。