class ReversibleArray:
  """An array that finds a member by its index in O(1) time and finds the index of a member in O(1) time, too.
     Indices are zero-based.  if the Reversible array is to work efficiently, the objects in it must have good
     definitions for __hash__ and __eq__."""
  def __init__( self, aCapacity ):
    """Construct an empty ReversibleArray."""
    self.mArray = [None]*aCapacity
    self.mHash = dict()

  def __getitem__(self,aIndex):
    """Get/set an item at a specified index.  Indices are zero-based."""
    return self.mArray[ aIndex ]

  def __setitem__(self,aIndex,aValue):
    if not aValue is None:
      self.mHash[ aValue ] = aIndex
    elif self.mArray[ aIndex ] in self.mHash:
      del self.mHash[ self.mArray[ aIndex ] ]

    self.mArray[ aIndex ] = aValue

  def IndexOf(self,aItem):
    """Get the index of a specified item in the array.  Return -1 if the item is not in the array.  If more than one
       item in the array equals the specified item, then return the last index to which an item equal to the specified
       item was assigned."""
    if not aItem in self.mHash:
      return -1;

    return self.mHash[ aItem ]

  def __len__(self):
    """the array's length"""
    return len(self.mArray)