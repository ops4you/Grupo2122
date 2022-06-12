import argparse

#Client argument parser
def clientParse():
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)    

        parser.add_argument('ip', type=str,help='Client IP')

        parser.add_argument('-ipS', type=str,help='IPv6 Address' , default="::1")

        parser.add_argument('-sport', type=int,help='Server Port', default="5555")

        parser.add_argument('-cport', type=int,help='Client Port', default="5553")            

        args = parser.parse_args()
        return(args.ip,args.ipS,args.sport,args.cport)


#DTN argument parser
def dtnParse():
       parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)         

       parser.add_argument('ip', type=str,help='Node IP')

       parser.add_argument('port', type=str,help='Node port')

       parser.add_argument('-gw', type=int,help='1 if Gateway Node, 0 if not', default=0)