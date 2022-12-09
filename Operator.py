import numpy as np
import GPTree
import InitialPopulation
class Operator(object):
    def crossover(self,population,fitness,TERMINALS,FUNCTIONS):
        #交叉操作
        #需要把选中的节点所包括的所有child替换
        #之后更新tree结构
        gptree = GPTree.GPTree()
        pop_size=np.shape(population)[0]
        idx1=np.random.randint(0,pop_size)
        idx2=np.random.randint(0,pop_size)
        while idx1 == idx2:
            idx2 = np.random.randint(0, pop_size)
        #后面考虑解决
        #idx1=np.random.choice(pop_size,size=1,p=fitness)
        individual1 = population[idx1]
        individual2 = population[idx2]
        #选取非terminal进行操作
        max_depth1=individual1[np.shape(individual1)[0]-1, 1]
        max_depth2 = individual2[np.shape(individual2)[0] - 1, 1]
        node1_idx = np.random.randint(2, max(max_depth1,3))
        node2_idx = np.random.randint(2, max(max_depth2,3))
        subtree1 = gptree.sub_tree(individual1[node1_idx-1, 0], individual1)
        subtree2 = gptree.sub_tree(individual2[node2_idx-1, 0], individual2)
        #插入新结构前需要调整子树2的层数
        depth1=individual1[node1_idx-1, 1]
        depth2=individual2[node2_idx-1, 1]
        subtract=depth1-depth2
        subtree2[:, 1]=subtree2[:, 1]+subtract
        # 需要处理individual1中重复的问题
        subtree2=self.repair(individual1,subtree1,subtree2,TERMINALS,FUNCTIONS)
        for i in range(np.shape(subtree1)[0]):
            delete_idx=np.where(individual1[:,0]==subtree1[i,0])
            individual1 = np.delete(individual1,delete_idx , axis=0)
        need_repair_parent_id=subtree1[0,2]
        parent_idx=np.where(individual1[:, 0] ==need_repair_parent_id)
        if individual1[parent_idx,3]==subtree1[0,0]:
            individual1[parent_idx, 3]=subtree2[0,0]
        else:
            individual1[parent_idx, 4] = subtree2[0, 0]
        #需要把和上面连接修复
        individual1 = np.vstack((individual1,subtree2))
        individual1=individual1[np.argsort(individual1[:,1]),:]
        population[idx1]=individual1
        individual2= InitialPopulation.initialPopulation_half(1,2, max_depth2, TERMINALS, FUNCTIONS)[0]
        population[idx2] =individual2
        #idx1,idx2=np.where(individual1[:,:]==5)
        return population

    def mutation(self,population,beta,TERMINALS,FUNCTIONS):
        pop_size=np.shape(population)[0]
        for i in range(pop_size):
            if np.random.rand()<=beta:
                # 随机选一个个体，然后随机一个node
                indi_idx = np.random.randint(0, pop_size)
                individual = population[indi_idx]
                node_num=np.shape(individual)[0]
                # 需要查找已经使用过的，随机替换一个
                max_length = len(TERMINALS) + len(FUNCTIONS)
                is_used = np.zeros(max_length, dtype='int64')
                for i in range(np.shape(individual)[0]):
                    id = individual[i, 0] - 1
                    is_used[id] = 1
                function_used = is_used[0:(len(FUNCTIONS))]
                terminal_used = is_used[len(FUNCTIONS):max_length]
                node_idx=np.random.randint(0, node_num)
                old_id=np.copy(individual[node_idx,0])
                # 两种情况
                if individual[node_idx,0]>len(FUNCTIONS):
                    idx=np.random.randint(0,len(TERMINALS))
                    while(terminal_used[idx]==1):
                        idx = np.random.randint(0, len(TERMINALS))
                    terminal_used[idx]=1
                    terminal_used[individual[node_idx,0]-1-len(FUNCTIONS)]=0
                    idx=idx+len(FUNCTIONS)
                else:
                    idx=np.random.randint(0,len(FUNCTIONS))
                    while(function_used[idx]==1):
                        idx = np.random.randint(0, len(FUNCTIONS))
                    function_used[idx] = 1
                    function_used[individual[node_idx, 0] - 1] = 0
                new_id=idx+1
                # 修复parent
                individual[node_idx, 0]=new_id
                if old_id in individual[:, 3]:
                    idx_temp = np.where(individual[:, 3] == old_id)
                    if individual[idx_temp,3]==old_id:
                        individual[idx_temp, 3]=new_id
                if old_id in individual[:, 4]:
                    idx_temp = np.where(individual[:, 4] == old_id)
                    if individual[idx_temp,4]==old_id:
                        individual[idx_temp, 4]=new_id
                # 修复child
                if old_id in individual[:,2]:
                    individual[np.where(individual[:, 2] == old_id), 2] = new_id
                population[i]=individual


        return population

    def repair(self,individual,subtree1,subtree2,TERMINALS,FUNCTIONS):
        #查找已经使用的，然后在子树中看是否有使用
        max_length=len(TERMINALS)+len(FUNCTIONS)
        is_used=np.zeros(max_length,dtype='int64')
        for i in range(np.shape(individual)[0]):
            id=individual[i,0]-1
            is_used[id]=1
        for i in range(np.shape(subtree1)[0]):
            id=subtree1[i,0]-1
            is_used[id]=0
        #还要考虑有没有在子树2用过
        for i in range(np.shape(subtree2)[0]):
            id=subtree2[i,0]-1
            is_used[id]=1
        #开始修复过程
        function_used=is_used[0:(len(FUNCTIONS))]
        terminal_used = is_used[len(FUNCTIONS):max_length]
        for i in  range(np.shape(subtree2)[0]):
            id=subtree2[i,0]-1
            if is_used[id]==1:
                #根据function还是terminal判断
                if subtree2[i,0]>len(FUNCTIONS):
                    idx=np.random.randint(0,len(TERMINALS))
                    while(terminal_used[idx]==1):
                        idx = np.random.randint(0, len(TERMINALS))
                    terminal_used[idx]=1
                    idx=idx+len(FUNCTIONS)
                else:
                    idx=np.random.randint(0,len(FUNCTIONS))
                    while(function_used[idx]==1):
                        idx = np.random.randint(0, len(FUNCTIONS))
                    function_used[idx] = 1
                #新编号
                new_id=idx+1
                #对之前位置的替换，需要分别替换自己，和parent的连接
                old_id=np.copy(subtree2[i, 0])
                subtree2[i, 0] = new_id
                parent_id=subtree2[i,2]

                if parent_id in subtree2[:, 0]:
                    idx_temp = np.where(subtree2[:, 0] == parent_id)
                    if subtree2[idx_temp,3]==old_id:
                        subtree2[idx_temp, 3]=new_id
                    else:
                        subtree2[idx_temp, 4] = new_id
                #调整自己的child
                subtree2[np.where(subtree2[:,2]==old_id),2]=new_id
        return subtree2