class Graph:

  class Vertex:

    __slots__ = '_element'

    def __init__(self, x):
      self._element = x
  
    def element(self):
      return self._element

    def __str__(self):
      return str(self._element)
    

  class Edge:

    __slots__ = '_origin', '_destination', '_element'
  
    def __init__(self, origin, destination, element):
      self._origin = origin
      self._destination = destination
      self._element = element

    def opposite(self, v):
      if not isinstance(v, Graph.Vertex):
        raise TypeError('v mora biti instanca klase Vertex')
      if self._destination == v:
        return self._origin
      elif self._origin == v:
        return self._destination
      raise ValueError('v nije čvor ivice')
  
    def element(self):

      return self._element

    def __str__(self):
      return '({0},{1},{2})'.format(self._origin,self._destination,self._element)

  def __init__(self, directed=False):

    self._outgoing = {}
    self._incoming = {} if directed else self._outgoing

  def _validate_vertex(self, v):
    if not isinstance(v, self.Vertex):
      raise TypeError('Ocekivan je objekat klase Vertex')
    if v not in self._outgoing:
      raise ValueError('Vertex ne pripada ovom grafu.')

  def is_directed(self):
    return self._incoming is not self._outgoing

  def vertex_count(self):
    return len(self._outgoing)

  def vertices(self):
    return self._outgoing.keys()

  def edge_count(self):
    total = sum(len(self._outgoing[v]) for v in self._outgoing)
    return total if self.is_directed() else total // 2

  def get_edge(self, u, v):
    self._validate_vertex(u)
    self._validate_vertex(v)
    return self._outgoing[u].get(v)

  def degree(self, v, outgoing=True):
    self._validate_vertex(v)
    adj = self._outgoing if outgoing else self._incoming
    return len(adj[v])

  def incident_edges(self, v, outgoing=True):
    self._validate_vertex(v)
    adj = self._outgoing if outgoing else self._incoming
    for edge in adj[v].values():
      yield edge

  def insert_vertex(self, x=None):
    v = self.Vertex(x)
    self._outgoing[v] = {}
    if self.is_directed():
      self._incoming[v] = {}
    return v
      
  def insert_edge(self, u, v, x=None):
    if self.get_edge(u, v) is not None:
      raise ValueError('u and v are already adjacent')
    e = self.Edge(u, v, x)
    self._outgoing[u][v] = e
    self._incoming[v][u] = e
