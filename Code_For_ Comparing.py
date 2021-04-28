with open(r"DBScan_Dataset.txt", "r+") as f: file_data = f.readlines()
data = [[float(i) for i in line.strip().split("\t")] for line in file_data]
data = [tuple(data_point) for data_point in data]
import math
distances = {i:[math.sqrt(((j[0]-i[0])*(j[0]-i[0]))+((j[1]-i[1])*(j[1]-i[1])))for j in data] for i in data}

def checking_point(data_point,class_number,neighbours,info, new_classification, from_number = 0, minpts = 5, eps= 1.5):
    if info[data_point][1] == 0:
        info[data_point][1] =1
        list_of_neighbours = []
        t= 0
        for distance in distances[data_point]:
            if distance < eps:
                list_of_neighbours.append(data[t])
            t=t+1
        neighbours[data_point] = list_of_neighbours
        if minpts < len(list_of_neighbours):
            info[data_point][0] = class_number #class which they belong to

            if class_number in new_classification:
                new_classification[class_number].add(data_point)
            else:
                new_classification[class_number] = {data_point}
            
            for point in list_of_neighbours:
                checking_point(point,class_number,neighbours = neighbours,info=info, new_classification = new_classification, from_number = 1, minpts=minpts, eps=eps)
            return 1
        if len(list_of_neighbours) <= minpts and from_number == 1:
            info[data_point][0] = class_number #class which they belong to
            info[data_point][1] = 2 #indicates that they are boundary points
            new_classification[class_number].add(data_point)
    return 0

def give_accuracy(minpts, eps):

    neighbours = {}
    new_classification = {} #classification is also mentioned over here
    info = {i:[-1,0] for i in data} 
    class_number = 1
    
    for data_point in data:
        class_number = class_number + checking_point(data_point,class_number,neighbours = neighbours,info=info, new_classification = new_classification, from_number = 0, minpts=minpts, eps=eps)
    p = 0
    
    for i in data:
        if i[2] == info[i][0]: p+=1
    return p/len(data), len(new_classification.keys())


list_of_minpts = [2,3,4,5,6,7]
list_of_eps = [0.5,1.0,1.5,2.0,2.5,3.0,3.5]

accuracy_dict = {}
for i in list_of_minpts:
    for j in list_of_eps:
        accuracy_dict[(i,j)] = give_accuracy(i,j)
        
print(accuracy_dict)
        