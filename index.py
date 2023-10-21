import sys
from collections import defaultdict


class Graph(object):
    """
      Graph has a structure like this one
      id : [[id1, idN], time]
      where
      id of node in graph: [[list of ids that represent connections], timestamp in DB]
    """
    def __init__(self):
      self._graph = {}
      self._graph[1] = [[None], None]
      self.res = 0

    def add_connection(self, origin, dest, time):
      """ Add a connection to the graph """
      if origin not in self._graph:
        self._graph[origin] = [[], time]
      self._graph[origin][0].append(dest)

    def is_connected(self, node1, node2):
      """ 
        Check if node1 is connected to node2 or
        node2 is connected to node1
      """
      if self._graph[node1][0]:
        return node2 in self._graph[node1][0] or node1 in self._graph[node2][0]
      return node1 in self._graph[node2][0]

    def find_shortest_path(self, origin, dest, path=[]):
      """ Find the shortest path in the graph """
      path = path + [origin]
      if origin == dest:
        return path
      if origin not in self._graph:
        return None
      
      shortest = None
      for node in self._graph[origin][0]:
        if node not in path:
          new_path = self.find_shortest_path(node, dest, path)
          if not shortest or len(new_path) < len(shortest):
            shortest = new_path

      return shortest
    
    def find_indirect_neighbours(self, start_node, prev_node, path, visited):

      if len(path) == 3 and start_node not in visited and start_node:
        visited.append(start_node)
        self.res += 1
        return 
      if not start_node or len(path) > 3 or start_node in visited or prev_node == start_node:
        return 
      
      prev_node = start_node      
      for node in self._graph[start_node][0]:
        path.append(node)
        self.find_indirect_neighbours(node, prev_node, path, visited)
        path.pop()
        prev_node = node
      return self.res
    
class Solution(object):

  def __init__(self):
    # Creation of DAG
    with open(sys.argv[1], 'r') as f:
      rows = f.read()

    self.num_nodes = int(rows[0])
    rows_processed = rows[1:].strip().split('\n')

    self.graph = Graph()
    for id, row in enumerate(rows_processed):
      self.graph.add_connection(id + 2, int(row[0]), int(row[4]))
      self.graph.add_connection(id + 2, int(row[2]), int(row[4]))

  def get_avg(self):
    """ Get average depth of DAG """
    avg = 0
    for id in range(1, self.num_nodes + 1):
      path = self.graph.find_shortest_path(id + 1, 1) # you cannot consider path from 1 to 1
      depth = len(path) - 1
      avg += depth
    return round(avg / (self.num_nodes + 1), 2)

  def get_avg_nodes_depth(self):
    """ Get average number of Txs per depth """ 
    nodes_depths = {}
    for id in range(1, self.num_nodes + 1):
      path = self.graph.find_shortest_path(id + 1, 1) # you cannot consider path from 1 to 1
      depth = len(path) - 1
      nodes_depths[depth] = nodes_depths.get(depth, 0) + 1
    return round(sum(nodes_depths.values()) / len(nodes_depths.keys()), 2)

  def get_avg_indegree(self):
    """ Get average number of indegree connections per node """
    indegree = {}
    neighbours = [neighbour[0] for neighbour in list(self.graph._graph.values()) if neighbour[0] is not None]
    for vertexes in neighbours:
      for vertex in vertexes:
        if vertex and vertex in vertexes:
          indegree[vertex] = indegree.get(vertex, 0) + 1
    return round(sum(indegree.values()) / (self.num_nodes + 1), 3)

  def get_avg_time(self):
    """ Get average time of Txs """
    times = [time[1] for time in list(self.graph._graph.values()) if time[1] is not None]
    return round(sum(times) / len(times), 2)
  
  def get_avg_neighbours(self):
    """ Get average number of neighbours a node can have """
    neighbours = [0] * (self.num_nodes + 1)
    for id, value in self.graph._graph.items():
      if value[0][0]:
        for connect in value[0]:
          neighbours[id - 1] += 1
          neighbours[connect - 1] += 1
    return round(sum(neighbours) / len(neighbours), 2)
  
  def get_avg_indirect_neighbours(self):
    num_ind_neigh = 0
    for node in self.graph._graph.keys():
      num_ind_neigh = self.graph.find_indirect_neighbours(node, -1, [node], [])
    return num_ind_neigh / len(self.graph._graph.keys())


if __name__ == "__main__":
  print("-----------------------------------------------")
  print("------------- IOTA TECH EXERCISE --------------")
  print("-----------------------------------------------")
  solution = Solution()
  print("> AVG DAG DEPTH: ", solution.get_avg())
  print("> AVG TXS PER DEPTH: ", solution.get_avg_nodes_depth())
  print("> AVG REF: ", solution.get_avg_indegree())
  print("> AVG TX TIME: ", solution.get_avg_time()) 
  print("> AVG NUM OF NEIGHBOURS PER NODE (with ROOT): ", solution.get_avg_neighbours())
  print("> AVG NUM OF INDIRECT NEIGHBOURS PER NODE (with ROOT): ", solution.get_avg_indirect_neighbours())
  print("\t Definition: An indirect neighbour is the neighbour of a direct neighbour of a node")
  print("-----------------------------------------------")
  print("--------------- END OF EXERCISE ---------------")
  print("-----------------------------------------------")
