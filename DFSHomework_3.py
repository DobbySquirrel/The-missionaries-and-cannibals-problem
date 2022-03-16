# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 18:54:11 2022

@author: dobby
"""

import networkx as nx
import matplotlib.pyplot as plt
 
WALKABLE = 'walkable'
PARENT = 'parent'
VISITED = 'visited'
 
#3维网格图 
def my_graph(m,c,b):
    plt.subplots(1,1,figsize=(15,7))
    G=nx.Graph()
    #若b发生变化则以下结点的生成规则需要更改
    G.add_edges_from([
    ((x,y,0), (x,y+1,1))
    for x in range(m+1)
    for y in range(c)
    ] + [
    ((x,y,0), (x+1,y,1))
    for x in range(m)
    for y in range(c+1)
    ])#右岸->左岸之间可去1人
    G.add_edges_from([
    ((x,y,0), (x+1,y+1,1))
    for x in range(m)
    for y in range(c)
    ] + [
    ((x,y,0), (x+2,y,1))
    for x in range(m-1)
    for y in range(c+1)
    ] + [
    ((x,y,0), (x,y+2,1))
    for x in range(m+1)
    for y in range(c-1)
    ])#右岸->左岸可去2人
    pos = nx.spring_layout(G, iterations=100)
    nx.draw_networkx(G, pos=pos,
                     font_size=7,
                     font_color='white',
                     node_size=500,
                     width=1)
    START = (m,c,1)
    GOAL = (0,0,0)
 
    road_closed_nodes = dummy_nodes(G,m,c,b)

    nx.draw_networkx_nodes(
        G, pos,
        nodelist=road_closed_nodes,
        node_size=500,
        node_color="red",
        node_shape="x",
        label='x'
    )
 
    dfs(G, START, GOAL)# 基于栈实深度优先遍历搜索
    try:
        path = find_path_by_parent(G, START, GOAL)
    except:
        print("该种情况没有可行路径")
        return;
    print('path', path)
 
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=path,
        node_size=400,
        node_color="green",
        node_shape='o',
    )
 
 
    path_edges = []
    for i in range(len(path)):
        if (i + 1) == len(path):
            break
        path_edges.append((path[i], path[i + 1]))
 
    print('path_edges', path_edges)
 
    # 把path着色加粗重新描边
    G2=G.to_directed()
    nx.draw_networkx_edges(G2, pos,
                           edgelist=path_edges,
                           width=4,
                           alpha=0.5,
                           edge_color="g")
 
    plt.axis('off')
    plt.show()
 
 
# 基于栈的深度优先遍历搜索
def dfs(G, START, GOAL):
    for n in G.nodes():
        G.nodes[n]['visited'] = False#初始所有点都是未被访问的
 
    stack = []  # 用列表当作一个栈，只在栈顶操作（数组的第1个位置）
    stack.append(START)
    close_list = []
    while True:
        if len(stack) == 0:
            break
 
        print('-----')
        print('stack-', stack)
 
        visit_node = stack[0]
        G.nodes[visit_node]['visited'] = True
        print('访问', visit_node)
 
        if visit_node == GOAL:
            break
 
        close_list.append(visit_node)#已访问的节点
 
        count = 0
        neighbors = nx.neighbors(G, visit_node)#寻找visit_node周围的结点 
        for node in neighbors:#依次遍历visit_node周围的节点
            visited = G.nodes[node][VISITED]
            try:
                walkable = G.nodes[node][WALKABLE]#如果存在之前设定的WALKABLE则为阻碍点
            except:
                walkable = True
 
            if (visited) or (node in stack) or (node in close_list) or (not walkable):
                continue
 #如果结点被访问，或者在将要访问的stack中，或者在已被记录的最短路径close_list中，或者是阻碍点 则跳过
    
            G.nodes[node][PARENT] = visit_node#设定该找到的节点node的父节点为visit_node，改变G
            stack.append(node)#将node压入stack
            count = count + 1#计数
 
        if count == 0:#该节点下没有节点被压入
            print(visit_node, '尽头')
            del (stack[0])
            print('弹出', visit_node)
 
        print('stack--', stack)#显示进入下次循环的stack
 
    return stack
 
 
def find_path_by_parent(G, START, GOAL):
    t = GOAL
    path = [t]
    is_find = False
    while not is_find:
        for n in G.nodes(data=True):#G.nodes第一个是结点的数据，第二个是字典存储的结点属性
            if n[0] == t:
                parent = n[1][PARENT]#找Node中parent属性存储的信息
                path.append(parent)
 
                if parent == START:#找到开始结点
                    is_find = True
                    break
 
                t = parent
 
    path.reverse()#从GOAL->START需要翻转
    return path
  
def dummy_nodes(G,m,c,b):

    list1=[];
    #list1.append((m,c,0))#去右岸时，船未携带人 不需要考虑本不在生成点中
    #list1.append((0,0,1))#左岸无人却有船  不需要考虑本不在生成点中
    for i in range(m+1):
        for j in range(c+1):
            if(i<j and i!=0):#左岸野人会袭击传教士的情况
                p=(i,j,0)
                q=(i,j,1)
                list1.append(p)
                list1.append(q)
        
            if(m-i<c-j and m-i!=0):#右岸野人会袭击传教士的情况
                p=(i,j,0)
                q=(i,j,1)
                list1.append(p)
                list1.append(q)
    for i in list1:
        G.nodes[i][WALKABLE] = False
    
    return list1
  
if __name__ == '__main__':
    m=3#自定义修道士数
    c=3#自定义野人数
    b=2
    my_graph(m,c,b)