import json

# FIXME: This program doesn't work, do it manually
def main():
    print('RESETING database')
    
    empty_list = []
    port_list = [
        {
            "boat_count": 0,
            "port_name": "BREST"
        },
        {
            "boat_count": 0,
            "port_name": "VALENCIA"
        },
        {
            "boat_count": 0,
            "port_name": "PALERMO"
        },
        {
            "boat_count": 0,
            "port_name": "BRIGHTON"
        },
        {
            "boat_count": 0,
            "port_name": "AMSTERDAM"
        }
    ]
    
    with open('data/port_classifier.json', 'w') as outfile:
        json.dump(port_list, outfile, indent=4, sort_keys=True)
    with open('data/at_port_boat.json', 'w') as outfile:
        json.dump(empty_list, outfile, indent=4, sort_keys=True)
    with open('data/at_sea_boat.json', 'w') as outfile:
        json.dump(empty_list, outfile, indent=4, sort_keys=True)
        
    print("All data has been reset")
