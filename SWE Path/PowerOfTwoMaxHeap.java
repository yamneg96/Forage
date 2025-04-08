import java.util.ArrayList;
import java.util.List;

public class PowerOfTwoMaxHeap<T extends Comparable<T>> {
    private final List<T> heap;
    private final int childrenPerNode;

    public PowerOfTwoMaxHeap(int branchingFactorExponent) {
        if (branchingFactorExponent < 0 || branchingFactorExponent > 20) {
            throw new IllegalArgumentException("Branching factor exponent must be between 0 and 20");
        }
        this.childrenPerNode = 1 << branchingFactorExponent; // 2^exponent
        this.heap = new ArrayList<>();
    }

    public void insert(T value) {
        heap.add(value);
        siftUp(heap.size() - 1);
    }

    public T popMax() {
        if (heap.isEmpty()) {
            throw new IllegalStateException("Heap is empty");
        }

        T maxValue = heap.get(0);
        T lastValue = heap.remove(heap.size() - 1);

        if (!heap.isEmpty()) {
            heap.set(0, lastValue);
            siftDown(0);
        }

        return maxValue;
    }

    public T peekMax() {
        if (heap.isEmpty()) throw new IllegalStateException("Heap is empty");
        return heap.get(0);
    }

    public int size() {
        return heap.size();
    }

    public boolean isEmpty() {
        return heap.isEmpty();
    }

    private void siftUp(int index) {
        while (index > 0) {
            int parentIndex = (index - 1) / childrenPerNode;
            if (heap.get(index).compareTo(heap.get(parentIndex)) > 0) {
                swap(index, parentIndex);
                index = parentIndex;
            } else break;
        }
    }

    private void siftDown(int index) {
        int size = heap.size();
        while (true) {
            int maxIndex = index;

            int firstChildIndex = childrenPerNode * index + 1;
            int lastChildIndex = Math.min(firstChildIndex + childrenPerNode, size);

            for (int i = firstChildIndex; i < lastChildIndex; i++) {
                if (heap.get(i).compareTo(heap.get(maxIndex)) > 0) {
                    maxIndex = i;
                }
            }

            if (maxIndex != index) {
                swap(index, maxIndex);
                index = maxIndex;
            } else break;
        }
    }

    private void swap(int i, int j) {
        T tmp = heap.get(i);
        heap.set(i, heap.get(j));
        heap.set(j, tmp);
    }

    public void printHeap() {
        System.out.println(heap);
    }
// Example usage
public static void main(String[] args) {
  // Use 2^3 = 8 children per node
  PowerOfTwoMaxHeap<Integer> shippingQueue = new PowerOfTwoMaxHeap<>(3);

  int[] priorities = {45, 22, 70, 10, 90, 50, 60, 33, 85, 15};

  for (int priority : priorities) {
      shippingQueue.insert(priority);
  }

  System.out.println("Heap after insertions:");
  shippingQueue.printHeap();

  System.out.println("\nMax values (in order):");
  while (!shippingQueue.isEmpty()) {
      System.out.print(shippingQueue.popMax() + " ");
  }
}
}
