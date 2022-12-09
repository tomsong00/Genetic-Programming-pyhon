import numpy as np
import random
import GPTree


gptree=GPTree.GPTree()

def initialPopulation_half(population_size,MIN_DEPTH,MAX_DEPTH,TERMINALS,FUNCTIONS):
    #需要保证根是function
    #也需要保证叶子节点是Terminal
    max_node_num=gptree.node_num(MAX_DEPTH)
    #先存function，后terminal
    population = np.empty((population_size,), dtype=list)
    for i in range(population_size):
        #方法需要进一步完善，可以适当减少数量
        #修改：需要先选function，终端选terminal
        if i<population_size/2:
            #full
            function_num=gptree.node_num(MAX_DEPTH-1)
            fun_list = random.sample(range(1, len(FUNCTIONS)+1), function_num)
            if np.random.rand()<=0.5:
                terminal_num=max_node_num-function_num
            else:
                terminal_num = max_node_num - function_num-1
            terminal_list= random.sample(range(1, len(TERMINALS)+1), terminal_num)
            terminal_list=[val+len(FUNCTIONS) for val in terminal_list]
            rand_list=np.hstack((fun_list,terminal_list))
        else:
            #grow
            depth = np.random.randint(MIN_DEPTH, MAX_DEPTH + 1)
            function_num=gptree.node_num(depth-1)
            node_num = gptree.node_num(depth)
            fun_list = random.sample(range(1, len(FUNCTIONS)+1), function_num)
            if np.random.rand()<=0.5:
                terminal_num=node_num-function_num
            else:
                terminal_num = node_num - function_num-1
            terminal_list= random.sample(range(1, len(TERMINALS)+1), terminal_num)
            terminal_list = [val + len(FUNCTIONS) for val in terminal_list]
            rand_list=np.hstack((fun_list,terminal_list))
        individual = np.zeros([len(rand_list), 5], dtype=int)  # id,floor,parent,left,right
        individual[:, 0]=rand_list
        population[i]=individual
    population=gptree.build_tree(population)
    return population