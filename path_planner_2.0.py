import cv2

import random

green = (0, 255, 0)
red = (0, 0, 255)
black = (0, 0, 0)
blue = (255,0,0)

class point:
    x = None
    y = None
    parent = None
    links =[]
    g = 0
    h = 0
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.links=[]

    def show(self):
        print(self.x,",",self.y)

    def attach_pt(self,pt):
        (self.links).append(pt)

    def parent(self,pt):
        self.parent=pt
        self.g = pt.g+get_distance(self,pt)

    def set_h(self,end):
        self.h = get_distance(self,end)



def check_collision(point,image):

    if image[int(point.y)][int(point.x)] <100 :
        return True
    else:
        return False
def random_sampling_algo(image,N):


    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (T, image) = cv2.threshold(image, 155, 255, cv2.THRESH_BINARY)


    points = []
    for i in range(N):


        done = 0

        while (not done):
            x = random.randint(0,image.shape[0]-1)
            y = random.randint(0,image.shape[1]-1)
            pt = point(x,y)

            if (not check_collision(point(x,y),image)):
                done = 1
                points.append(point(x,y))
                break
    for i in range(len(points)):
        x = 1
        #points[i].show()
    #print("Total:",len(points))
    return points





def show_points(image,points):

    bg = image.copy()
    bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
    (T, bg) = cv2.threshold(bg, 155, 255, cv2.THRESH_BINARY)

    for i in range(len(points)):

        cv2.circle(image,(points[i].x,points[i].y),3,red,1)
        #print("Point:",points[i].show() ,"    Value: ",bg[points[i].x][points[i].y])
        #cv2.imshow("POINTS", image)
        #cv2.waitKey(0)

    cv2.imshow("POINTS",image)
    cv2.waitKey(0)

    cv2.imwrite("points.png",image)
    return image

def get_distance(element,pt):
    return ((element.x-pt.x)**2 + (element.y - pt.y)**2)**0.5


def expand_pt(pt,points):
    for i in range(len(points)):
        if (are_same(pt,points[i])):
            print("found the point")
            print("pt links:",len(points[i].links))
            return points[i].links


def get_connected(points,image,k):
    copy = image.copy()
    for i in range(len(points)):
        pt = points[i]

        temp =list (points)
        #print("Anchor pt:")
        #pt.show()
        #print("============")

        temp = sorted(temp,key=lambda element: get_distance(element,pt))

        k_nearest = temp[1:k+1]
        #print("Before:",len(pt.links))
        for x in range(len(k_nearest)):


            if (check_line(pt,k_nearest[x],image)):

                cv2.line(copy,(pt.x,pt.y),(k_nearest[x].x,k_nearest[x].y),green,1)
                points[i].attach_pt(k_nearest[x])
                #print("attaching")
            else:
                    continue
                    #cv2.line(copy, (pt.x, pt.y), (k_nearest[x].x, k_nearest[x].y), red, 1)
        #print("after:",len(pt.links))
        #cv2.imshow("image", copy)
        #cv2.waitKey(0)

    #cv2.imshow("Before", copy)
    #cv2.waitKey(0)
    return copy

def show_connections(image,points):
    for i in range(len(points)):

        for j in range(len(points[i].links)):
            if i == len(points)-1 or i == len(points)-2:
              cv2.circle(image,(points[i].x,points[i].y),6,blue,-1)
            else:
                cv2.circle(image, (points[i].x, points[i].y), 3, red, -1)
            cv2.line(image,(points[i].x,points[i].y),(points[i].links[j].x,points[i].links[j].y),green,1)
            cv2.circle(image, (points[i].links[j].x,points[i].links[j].y), 3, red, -1)

    cv2.imshow("Network:",image)
    cv2.imwrite("network.png",image)
    cv2.waitKey(0)
    return image
def check_line(p1,p2,image):
    x1 = p1.x
    y1 = p1.y

    x2 = p2.x
    y2 = p2.y
    bg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (T, bg) = cv2.threshold(bg, 155, 255, cv2.THRESH_BINARY)
    if x1 == x2:
        if (y1<y2):
         for y in range(y1,y2):
             pt = point(x1,y)

             if (check_collision(pt,bg)):
                 return False

         return True
        else:
            for y in range(y2, y1):
                pt = point(x2, y)

                if (check_collision(pt, bg)):
                    return False

            return True
    else:
        m = (y2-y1)/(x2-x1)

        if x1<x2:
            for i in range(x1,x2):
                pt = point(i,m*(i-x1)+y1)
                if (check_collision(pt,bg)):
                    return False
            return True
        else:
            for i in range(x2,x1):
                pt = point(i,m*(i-x1)+y1)
                if (check_collision(pt,bg)):
                    return False
            return True



def add_start_end(start,end,image,points,k):
    temp = sorted(points, key=lambda element: get_distance(element, start))
    copy = image.copy()
    k_nearest = temp[1:k + 1]

    for x in range(len(k_nearest)):

        if (check_line(start, k_nearest[x], image)):

            cv2.line(copy, (start.x, start.y), (k_nearest[x].x, k_nearest[x].y), red, 1)
            start.attach_pt(k_nearest[x])
        else:
            continue
            # cv2.line(copy, (pt.x, pt.y), (k_nearest[x].x, k_nearest[x].y), red, 1)

    temp = sorted(points, key=lambda element: get_distance(element, end))

    k_nearest = temp[1:k + 1]

    for x in range(len(k_nearest)):

        if (check_line(end, k_nearest[x], image)):

            cv2.line(copy, (end.x, end.y), (k_nearest[x].x, k_nearest[x].y), red, 1)
            end.attach_pt(k_nearest[x])


        else:
            continue
            # cv2.line(copy, (pt.x, pt.y), (k_nearest[x].x, k_nearest[x].y), red, 1)

    for z in range(len(points)):
           for x in range(len(end.links)):

               if are_same(points[z],end.links[x]):
                   points[z].attach_pt(end)


    points.append(start)
    points.append(end)
    #cv2.imshow("image",copy)
    #cv2.waitKey(0)

    return points
def show_path(path,image):
    print("Path:")
    for i in range(len(path)-1):
        cv2.circle(image,(path[i].x,path[i].y),3,blue,-1)
        cv2.line(image,(path[i].x,path[i].y),(path[i+1].x,path[i+1].y),blue,2)
        print(path[i].x,",",path[i].y)
    cv2.circle(image,(path[-1].x,path[-1].y),3,blue,3,-1)
    print(path[-1].x, ",", path[-1].y)
    cv2.imshow("PATH",image)
    cv2.imwrite("final_route.png",image)
    cv2.waitKey(0)
def are_same(pt1,pt2):
    if (pt1.x == pt2.x and pt1.y == pt2.y and len(pt1.links) == len(pt2.links)):
        return True
    else:
        return False

def goal_reached(current_node,end):
    if (are_same(current_node,end)):
        return True
    else:
        return False

def get_cost(pt,end):
    return pt.g + get_distance(pt,end)

def found_in(pt,fringe):
    for i in range(len(fringe)):
        if (are_same(pt,fringe[i])):
            return True

    return False

def occurences(pt,fringe):
    count = 0
    for i in range(len(fringe)):
        if are_same(pt,fringe[i]):
            count+=1

    return count


def astar_search(start,end,points):
    visited = []
    fringe = []
    visited.append(start)
    current_node = start

    while not (goal_reached(current_node, end)):

        exps = current_node.links

        for x in range(len(exps)):
            #exps[x].g = current_node.g + get_cost(current_node, exps[x])
            if not (found_in(exps[x], visited)) and not (found_in(exps[x], fringe)):
                exps[x].parent(current_node)
                fringe.append(exps[x])
        #print("current G",current_node.g)
        fringe = sorted(fringe, key=lambda pt: pt.g + get_cost(pt, end))


        temp_node = fringe[0]
        fringe.pop(0)
        #temp_node.parent(current_node)

        visited.append(temp_node)


        current_node = temp_node



    print("GOAL FOUND!!!!!")
    count = 0
    path = []
    path.append(end)
    while not (are_same(current_node, start)):
        current_node = current_node.parent
        path.append(current_node)

    path.reverse()

    return  path




image = cv2.imread("path.png")
orig = image.copy()

points = random_sampling_algo(image,800)

image = get_connected(points,image,7)

start = point(10,10)
end = point(400,450)
points = add_start_end(start,end,orig,points,7)

image = show_connections(orig,points)


path = astar_search(start,end,points)
show_path(path, image)






