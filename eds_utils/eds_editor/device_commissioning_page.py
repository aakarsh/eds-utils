from gi.repository import Gtk

from ..core import BAUD_RATE
from ..core.eds import EDS


class DeviceCommissioningPage(Gtk.ScrolledWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.eds = None

        frame = Gtk.Frame(label='Device Commissioning', margin_top=5, margin_bottom=5,
                          margin_start=5, margin_end=5)
        frame.set_halign(Gtk.Align.START)
        frame.set_valign(Gtk.Align.START)
        self.set_child(frame)

        grid = Gtk.Grid(column_spacing=5, row_spacing=5, row_homogeneous=True,
                        margin_top=5, margin_bottom=5,
                        margin_start=5, margin_end=5)
        frame.set_child(grid)

        label = Gtk.Label.new('Node Name:')
        label.set_halign(Gtk.Align.START)
        self.node_name = Gtk.Entry()
        self.node_name.set_max_length(246)
        grid.attach(label, column=0, row=0, width=1, height=1)
        grid.attach(self.node_name, column=1, row=0, width=2, height=1)

        label = Gtk.Label.new('Network Name:')
        label.set_halign(Gtk.Align.START)
        self.network_name = Gtk.Entry()
        self.network_name.set_max_length(243)
        grid.attach(label, column=0, row=1, width=1, height=1)
        grid.attach(self.network_name, column=1, row=1, width=2, height=1)

        label = Gtk.Label.new('Node ID:')
        label.set_halign(Gtk.Align.START)
        node_id = Gtk.SpinButton()
        self.node_id = Gtk.Adjustment.new(1, 0x1, 0x7F, 1, 0, 0)
        node_id.set_adjustment(self.node_id)
        grid.attach(label, column=3, row=0, width=1, height=1)
        grid.attach(node_id, column=4, row=0, width=1, height=1)

        label = Gtk.Label.new('Net Number:')
        label.set_halign(Gtk.Align.START)
        net_number = Gtk.SpinButton()
        self.net_number = Gtk.Adjustment.new(0, 0, 0xFFFFFFFF, 1, 0, 0)
        net_number.set_adjustment(self.net_number)
        grid.attach(label, column=3, row=1, width=1, height=1)
        grid.attach(net_number, column=4, row=1, width=1, height=1)

        label = Gtk.Label.new('Baud Rate:')
        label.set_halign(Gtk.Align.START)
        grid.attach(label, column=0, row=2, width=1, height=2)
        self.baud_rate_buttons = []
        first_radio_button = None
        for i in range(len(BAUD_RATE)):
            radio_button = Gtk.CheckButton.new()
            radio_button.set_label(f'{BAUD_RATE[i]} kpbs')

            if first_radio_button is None:  # set the first_radio_button var
                first_radio_button = radio_button
            else:
                radio_button.set_group(first_radio_button)

            column = i % 4  # 0 - 3
            row = i // 4  # 0 or 1
            self.baud_rate_buttons.append(radio_button)
            grid.attach(radio_button, column=1 + column, row=2 + row, width=1, height=1)
        radio_button.set_active(True)  # 1000 kpbs

        label = Gtk.Label.new('LSS Serial Number:')
        label.set_halign(Gtk.Align.START)
        lss_serial_num = Gtk.SpinButton()
        self.lss_serial_num = Gtk.Adjustment.new(0, 0, 0xFFFFFFFF, 1, 0, 0)
        lss_serial_num.set_adjustment(self.lss_serial_num)
        grid.attach(label, column=0, row=4, width=1, height=1)
        grid.attach(lss_serial_num, column=1, row=4, width=1, height=1)

        label = Gtk.Label.new('CANopen Manager:')
        label.set_halign(Gtk.Align.START)
        self.canopen_manager = Gtk.Switch()
        self.canopen_manager.set_halign(Gtk.Align.START)
        self.canopen_manager.set_valign(Gtk.Align.CENTER)
        grid.attach(label, column=2, row=4, width=1, height=1)
        grid.attach(self.canopen_manager, column=3, row=4, width=1, height=1)

        button = Gtk.Button(label='Update')
        button.set_halign(Gtk.Align.END)
        button.set_valign(Gtk.Align.END)
        button.connect('clicked', self.on_update_button_clicked)
        grid.attach(button, column=0, row=5, width=2, height=2)

        button = Gtk.Button(label='Cancel')
        button.set_halign(Gtk.Align.START)
        button.set_valign(Gtk.Align.END)
        button.connect('clicked', self.on_cancel_button_clicked)
        grid.attach(button, column=2, row=5, width=2, height=2)

    def load_eds(self, eds: EDS):
        self.eds = eds

        # a set all the after loading the eds
        self.on_cancel_button_clicked(None)

    def on_update_button_clicked(self, button):

        device_comm = self.eds.device_commissioning
        device_comm.node_name = self.node_name.get_text()
        device_comm.node_id = int(self.node_id.get_value())
        device_comm.net_number = int(self.net_number.get_value())
        device_comm.network_name = self.network_name.get_text()
        for i in self.baud_rate_buttons:
            if i.get_active():
                index = self.baud_rate_buttons.index(i)
                device_comm.baud_rate = BAUD_RATE[index]
                break
        self.baud_rate_buttons[index].set_active(True)
        device_comm.canopen_manager = self.canopen_manager.get_state()
        device_comm.lss_serialnumber = int(self.lss_serial_num.get_value())

    def on_cancel_button_clicked(self, button):

        device_comm = self.eds.device_commissioning
        self.node_name.set_text(device_comm.node_name)
        self.node_id.set_value(device_comm.node_id)
        self.net_number.set_value(device_comm.net_number)
        self.network_name.set_text(device_comm.network_name)
        index = BAUD_RATE.index(device_comm.baud_rate)
        self.baud_rate_buttons[index].set_active(True)
        self.canopen_manager.set_state(device_comm.canopen_manager)
        self.lss_serial_num.set_value(device_comm.lss_serialnumber)
