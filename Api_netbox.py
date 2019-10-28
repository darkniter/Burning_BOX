from processor import ports, device, device_type, map_devices, ip_adresses, VLAN
import processor.config as config
import pynetbox
from processor.utilities.transliteration import transliterate

net_box = pynetbox.api(config.NETBOX_URL, config.TOKEN)


def Switches(region):
    ip_list = None
    # loaded maindevices
    vlans_map = Vlan_init()

    xl_map = map_devices.excel_map(config.VLAN_PATH_XL)

    for street in vlans_map[transliterate(region)]:
        if street[8] == '/23':
            filter_ip = street[3].split('-')[-1].split('.')

            filter_ip = ".".join([filter_ip[0], filter_ip[1], filter_ip[2]])

        elif street[8] == '/22':
            filter_ip = street[3].split('-')[-1].split('.')

            filter_ip = ".".join(filter_ip[0:2:1])

        map_devices.map_filtration_init(filter_ip)
    # loaded items from map
        filtred_map = map_devices.map_load(config.MAP_LOCATION)

    # setup missing types
        new_types = device_type.add_device_types('prod', filtred_map)

        print("added:", new_types)

        if len(new_types) > 0:
            # get type list for ports
            ports.init_ports(new_types)

        # add new devices from map
        info_ip = device.device_name_SWITCH(filtred_map, xl_map, street)
        print(info_ip)
        if len(info_ip) > 0:
            ip_list = ip_adresses.setup_ip(info_ip)

    return ip_list


def Vlan_init(region=None):

    vlans_map = map_devices.VLAN_map(region)
    VLAN.region_add_from_vlan(vlans_map)
    VLAN.main_add_VLANs(vlans_map)

    return vlans_map


def Modems():
    vlans_list = []
    filtred_map = map_devices.from_json(config.MODEMMAP)

    new_types = device_type.add_device_types('prod', filtred_map)
    print("added:", new_types)

    if len(new_types) > 0:
        # get type list for ports
        ports.init_ports(new_types)

    # vlans_list = Vlan_init()

    info_ip = device.device_name_MODEM(filtred_map, vlans_list)
    print('added_dev:', info_ip)

    if len(info_ip) > 0:
        ip_list = ip_adresses.setup_ip(info_ip)

    return ip_list


def load_conf_dev_type():
    new_types = device_type.add_device_types('dev')

    print("added:", new_types)

    if len(new_types) > 0:
        # get type list for ports
        ports.init_ports(new_types)


def pre_conf():
    regions = [
                'Кабаново',
                'Куровское',
                'Демихово',
                'Ликино-Дулёво',
                'Орехово-Зуево'
               ]
    for load in regions:
        Switches(load)
    return


if __name__ == "__main__":
    # pre_conf()
    Modems()
    # load_conf_dev_type()
