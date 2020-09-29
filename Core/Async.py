import time

class Async:

    coroutines = []


    def __init__():
        pass

    def run(method):       
        coroutine = Async.RunningInstance(method)

        if coroutine.update():
            Async.coroutines.append(coroutine)

    def update():
        Async.coroutines = [x for x in Async.coroutines if x.update()]

    class RunningInstance:

        def __init__(self, generator):
            self.generator = generator
            self.next = -1.0 #Ensure code runs right away

        #Return true when there is more code to ru n
        def update(self):
            now = time.time()
            if self.next > now:
                return True
                      
            try:
                result = next(self.generator)
            except Exception as e:
                return False

            if result is None:
                self.next = -1.0
            else:
                self.next = now + result

            return True


            

            
