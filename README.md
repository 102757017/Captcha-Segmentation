# Captcha-Segmentation
使用opencv对验证码进行分割  
以下是某网站的交易确认的验证码：  
![验证码图片](https://github.com/102757017/Captcha-Segmentation/blob/master/get-captcha.png)  
验证码是彩色的，有随机干扰线，干扰线比较粗，并且字符与干扰线边缘都进行了羽化并且都带有阴影；字符颜色随机，有随机倾斜、随机的位置、稍微变换了大小、稍微有些扭曲，部分字符有粘连。  
由于字符位置有随机变换，直接将图片四等分是不形的  
尝试使用寻找连通区域分割字符，干扰线将字符贯通了，因此首先需要去除干扰线，尝试使用腐蚀操作去除干扰线，发现干扰线的阴影会影响效果  
因此先去除图片阴影，可以使用K-means聚类对图片进行相似颜色的合并，但是K-means算法速度比较慢，需要2~3秒时间，关键时刻等个几秒钟，东西都抢没了，需要效率更高的算法，这里使用photoshop内色调分离的算法减少颜色，处理后结果如下：  
![减色图片](https://github.com/102757017/Captcha-Segmentation/blob/master/re_color.png)  
然后转换到HSV色彩空间提取灰色~黑色的区域，获得了干扰线如下：  
![干扰线图片](https://github.com/102757017/Captcha-Segmentation/blob/master/mask.jpg)  
将干扰线区域作为蒙版对图片进行修复，去除干扰线后结果如下：  
![修复图片](https://github.com/102757017/Captcha-Segmentation/blob/master/repair.png)  
修复后的图片字符有粘连，使用连通区域检测只能分离出2个字符，字符颜色又不确定，不能按颜色分类，因此采用分水岭算法对字符进行分割，计算过程如下：  
![分割图片](https://github.com/102757017/Captcha-Segmentation/blob/master/Division.PNG)  
此时四个字符已近完全分离开了，分别提取最小外接矩形，将倾斜字符校平，结果分别进行保存。  
![图片](https://github.com/102757017/Captcha-Segmentation/blob/master/result.PNG)  
下一步可以使用对分割的字符图片进行降维，然后k-means聚类（确认该验证码用到了多少个字符就聚为几类，K-means算法请参考https://github.com/102757017/basic/blob/master/%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/%E8%81%9A%E7%B1%BB/k-means.py），分别保存到不同的文件夹，聚类可能会有少部分字符分类错误，进行手工修改，完工后就可以作为CNN的训练集了，如此就实现了半监督学习，不用手工去打码了。