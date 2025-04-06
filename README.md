
## 简介
    基于ortools的混合整数规划求解器，计算舰船强化的最低资源消耗

## 项目仓库
https://github.com/FredHe3016/AzureLaneShipEnhance

## 开发环境
- **操作系统**: Windows 11
- **Python**: 3.13.2

## 打包成可执行文件
    在项目主目录下执行build.bat即可，注意需要将build.bat中的ORTOOLS_LIB_ROOT修改为您设备的ortools安装路径

## 输入注意事项：
1. 舰船名称和本体双倍强化值相关，请尽量输入正确名称（暂不兼容河蟹、改造、昵称等）
2. 强化素材输入框内，在舰船名称后输入整数(≥0)代表限制数量
3. 强化素材输入框内，舰船名称/限制数量需使用空格或换行隔开，单个舰船名称后最多只能跟随一个数字
4. 计算的目标是最小化各项资源*权重之和（物资的权重固定为1）
5. 因为除了计算方法以外很多东西是现学的，可能会出现一些bug还请见谅

## 待完成事项：
1. 部分舰船强化值补全，以及所有舰船每级强化值和最大升级次数的数据整理
2. 勋章池物资期望计算（作为勋章的默认权重），需要整理勋章池掉落、舰船初始携带装备、以及装备对应拆解物资的数据
3. 强化材料部分增加快速下拉框用于快速输入，目前考虑的选项有：
    - 所有舰船
    - 主线可掉落舰船
    - 主线/活动/档案可掉落舰船
    - 待补充
4. 预定义输入舰船强化值组件(基于舰船名称生成部分强化相关数据)

## 其他计划：
1. 强化材料增加以类似表格形式进行输入的方式
2. 输出舰船名称伴有相应舰船头像
3. 不溢出强化值条件下的最浪费方案（问就是吃饱了撑的）
4. 做成网页形式（现学前后端中...）
5. 允许输入强化界面截图，通过识图来快速完成强化数据的输入（完全不会这个QvQ，如果现学现卖不成的话就只能鸽了）