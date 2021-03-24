import random

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from networkx.algorithms.community import k_clique_communities
from networkx.drawing.nx_agraph import graphviz_layout
# 包的用法可以参考官方文档以及官方代码tutorial.py


# G=nx.DiGraph()
# G.add_edge(1, 2, weight=4.7 )
# G.add_edges_from([(3, 4), (4, 5)], color='red')
# G.add_edges_from([(1, 2, {'color': 'blue'}), (2, 3, {'weight': 8})])
#
# G[1][2]['weight'] = 4.7
# G.edges[3, 4]['weight'] = 4.2
# nx.draw(G,with_labels=True)
# plt.show()


class deal_net:
    '''构建比特币交易网络，有向图，不考虑多重边，一个时段内2地址多个交易只会单纯增加weight。'''
    _filepath=''
    _G=nx.DiGraph()
    _MG = nx.MultiGraph()# 多重图，解决好动态网络问题，就可以不考虑多重图
    def __init__(self,filepath:str)->'None':
        self._filepath = filepath
        self._creat_net()

    def _creat_net(self):
        # 读取文件,[(source,target,attribute)]
        df = pd.read_csv(self._filepath, encoding='utf-8', engine='python')  # 由于中文问题，engine需换成python
        data = df[['source', 'target', 'weight']]
        merge_result_tuples = [tuple(xi) for xi in data.values]  # 将dataframe的行转为networkx元组参数格式

        count = 0

        for i in merge_result_tuples:
            self._G.add_edge(str(i[0]), str(i[1]), weight=i[2])  #特殊属性 `weight` 应该是数字，因为它被需要加权边缘的算法使用。
            count += 1
            if count>1500:
                break
        # self._G.add_weighted_edges_from()

    def get_net_features(self):
        num_nodes = nx.number_of_nodes(self._G)  # 节点数
        num_edges = nx.number_of_edges(self._G)  # 连接数
        density = nx.density(self._G)  # 密度
        clusterint_coefficient = nx.average_clustering(self._G)  # 平均聚集系数/局部聚集系数
        transitivity = nx.transitivity(self._G)  # 传递性/全局聚集系数
        reciprocity = nx.reciprocity(self._G)  # 互惠性

        print('节点个数: ', num_nodes)
        print('连接数: ', num_edges)
        print('密度: ', density)
        print('局部聚集系数: ', clusterint_coefficient)
        print('全局聚集系数: ', transitivity)
        print('互惠性: ', reciprocity)
        # 中心度计算
        out_degree = nx.out_degree_centrality(self._G)  # 出度中心度
        in_degree = nx.in_degree_centrality(self._G)  # 入度中心度
        out_closeness = nx.closeness_centrality(self._G.reverse())  # 出接近中心度
        in_closeness = nx.closeness_centrality(self._G)  # 入接近中心度
        betweenness = nx.betweenness_centrality(self._G)  # 中介中心度

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
            if out_degree[out] > max_: max_ = out_degree[out]
            s = s + out_degree[out]
        print('出度中心势：', (num_nodes * max_ - s) / (num_nodes - 2))

        max_ = 0
        s = 0
        for in_ in in_degree.keys():
            if in_degree[in_] > max_: max_ = in_degree[in_]
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


    def clique(self,k):
        '''寻找网络中的社团，最好能着色,有向图Label Propagation，无向图clique'''

        # 有向图转为无向图
        G=self._G.to_undirected()
        c_G=list(k_clique_communities(G,k))

        # community可视化
        pos = nx.spring_layout(G)  # 这种布局较慢，呈放射状
        # pos=nx.random_layout(G)  # 随机布局，基本是正方形
        # pos=nx.shell_layout(G)  # 同心圆
        nx.draw_networkx_nodes(G, pos,node_size=10)
        count = 0
        color = ['m', 'g', 'c', 'b', 'y', 'k', 'w']*3
        for i in range(100):
            hex_color='#{:06x}'.format(random.randint(0, 256**3))
            color.append(hex_color)
        # TODO 颜色不够用了
        for com in c_G:
            count = count + 1
            list_nodes = list(com)
            nx.draw_networkx_nodes(G, pos, list_nodes, node_size=50,node_color=color[count - 1])
            print("Community", count, "is:", list_nodes)
        nx.draw_networkx_edges(G, pos,style='dotted',edge_color='green')
        # nx.draw_networkx_labels(G, pos)
        plt.axis("off")
        plt.show()
        print("-"*20)


    def GN(self):
        pass

    def louvain(self):
        pass


    def edge_predict(self):
        '''链路预测，边预测'''
        pass

    def draw(self):
        nx.draw(self._G, with_labels=False,font_weight='bold',)
        elarge = [(u, v) for (u, v, d) in self._G.edges(data=True) if d["weight"] > 0.5]
        esmall = [(u, v) for (u, v, d) in self._G.edges(data=True) if d["weight"] <= 0.5]

        pos = nx.spring_layout(self._G, seed=7)  # positions for all nodes - seed for reproducibility

        # nodes
        nx.draw_networkx_nodes(self._G, pos, node_size=30)

        # edges
        nx.draw_networkx_edges(self._G, pos, edgelist=elarge, node_size=20)
        nx.draw_networkx_edges(
            self._G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color="b", style="dashed",node_size=20
        )

        # labels
        # nx.draw_networkx_labels(self._G, pos, font_size=10,font_family="sans-serif")

        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.show()



if __name__=='__main__':
    file_path=r"source/追溯网络数据/实体追溯网络/溯源三层网络/cluster_tracefrom_df_news.csv"
    bitcoin_net=deal_net(file_path)

    bitcoin_net.clique(3)
    # bitcoin_net.get_net_features()
    # bitcoin_net.draw()