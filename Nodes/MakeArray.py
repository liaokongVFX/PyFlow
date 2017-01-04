from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class MakeArray(BaseNode.Node, AGNode):
    def __init__(self, name, graph, ports_number=0):
        super(MakeArray, self).__init__(name, graph,
                                      w=120, colors=Colors,
                                      spacings=Spacings)
        AGNode.__init__(self, name, graph)
        self.ports_number = ports_number
        self.id = 0

        lyt = self.add_layout()

        pb = QtGui.QPushButton('+')
        pb.clicked.connect(self.addInPort)
        prx_btn = QtGui.QGraphicsProxyWidget()
        prx_btn.setWidget(pb)
        lyt.addItem(prx_btn)

        self.height_step = pb.size().height()

        self.out_arr = self.add_output_port('out', AGPortDataTypes.tArray)

    def post_create(self):
        if self.ports_number > 0:
            for i in range(self.ports_number):
                self.addInPort()
        self.label.setPos(0, -self.label.boundingRect().height())

    def save_command(self):
        return "createNode ~type {0} ~count {4} ~x {1} ~y {2} ~n {3}\n".format(self.__class__.__name__, self.scenePos().x(), self.scenePos().y(), self.name, self.id)

    def addInPort(self):
        port = self.add_input_port(str(self.id), AGPortDataTypes.tAny)
        self.h += self.height_step
        portAffects(port, self.out_arr)
        self.id += 1
        push(self.out_arr)
        self.graph.redraw_nodes()

    @staticmethod
    def get_category():
        return 'Array'

    def compute(self):
        self.out_arr.set_data(list([i.get_data() for i in self.inputs]), False)
