import roku
import blessed
import yaml
import argparse
import os

t = blessed.Terminal()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help="The hostname or IP address of the Roku", nargs='?')
    parser.add_argument('-k', '--keymap', type=argparse.FileType('r'), help="A key map")
    args = parser.parse_args()

    # Create a roku
    r = None
    if args.host:
        r = roku.Roku(args.host)
    else:
        print("Looking for a Roku...")
        for i in range(10):
            rokus = roku.Roku('').discover()
            if len(rokus):
                r = rokus.pop()
                break
        if r:
            print(r)
        else:
            print("Failed to find a Roku")
            return

    # Load keymap
    if args.keymap:
        keymap_data = args.keymap.read()
    else:
        path = os.path.join(os.path.dirname(__file__), 'keys.yaml')
        with open(path) as f:
            keymap_data = f.read()
    keymap = yaml.safe_load(keymap_data)

    # Process keymap
    keys = {}
    for k in keymap:
        code = None
        if type(k) == int:
            code = k
        else:
            try:
                code = ord(k)
            except:
                code = getattr(t, k)
        if code:
            keys[code] = getattr(r, keymap[k])
        else:
            print("Failed to parse key {}".format(k))

    print("Press 'q' to exit or 'm' to print the key map.")

    # Start capturing keys
    try:
        with t.cbreak():
            k = None
            while k not in ['q', 'Q']:
                k = t.inkey()
                code = k.code or ord(k)
                # print(str(k), k.name, k.code, code)
                if str(k) == 'm':
                    print("Key map:")
                    print(yaml.dump(keymap, default_flow_style=False))
                elif code in keys:
                    keys[code]()
    except KeyboardInterrupt:
        pass
