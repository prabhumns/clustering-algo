#Reading
with open(r"DBScan_Dataset.txt", "r+") as f: file_data = f.readlines() #opening file and reading data
data = [[float(i) for i in line.strip().split("\t")] for line in file_data] 
data = [tuple(data_point) for data_point in data] #making each one the data as a tuple along with the ground truth
import math
distances = {i:[math.sqrt(((j[0]-i[0])*(j[0]-i[0]))+((j[1]-i[1])*(j[1]-i[1])))for j in data] for i in data} #has all the distances stored in it

#This has the information collected during classififcation
info = {i:[-1,0] for i in data} #first one represent the new classification and second whether it is already verified or not to prevent infinte loop

#test values
minpts = 5
eps = 1.5 

neighbours = {} #Neighbours are stored over here
new_classification = {} #classification is also mentioned over here

def checking_point(data_point,class_number, from_number = 0):
    if info[data_point][1] == 0: #whether the data point is verified or not previously
        info[data_point][1] =1 #marking it as verified
        list_of_neighbours = [] 
        t= 0
        for distance in distances[data_point]:
            if distance < eps:
                list_of_neighbours.append(data[t])
            t=t+1
        neighbours[data_point] = list_of_neighbours #neighbours of each point are mentioned in dict
        if minpts < len(list_of_neighbours): #If they are core points
            info[data_point][0] = class_number #class which they belong to

            if class_number in new_classification:
                new_classification[class_number].add(data_point)
            else:
                new_classification[class_number] = {data_point}
            
            for point in list_of_neighbours: #Neighbours also will be checked just after the base point
                checking_point(point,class_number,from_number=1) #from_number indicates whether it is a new point or called from other point
            return 1

        if len(list_of_neighbours) <= minpts and from_number == 1: #Boundary points
            info[data_point][0] = class_number #class which they belong to
            new_classification[class_number].add(data_point)

    return 0

class_number = 1
for data_point in data:
    class_number = class_number + checking_point(data_point,class_number) 
    
print(new_classification.keys()) #Shows the classes that were created

p = 0
for i in data:
    if i[2] == info[i][0]: p+=1 #accuracy calculation
print (p/len(data))

