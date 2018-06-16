'''
Transmogrifier - Translates config files into code and reports
'''

import lib.cmdline
import plugins.transmogrifiers

lib.cmdline.build()


def main():
    ''' The main method '''

    args = lib.cmdline.parse()

    plugins.transmogrifiers.execute(args)


if __name__ == '__main__':
    main()
    print("Done")

