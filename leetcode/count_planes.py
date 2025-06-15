def count_planes(starHeight, descentRate):
    #貪心算法：按照高度升序排序，優先擊落高低較低的飛機，類似俄羅斯方塊/擊落飛機遊戲
    planes = sorted(zip(starHeight,descentRate), key= lambda x:x[0])
    count = 0

    for height, rate in planes:
        if
