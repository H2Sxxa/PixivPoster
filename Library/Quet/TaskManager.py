from abc import ABC, abstractmethod
from json import loads
from uuid import uuid4
class _Task(ABC):
    @abstractmethod
    def __init__(self, taskfile:str) -> None:
        '''
        myTask=Task("./task.txt")
        '''
    @abstractmethod
    def setArgsTasks(self,taskname:str,func) -> None:
        '''
        it will find args itself task["args"]
        only str
        '''
    @abstractmethod
    def getTasks(self) -> dict:
        '''
        return the result of the tasks {taskname:result}
        '''
    @abstractmethod
    def setTask(self, taskname:str, func, *args, **kwargs) -> None:
        '''
        myTask.setTask("task1",print,1)
        '''
    @abstractmethod
    def runTask(self) -> None:
        '''
        myTask.runTask
        '''
        
class Task(_Task):
    def __init__(self,taskfile):
        super().__init__(taskfile=taskfile)
        tasklist=open(taskfile,"r",encoding="utf-8").read().splitlines()
        self.taskdict={}
        self.taskargs={}
        self.taskresult={}
        self.tasklist=[]
        for task in tasklist:
            self.tasklist.append(loads(task))
    def getTasks(self):
        super().getTasks()
        return self.taskresult
    def setArgsTasks(self,taskname,func):
        self.taskdict.update({taskname:func})
        self.taskargs.update({taskname+"_args":"$args"})
    def setTask(self,taskname,func,*args,**kwargs):
        super().setTask(taskname,func,*args,**kwargs)
        self.taskdict.update({taskname:func})
        self.taskargs.update({taskname+"_args":args,taskname+"_kwargs":kwargs})
    def runTask(self):
        super().runTask()
        for task in self.tasklist:
            if "task" not in task.keys():
                self.taskresult.update({})
                continue
            if "name" not in task.keys():
                task.update({"name":"%s:%s" % (uuid4(),task["task"])})
            if task["task"] in self.taskdict.keys():
                print(task)
                try:
                    if self.taskargs[task["task"]+"_args"] == "$args":
                        res=self.taskdict[task["task"]](task["args"])
                    else:
                        res=self.taskdict[task["task"]](*self.taskargs[task["task"]+"_args"],**self.taskargs[task["task"]+"_kwargs"])
                    self.taskresult.update({task["name"]:res})
                except Exception as e:
                    self.taskresult.update({task["name"]:e})
            else:
                self.taskresult.update({task["name"]:"unknown task"})