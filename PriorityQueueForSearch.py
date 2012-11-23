from ReversibleArray import ReversibleArray

class PriorityQueueForSearch:
  """An efficient priority queue which contains the minimal set of operations needed to support a prioritied search,
     such as a Uniform Cost Search or an A* Search."""

  def __init__( self, aHasLowerPriorityThan ):
    """Construct an empty PriorityQueueForSearch.  A delegate that determines priority must be provided on construction.
       aHasHigherPriorityThan: a delegate that, for any two nodes, returns true if the first node
       has lower priority than the second node, and false otherwise"""
 
    # The root of the heap is at index 1.  The last leaf in the heap is in the last populated index in
    # mHeap.  the last populated index in mHeap is maintained in mIndexOfLastLeaf.
    self.mIndexOfLastLeaf = 0
    
    # states in the queue are stored in a heap, which allows for O(log n) removal, 
    # O(log n) enqueueing and O(log n) replacement.
    self.mHeap = ReversibleArray( 2 << 16 )
    
    # nodes corresponding to states in the queue are stored in a hash, which allows for O(1) insertion, 
    # O(1) retrieval and O(1) removal.
    self.mHash = dict()
    
    # a delegate that returns true if the first argued node has lower priority than the second, and false otherwise.
    self.mHasLowerPriorityThan = aHasLowerPriorityThan
    
    self.NumberEnqueued = 0

  def EnqueueIfBetter( self, aItem ):
    """Add a node to the priority queue if and only if there is no node in the queue that has the same state
       but the same or higher priority."""
    if not aItem.state in self.mHash:
      self.mHash[aItem.state] = aItem
      self.AddToHeap( aItem.state )
    elif self.mHasLowerPriorityThan( self.mHash[ aItem.state ],  aItem ):
      self.mHash[ aItem.state ] = aItem
      self.PlaceAt( aItem.state, self.mHeap.IndexOf( aItem.state ) )

    self.NumberEnqueued += 1

  def Dequeue(self):
    """Remove the highest prority node in the queue from the queue and return it."""
  
    if self.IsEmpty():
      raise Exception("The Heap is empty.")

    lReturnValue = self.mHash[ self.mHeap[ 1 ] ]

    self.RemoveFromHeap( 1 )

    del self.mHash[lReturnValue.state]

    return lReturnValue

  def IsEmpty(self):
    """Return true if there are no nodes in the queue, false otherwise."""
    return self.mIndexOfLastLeaf <= 0

  def RemoveFromHeap( self, aHeapIndex ):
    """Remove a state at a random index from the heap and adjust the heap.  Current this method only works for index 1;
       additional adjustment may be needed for other indices, i.e. the item last assigned to mHeap[j/2] must be
       floated up to its proper location."""
    lLastLeafBeforeRemoval = self.mHash[ self.mHeap[ self.mIndexOfLastLeaf ] ]
    self.mHeap[ aHeapIndex ] = self.mHeap[ self.mIndexOfLastLeaf ]
    self.mHeap[ self.mIndexOfLastLeaf ] = None
    self.mIndexOfLastLeaf -= 1

    if aHeapIndex == self.mIndexOfLastLeaf + 1:
      return

    j = 2 * aHeapIndex
    while j <= self.mIndexOfLastLeaf:
      if j < self.mIndexOfLastLeaf and self.mHasLowerPriorityThan(  self.mHash[ self.mHeap[ j ] ], self.mHash[ self.mHeap[ j + 1 ] ] ):
        j += 1

      if not self.mHasLowerPriorityThan( lLastLeafBeforeRemoval, self.mHash[ self.mHeap[ j ] ] ):
        break

      self.mHeap[ j / 2 ] = self.mHeap[ j ]
      
      j *= 2

    self.mHeap[ j / 2 ] = lLastLeafBeforeRemoval.state

  def AddToHeap( self, aItem ):
    """Add an item to the heap.  If the heap is full to capacity before the addition, double its size before adding the item."""
  
    self.mIndexOfLastLeaf += 1

    if self.mIndexOfLastLeaf >= len(self.mHeap) - 1:
      self.DoubleUp()

    self.PlaceAt( aItem, self.mIndexOfLastLeaf )

  def PlaceAt( self, aItem, aIndex ):
    """Place an item at a specified index on the heap, then float it up to its proper place.
       aItem: an item
       aIndex: the index at which the item should start at before it is floated upward"""
    i = aIndex
    while i > 1 and self.mHasLowerPriorityThan( self.mHash[ self.mHeap[ i / 2 ] ], self.mHash[ aItem ] ):
      self.mHeap[ i ] = self.mHeap[ i / 2 ]
      i /= 2

    self.mHeap[ i ] = aItem

  def DoubleUp(self):
    """Since mHeap is fixed-length array, it must be replaced with a longer array when the queue fills beyond its capacity.
      DoubleUp() creates an array that is twice the length of mHeap, copies the contents of mHeap to the new array, then
      assigns the new array to mHeap."""
    lNewCollection = ReversibleArray( 2 * len(self.mHeap) )

    for i in xrange(len(self.mHeap)):
      lNewCollection[ i ] = self.mHeap[ i ]

    self.mHeap = lNewCollection

if __name__ == '__main__':
  queue = PriorityQueueForSearch(lambda x,y: x.state > y.state)
  queue.EnqueueIfBetter(Node(1))
  queue.EnqueueIfBetter(Node(2))
  queue.EnqueueIfBetter(Node(6))
  queue.EnqueueIfBetter(Node(3))
  queue.EnqueueIfBetter(Node(1))
  queue.EnqueueIfBetter(Node(4))
  
  while not queue.IsEmpty():
    print queue.Dequeue().state