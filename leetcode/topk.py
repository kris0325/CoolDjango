import heapq

"""
topKSmaller

在這個情境中,我們要找的是最大的10個數字(top 10 largest numbers)。您提到的解決方法是正確的,使用最小堆(MinHeap)確實是一個高效的解決方案[6]。讓我們詳細解釋一下您提到的幾種方法:

## 解決方案比較

**1. 最大堆(MaxHeap)方法**
- 將所有元素放入最大堆中
- 優點: 直觀
- 缺點: 空間複雜度高,需要存儲所有元素

**2. 最小堆(MinHeap)方法** (推薦)
- 維護一個大小為10的最小堆
- 優點: 空間複雜度低,只需要存儲10個元素
- 時間複雜度: O(N log 10),其中N是元素總數

**3. 快速選擇(QuickSelect)方法**
- 基於快速排序的思想
- 優點: 平均時間複雜度O(N)
- 缺點: 最壞情況下時間複雜度O(N^2),且有遞歸調用棧

## 最小堆實現步驟

1. 創建一個大小為10的最小堆
2. 將前10個元素放入堆中
3. 對於剩餘的每個元素:
   - 如果大於堆頂元素,則移除堆頂元素並插入新元素
   - 否則,跳過該元素
4. 最後,堆中的10個元素就是最大的10個數[3][6]

## 程式碼示例 (Java)

```java
import java.util.PriorityQueue;

public class TopK {
    public static PriorityQueue<Long> findTopK(long[] numbers, int k) {
        PriorityQueue<Long> minHeap = new PriorityQueue<>(k);
        
        for (long num : numbers) {
            if (minHeap.size() < k) {
                minHeap.offer(num);
            } else if (num > minHeap.peek()) {
                minHeap.poll();
                minHeap.offer(num);
            }
        }
        
        return minHeap;
    }
}
```
這個方法的時間複雜度是O(N log k),其中N是元素總數,k是我們要找的最大元素的數量(在這個情況下是10)。空間複雜度是O(k),因為我們只需要存儲k個元素[4]。

使用最小堆的方法不僅高效,而且在處理大規模數據時特別有用,因為它可以在不將所有數據加載到內存中的情況下工作[1][2]。

"""


def topKLarge(nums, k):
    min_heap = []
    for num in nums:
        if len(min_heap) < k:
            heapq.heappush(min_heap, num)
        elif num > min_heap[0]:
            heapq.heappop(min_heap)
            heapq.heappush(min_heap, num)

    return min_heap


"""
如果要求最小的top K個數字,我們可以使用最大堆(MaxHeap)來實現。這是一個與求最大top K個數字相反的思路。以下是具體的實現方法:

## 最大堆實現步驟

1. 創建一個大小為K的最大堆
2. 將前K個元素放入堆中
3. 對於剩餘的每個元素:
   - 如果小於堆頂元素,則移除堆頂元素並插入新元素
   - 否則,跳過該元素
4. 最後,堆中的K個元素就是最小的K個數

## 程式碼示例 (Java)

```java
import java.util.PriorityQueue;
import java.util.Collections;

public class TopKSmallest {
    public static PriorityQueue<Integer> findTopKSmallest(int[] numbers, int k) {
        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
        
        for (int num : numbers) {
            if (maxHeap.size() < k) {
                maxHeap.offer(num);
            } else if (num < maxHeap.peek()) {
                maxHeap.poll();
                maxHeap.offer(num);
            }
        }
        
        return maxHeap;
    }
}
```

這個方法的時間複雜度是O(N log k),其中N是元素總數,k是我們要找的最小元素的數量。空間複雜度是O(k),因為我們只需要存儲k個元素[1][2].

使用最大堆來找最小的top K個數字的原理是:我們始終保持堆中有K個最小的元素,而堆頂元素是這K個中最大的。當我們遇到比堆頂更小的元素時,我們就用它替換堆頂元素,這樣就能保證堆中始終保持K個最小的元素[3][4].

這種方法不僅高效,而且在處理大規模數據時特別有用,因為它可以在不將所有數據加載到內存中的情況下工作。

"""


def topKSmaller(nums, k):
    max_heap = []
    for num in nums:
        if len(max_heap) < k:
            # 我們使用負數來模擬最大堆,因為Python的heapq模塊默認實現最小堆.
            heapq.heappush(max_heap, -num)
        elif -num > max_heap[0]:
            heapq.heappop(max_heap)
            heapq.heappush(max_heap, -num)
    return [-x for x in max_heap]
