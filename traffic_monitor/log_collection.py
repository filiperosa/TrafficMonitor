
from typing import Union, List
from traffic_monitor.log import Log

class LogCollection:
    """ Collection of logs, keeping track of oldest and newest log """

    def __init__(self, logs: List[Log] = None):
        if logs is None:
            logs = []
        self.logs = logs
        self.min = None
        self.max = None

        if len(self.logs):
            self.min = self._search_new_min()
            self.max = self._search_new_max()

    def append(self, log: Log):
        """ Append log to collection """
        if self.min is None or log.timestamp < self.logs[self.min].timestamp:
            self.min = self.__len__()
        if self.max is None or log.timestamp > self.logs[self.max].timestamp:
            self.max = self.__len__()
        
        self.logs.append(log)        

    def get_oldest(self) -> Union[Log,None]:
        """ Get oldest log """
        if self.min is None:
            return None

        return self.logs[self.min]

    def get_newest(self) -> Union[Log,None]:
        """ Get newest log """
        if self.max is None:
            return None
        return self.logs[self.max]
    
    def pop_oldest(self) -> Union[Log,None]:
        """ Pop oldest log """

        if self.min is None:
            return None

        log = self.logs.pop(self.min)

        self.max = max(self.max - 1, 0)
        # select log with minimum timestamp
        if len(self.logs):
            self.min = self._search_new_min()

            # In the remote case where the index of min is greater than the max
            if(self.min > self.max):
                self.max = self._search_new_max()
        else:
            self.min = None
            self.max = None


        return log
    
    def pop_newest(self) -> Union[Log,None]:
        """ Pop newest log """

        if self.max is None:
            return None

        log = self.logs.pop(self.max)

        # select log with maximum timestamp
        if len(self.logs):
            self.max = self._search_new_max()

            # In the remote case where the index of min is greater than the max
            if(self.min > self.max):
                self.min = self._search_new_min()
        else:
            self.max = None

        return log
    
    def clear(self):
        """ Empty log collection """
        self.__init__()

    def __len__(self):
        return len(self.logs)
    
    def __iter__(self):
        return iter(self.logs)
    
    def __str__(self):
        return f" oldest: {self.min} newest: {self.max}, logs: {[log.timestamp for log in self.logs]}"
    
    def _search_new_min(self, neighbourhood=20):
        """
        Search for new min index close to the beginning of the list

        args:
            neighbourhood: number of elements to search for new min
        """
        to_index = min(neighbourhood, len(self.logs))
        indexes = range(0, to_index)

        if len(self.logs):
            return min(indexes, key=lambda i: self.logs[i].timestamp)
        
        return None
    
    def _search_new_max(self, neighbourhood=20):
        """
        Search for new max index close the the end of the list
        args:
            neighbourhood: number of elements to search for new max
        """
        from_index = max(len(self.logs) - neighbourhood, 0)
        indexes = range(from_index, len(self.logs)).__reversed__()

        if len(self.logs):
            return max(indexes, key=lambda i: self.logs[i].timestamp)
        
        return None

        
    