from mininet.topo import Topo

class StopAndWaitTopo(Topo):
    def build(self):
        client = self.addHost('h1', ip='10.0.0.1/24')
        server = self.addHost('h2', ip='10.0.0.8/24')
        switch = self.addSwitch('s1')

        self.addLink(client, switch, bw=10, delay='100ms', loss=0)
        self.addLink(server, switch, bw=10, delay='100ms', loss=0)

topos = {'stopandwait': (lambda: StopAndWaitTopo())}
