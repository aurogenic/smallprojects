class Queue:
    def __init__(self, lst =[]):
        self.data  = []

    def push(self, value):
        self.data.append(value)

    def pop(self):
        if self.isEmpty():
            return "QUEUE IS EMPTY"
        val = self.peek()
        self.data.pop(0)
        return val

    def peek(self):
        if self.isEmpty():
            return "QUEUE IS EMPTY"
        return self.data[0]
    
    def get(self, i):
        return self.data[i]
    
    def peekEnd(self):
        return self.data[-1]
    
    def disp(self):
        print(self.data)

    def isEmpty(self):
        return len(self.data) == 0
    
    def size(self):
        return len(self.data) 


def main():
    q = Queue()
    for i in range(1, 11):
        q.push(i)

    q.disp()
    print(q.pop())
    q.disp()

if __name__ == '__main__':
    main()