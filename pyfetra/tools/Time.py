


class Time:
    def __init__(self, time, increment):
        self._time = time
        self._increment = increment
        self._full = self._build_full()
        self._current_incr = 0
        self._current_time = 0.

    def _build_full(self):
        full_list =[]
        full_list.append(self._time[0])
        for i,incr in enumerate(self._increment):
            dt = (self._time[i+1]-self._time[i])/incr
            for j in range(incr):
                full_list.append(self._time[i]+dt*(j+1))
        return full_list

    def __iter__(self):
        return self

    def __next__(self):
        if ( self._current_time >= self._time[-1] ):
            self._current_time = 0.
            self._current_incr = 0
            raise StopIteration
        else:
            self._current_incr += 1
            self._current_time = self._full[self._current_incr]
            return self._current_time

    def __call__(self):
        return self._current_time

    def getIncr(self):
        return self._current_incr

    def previous(self):
        return self._full[self._current_incr -1 ]

    def dt(self):
        return self.__call__() - self.previous()



if __name__=="__main__":
    sequence = Time(time=[0.,1.], increment=[1,])
    for t in sequence:
        print( t )

    print("next")
    sequence = Time(time=[0.,1.,2.], increment=[2,5])
    for t in sequence:
        print( t )
