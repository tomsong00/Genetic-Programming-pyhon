import numpy as np
class GPTree(object):
    #节点数量
    def node_num(self,deepth):
        num=0
        for i in range(1,deepth+1):
            num=num+2**(i-1)
        return num
    #层数
    def depth_num(self,individual):
        depth_num=0
        for i in range(np.shape(individual)[0]):
            this_depth_max = 2 **depth_num
            if (i+1)>=depth_num+this_depth_max:
                depth_num=depth_num+1
        return depth_num

    #根据构建树结构
    def build_tree(self,population):
        for i in range(np.shape(population)[0]):
            #individual=population[i]
            depth=1
            this_depth_num=0
            for j in range(np.shape(population[i])[0]):
                this_depth_max=2**(depth-1)
                #确定层数
                if (this_depth_num+1)>this_depth_max:
                    depth=depth+1
                    this_depth_num=0
                this_depth_num=this_depth_num+1
                #确定树状结构,确定parent
                if depth==1:
                    parent=0
                if depth!=1:
                    if np.mod(j+1,2)==0:
                        parent=population[i][int((j+1)/2)-1,0]
                    else:
                        parent = population[i][int(np.floor((j+1)/2)-1),0]
                if 2*(j+1)<=np.shape(population[i])[0]:
                    #是否末端
                    left = population[i][(j + 1)*2-1, 0]
                    #判断是否存在right
                    if 2*(j+1)+1<=np.shape(population[i])[0]:
                        right= population[i][(j + 1)*2, 0]
                    else:
                        right=-1
                else:
                    #末端
                    left=-1
                    right=-1
                population[i][j, 1] = depth
                population[i][j, 2] =parent
                population[i][j, 3] =left
                population[i][j, 4] =right
        return population
    #生成表达式
    def print_best_tree(self,individual,FUNCTIONS,TERMINALS):
        return 0
    #计算树,并生成表达式
    def compute_tree(self,individual,FUNCTIONS,TERMINALS):
        #根据层数往上反推
        node_num=np.shape(individual)[0]
        #max_depth = individual[np.shape(individual)[0]-1, 1]
        length=len(FUNCTIONS)
        #按层倒序循环
        record=[]
        for j in range(node_num-1,-1,-1):
            #print(j)
            #区分是否是terminal
            if individual[j,3]!=-1:
                #是否是terminal的上一层,需要根据下一层
                #child1_id=individual[j, 3]
                child1_id =individual[j, 3]
                idx=np.where(individual[:,0]==child1_id)
                if individual[idx,4]==-1:
                    #如果有右node
                    if individual[j,4]!=-1:
                        child1=TERMINALS[(individual[j, 3] - length - 1)]
                        child2=TERMINALS[(individual[j, 4] - length - 1)]
                        result=FUNCTIONS[individual[j,0]-1](child1,child2)
                    else:
                        #如果没有右node
                        child1 = TERMINALS[(individual[j, 3] - length - 1)]
                        result=FUNCTIONS[individual[j, 0]-1](child1)
                    record.append([individual[j, 0],float(result)])
                else:
                    temp_record=np.array(record)
                    child1=np.where(temp_record[:,0]==individual[j,3])
                    child2 = np.where(temp_record[:, 0] == individual[j, 4])
                    result = FUNCTIONS[individual[j, 0] - 1](temp_record[child1,1],temp_record[child2,1])
                    record.append([individual[j, 0], float(result)])
        value=record[-1][1]
            #print(record[-1][1])
        return value
    def sub_tree(self,node,individual):
        #根据个体和输入节点编号找到子树
        node_num=np.shape(individual)[0]
        subtree=[]
        last_len=0
        scan_idx=0
        #需要保证按层排列
        # 首先需要找到该节点
        idx = np.where(individual[:, 0] == node)
        #两种情况，他本身，和他的child
        depth=int(individual[idx,1])
        parent=int(individual[idx,2])
        child1=int(individual[idx,3])
        child2=int(individual[idx,4])
        subtree.append([node,depth,parent,child1,child2])
        #之后，在child之上继续搜索，直到list不增长
        while(len(subtree)>last_len):
            last_len=len(subtree)
            for i in range(3,5):
                node=subtree[scan_idx][i]
                #if individual[idx,3]!=-1 and individual[idx,4]!=-1:
                if node in individual[:, 0]:
                    idx = np.where(individual[:, 0] == node)
                    depth = int(individual[idx, 1])
                    parent = int(individual[idx, 2])
                    child1 = int(individual[idx, 3])
                    child2 = int(individual[idx, 4])
                    subtree.append([node,depth,parent, child1, child2])
            scan_idx=scan_idx+1
        subtree=np.array(subtree)
        return subtree
