from sys import *
from random import *
from TOSSIM import *
from tinyos.tossim.TossimApp import *

n = NescApp()
t = Tossim(n.variables.variables())
r = t.radio()

#import the topology information...
f = open("topo.txt", "r")
lines = f.readlines()
for line in lines:
  s = line.split()
  if (len(s) > 0):
     r.add(int(s[0]), int(s[1]), float(s[2]))

#Debugging statements...
#NOTEME: dump the debugging information to the standard channel
t.addChannel("TOSMC", sys.stdout)
t.addChannel("ASSIST", sys.stdout)
t.addChannel("Event", sys.stdout);
t.addChannel("Multihop", sys.stdout);

#establish the noise model upon the noise file...
noise = open("meyer-heavy.txt", "r")
lines = noise.readlines()
for line in lines:
  str = line.strip()
  if (str != ""):
      val = int(str)
      for i in range(0, 8):
        t.getNode(i).addNoiseTraceReading(val)

for i in range (0, 8):
  print "Creating noise model for ",i;
  t.getNode(i).createNoiseModel()

#Tell how many motes are involved in the network initially
#An instruction only for T-Check (be called in the first place)
t.initMoteNum(8, 2)

#Each mote boot...
t.getNode(0).bootAtTime(1000);
t.getNode(1).bootAtTime(1001);
t.getNode(2).bootAtTime(1002);
t.getNode(3).bootAtTime(1003);
t.getNode(4).bootAtTime(1004);
t.getNode(5).bootAtTime(1005);
t.getNode(6).bootAtTime(1006);
t.getNode(7).bootAtTime(1007);

#injecting packets from serial port and radio port
#NOTEME: these instructions only are supported in abstraction mode;
#in other words, if the hardware switch is activated in Makefile, 
#the paket-level injection can't be used... 

#msg = RadioCountMsg()
#msg.set_counter(7);

#spkt = t.newSerialPacket();
#spkt.setData(msg.data)
#spkt.setType(msg.get_amType())
#spkt.setDestination(0)
#spkt.deliver(0, t.time()+3)

#pkt = t.newPacket();
#pkt.setData(msg.data)
#pkt.setType(msg.get_amType())
#pkt.setDestination(0)
#pkt.deliver(3, t.time()+10);

#Prefix execution phase
#NOTEME: continue to use the event execution mode in TOSSIM 
for i in range (0, 50000):
  t.runNextEvent()

#coarse-grain node-level non-determinism..
#NOTEME: this kind of nondeterminism is always tightly
#Always coupled with liveness property checking
#t.mcMoteDeath(1, 50)
#t.mcMoteRevival(1, 100)
#t.mcMoteReboot(1, 150)


# The transmission event's probability
# Note that these three functions should be used in conjunction
# with loss_mode equal to 3 (loss_probability); in other words, 
# if the loss_mode is not set to 3, then these three functions
# will not affect anything.
#t.setSendProb(0.7);
#t.setReceiveProb(0.7);
#t.setAckProb(0.8);

#First argument -- packet_loss_mode: 0(no_loss); 1(loss_random); 2(loss_noise); 3(loss_probability)
#Second argument -- biasing_mode: 0(flattening); 1(biasing);
#Third argument -- tossim_mode: 0(no_tossim); 1(tossim) 
#NOTEME: Please refer to howtorun.pdf file in webpage for more verbose meanings of these arguments.
t.setLossAndBiasingAndTossim(0, 1, 1);
#Activate the delta debugging function...
#NOTEME: if set, it can help shorten the buggy trace in random walk phase... 
t.setDeltaDebugging(0);

#Combination of explicit state model checking and random walk...
#First argument -- POR support or not: "DFS"(without_POR); "DFSPOR"(with_POR);
#Second argument -- DFS bound
#Third argument -- random walk bound 
t.startModelChecking("DFSPOR", 50, 100000)

#Pure random walk...
#First argument -- random walk bound
#Second argument -- random walk round
#t.startRandomWalk(100000, 10);
