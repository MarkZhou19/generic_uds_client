import cantools

db = cantools.database.load_file('DamonCANbus/Powertrain_CAN/PWT_Vhcl_CAN/PWT_CAN1.dbc')

print(db.messages)