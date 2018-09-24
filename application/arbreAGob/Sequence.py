#!/usr/bin/python2.7

class Sequence:

    def __init__( self, string_description ):
        # format : 
        # n1,n2,n3,n4#ordered#Jukebox#win
        print string_description
        seq = string_description.split('#')[0].strip().split(',')
        ordered = string_description.split('#')[1].strip() == "True"
        jukebox = string_description.split('#')[2].strip() == "True"
        win = string_description.split('#')[3].strip()
        self.jukebox = jukebox
        self.ordered = ordered
        self.seq = seq
        self.current = []
        self.win = win

    def __str__( self ):
        print "seq : "
        print self.seq
        print "Ordered :"
        print self.ordered
        print "JukeBox :"
        print self.jukebox
        print "win :"
        print self.win

    def addCode( self, code ):
        if code not in self.current:
            self.current.append( code )

    def reset( self ):
        self.current = []

    def canBechecked( self ):
        return len( self.current ) == len( self.seq )

    def isValid( self ):
        if not self.canBechecked( ):
            return False
        
        tempSeq = list( self.seq )
        tempCur = list( self.current )
        self.current = []

        if self.ordered:
            return tempSeq == tempCur 

        while tempCur:
            value = tempCur.pop()
            if value not in tempSeq:
                return False
            tempSeq.remove( value )
        return True

