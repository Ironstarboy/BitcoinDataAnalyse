import networkx as nx

def get():
    # 从一个List添加节点(1,2,{'weight':100})
    G.add_nodes_from([2, 3])
    pass

G = nx.DiGraph() #初始化一个有向图
G.add_edge('A', 'B') #添加边
G.add_edge('A', 'D')
G.add_edge('B', 'C')
G.add_edge('B', 'D')
G.add_edge('D', 'E')
G.add_edge('E', 'D')
# 网络的基本性质
num_nodes = nx.number_of_nodes(G)  # 节点数
num_edges = nx.number_of_edges(G)  # 连接数
density = nx.density(G)  # 密度
clusterint_coefficient = nx.average_clustering(G)  # 平均聚集系数/局部聚集系数
transitivity = nx.transitivity(G)  # 传递性/全局聚集系数
reciprocity = nx.reciprocity(G)  # 互惠性

print('节点个数: ', num_nodes)
print('连接数: ', num_edges)
print('密度: ', density)
print('局部聚集系数: ', clusterint_coefficient)
print('全局聚集系数: ', transitivity)
print('互惠性: ', reciprocity)
# 中心度计算
out_degree = nx.out_degree_centrality(G)  # 出度中心度
in_degree = nx.in_degree_centrality(G)  # 入度中心度
out_closeness = nx.closeness_centrality(G.reverse())  # 出接近中心度
in_closeness = nx.closeness_centrality(G)  # 入接近中心度
betweenness = nx.betweenness_centrality(G)  # 中介中心度

print('出度中心度: ', out_degree)
print('入度中心度: ', in_degree)
print('出接近中心度: ', out_closeness)
print('入接近中心度: ', in_closeness)
print('中介中心度: ', betweenness)
# 中心势计算
# 在networkx中没有似乎没有直接计算中心势的方法，这里我们可以根据公式自己计算。
max_ = 0
s = 0
for out in out_degree.keys():
    if (out_degree[out] > max_): max_ = out_degree[out]
    s = s + out_degree[out]
print('出度中心势：', (num_nodes * max_ - s) / (num_nodes - 2))

max_ = 0
s = 0
for in_ in in_degree.keys():
    if (in_degree[in_] > max_): max_ = in_degree[in_]
    s = s + in_degree[in_]
print('入度中心势：', (num_nodes * max_ - s) / (num_nodes - 2))

max_ = 0
s = 0
for b in out_closeness.keys():
    if (out_closeness[b] > max_): max_ = out_closeness[b]
    s = s + out_closeness[b]
print('出接近中心势：', (num_nodes * max_ - s) / (num_nodes - 1) / (num_nodes - 2) * (2 * num_nodes - 3))

max_ = 0
s = 0
for b in in_closeness.keys():
    if (in_closeness[b] > max_): max_ = in_closeness[b]
    s = s + in_closeness[b]
print('入接近中心势：', (num_nodes * max_ - s) / (num_nodes - 1) / (num_nodes - 2) * (2 * num_nodes - 3))

max_ = 0
s = 0
for b in betweenness.keys():
    if (betweenness[b] > max_): max_ = betweenness[b]
    s = s + betweenness[b]
print('中介中心势：', (num_nodes * max_ - s) / (num_nodes - 1))
# 绘制
import matplotlib.pyplot as plt
nx.draw(G,with_labels=True)
plt.show()